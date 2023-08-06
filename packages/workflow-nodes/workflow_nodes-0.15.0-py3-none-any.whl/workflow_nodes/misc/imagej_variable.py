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
import re
import sys
from pathlib import Path

import click
from xmlhelpy import option

from .main import misc


def _store_variable(name, outfile, value):
    if re.search("^[0-9.,]+$", value) is None:
        # this is not a number, wrap it in double quotes
        value = f'"{value}"'

    variable_str = f"{name}={value}\n"
    with Path(outfile).expanduser().open(mode="a+", encoding="utf-8") as f:
        f.write(variable_str)

    click.echo("Wrote {} to {}".format(variable_str.rstrip("\n"), outfile))


@misc.command(
    example='--name "crop_selection" --variable "[53, 132, 150, 293]" --outfile'
    ' "myvariables.imjv"'
)
@option("name", char="n", description="The name of the variable", required=True)
@option("value", char="v", description="The value of the variable", required=True)
@option(
    "outfile",
    char="o",
    description="The file used as variable store, the new variable will be appended to"
    " it",
    default=".variables.ijmv",
)
@option(
    "split_vector",
    char="s",
    is_flag=True,
    description="Split the variable value into multiple variables. The format must be"
    " [a, b, c, d, e...] where each item will be treated as a variable itself with the"
    " name {$variable_name}_0, {$variable_name}_1 and so forth.",
)
def imagej_variable(name, value, outfile, split_vector):
    """Turn a string value into a variable and store it in a file."""
    if not name:
        click.echo("Error: The variable name must not be empty.")
        sys.exit(1)

    if split_vector:
        # assume the format "[a, b, c, e, f]"
        vector_str = value.strip('"')
        vector_str = vector_str.lstrip("[")
        vector_str = vector_str.rstrip("]")  # remove parantheses
        values = list(map(lambda a: a.strip(), vector_str.split(",")))
        if len(values) == 0:
            click.echo(
                f"Error: Could not split vector {vector_str} (expected format:"
                " [a, b, c, ...].",
                err=True,
            )
        for (i, v) in enumerate(values):
            _store_variable(f"{name}_{i}", outfile, v)

    else:
        _store_variable(name, outfile, value)
