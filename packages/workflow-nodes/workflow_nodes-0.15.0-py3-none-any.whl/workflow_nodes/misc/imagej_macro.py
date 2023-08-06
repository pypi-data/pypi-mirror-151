# Copyright 2020 Karlsruhe Institute of Technology
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import subprocess
import sys
from pathlib import Path

import click
from xmlhelpy import option

from .main import misc


@misc.command(example='--variables "my_int=1, my_string=abc" example.ijm')
@option("macro", char="m", description="path to the macro file (.ijm)", required=True)
@option(
    "variables",
    char="v",
    description="Define variables which will be inserted into the macro. Separate"
    " multiple variables by comma. Overwrites variables specified by --varfile.",
)
@option("varfile", char="f", description="Load a list of variables from a file")
@option(
    "virtual-framebuffer",
    char="x",
    description="Use a virtual framebuffer to hide windows which would be opened by"
    " imagej.",
    is_flag=True,
)
def imagej_macro(macro, variables, varfile, virtual_framebuffer):
    """A program to start an ImageJ macro with variables."""
    final_macro_filename = macro
    macro_variables = {}  # map to hold all variables

    def _split_var_definition(definition):
        var_definition = definition.split("=")
        if len(var_definition) != 2:
            raise ValueError("Invalid variable definition")
        var_name = var_definition[0].strip()
        var_value = var_definition[1].strip()
        if not var_name:
            raise ValueError(
                "Invalid variable definition: Variable names must not be empty"
            )

        return {var_name: var_value}

    # add variables added via --variable <string>
    if variables is not None:
        var_list = variables.split(",")
        for var_def in var_list:
            try:
                var_parsed = _split_var_definition(var_def)
                macro_variables.update(var_parsed)
            except ValueError:
                click.echo(
                    f"Warning: Variable definition '{var_def}' could not be parsed and"
                    " will be omitted.",
                )

    # add variables from the variable file
    if varfile is not None:
        with open(varfile, encoding="utf-8") as f:
            for line in f:
                try:
                    var_parsed = _split_var_definition(line.rstrip("\n"))
                    macro_variables.update(var_parsed)
                except ValueError:
                    click.echo(
                        f"Warning: Variable definition '{line}' could not be parsed and"
                        " will be omitted.",
                    )

    if len(macro_variables) > 0:
        final_macro_filename = ".macro.tmp.ijm"

        with Path(macro).expanduser().open(encoding="utf-8") as macro_file:
            macro_content = macro_file.read()
        with Path(final_macro_filename).expanduser().open(
            mode="w+", encoding="utf-8"
        ) as tmp_file:
            tmp_file.write("// BEGIN VARIABLES //\n")

            for name, value in macro_variables.items():
                tmp_file.write(f"{name}={value};\n")

            tmp_file.write("// END VARIABLES //\n")
            tmp_file.write("\n")
            tmp_file.write(macro_content)

    # works with Fiji imagej 1.51
    cmd = []
    if virtual_framebuffer:
        # Add xvfb-run to hide opened windows without causing trouble for imagej. Since
        # xvfb-run does not show errors by default, direct them to stdout for better
        # logging.
        cmd += [
            "xvfb-run",
            "-e",
            "/dev/stdout",
        ]
    cmd += ["imagej", "--no-splash", "--console", "-macro", final_macro_filename]

    click.echo("calling the macro...")
    click.echo(" ".join(cmd))
    click.echo("~" * 50)
    exit_code = subprocess.run(cmd).returncode
    click.echo("~" * 50)
    click.echo("done")
    sys.exit(exit_code)
