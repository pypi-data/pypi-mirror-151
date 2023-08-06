# Copyright 2022 Karlsruhe Institute of Technology
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

from xmlhelpy import argument
from xmlhelpy import option

from .main import misc


@misc.command()
@argument("infile")
@argument("outfile")
@option("input-format", char="f", description="Specifies the input file format.")
@option("output-format", char="v", description="Specifies the output file format.")
@option(
    "prune",
    char="p",
    description="Remove lower order cells, remove orphaned nodes.",
    is_flag=True,
)
def meshio_convert(infile, outfile, input_format, output_format, prune):
    """Wrapper node for meshio convert."""
    cmd = ["meshio", "convert"]

    if infile:
        cmd.append(infile)
    if outfile:
        cmd.append(outfile)
    if input_format:
        cmd += ["--input-format", input_format]
    if output_format:
        cmd += ["--output-format", output_format]
    if prune:
        cmd.append("--prune")

    sys.exit(subprocess.run(cmd).returncode)
