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

import click
from xmlhelpy import argument
from xmlhelpy import option

from .main import system


@system.command()
@argument("file", description="Input file")
@option("interactive", char="i", description="Force interactive mode.", is_flag=True)
@option(
    "mathlib", char="l", description="Define the standard math library.", is_flag=True
)
@option(
    "warn",
    char="w",
    description="Give warnings for extensions to POSIX bc.",
    is_flag=True,
)
@option(
    "standard",
    char="s",
    description="Process exactly the POSIX bc language.",
    is_flag=True,
)
@option(
    "quiet",
    char="q",
    description="Do not print the normal GNU bc welcome.",
    is_flag=True,
)
def bc(file, interactive, mathlib, warn, standard, quiet):
    """Wrapper node for bc."""
    cmd = ["bc"]

    if interactive:
        cmd.append("-i")
    if mathlib:
        cmd.append("-l")
    if warn:
        cmd.append("-w")
    if standard:
        cmd.append("-s")
    if quiet:
        cmd.append("-q")
    if file:
        cmd.append(file)

    click.echo(" ".join(cmd), err=True)
    sys.exit(subprocess.run(cmd).returncode)
