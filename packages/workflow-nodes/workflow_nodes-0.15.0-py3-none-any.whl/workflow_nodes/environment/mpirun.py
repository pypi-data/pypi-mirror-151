# Copyright 2021 Karlsruhe Institute of Technology
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
from xmlhelpy import Integer
from xmlhelpy import option

from .main import environment


@environment.environment()
@option(
    "numofprocesses",
    char="c",
    param_type=Integer,
    description="Number of processes used",
)
@option("quiet", char="q", is_flag=True, description="Suppress helpful messages")
@option("verbose", char="v", is_flag=True, description="Be verbose")
def mpirun(numofprocesses, quiet, verbose, env_exec):
    """Run pace3D solvers on multiple processors using mpirun."""
    cmd = ["mpirun"]

    if numofprocesses:
        cmd += ["-c", str(numofprocesses)]
    if quiet:
        cmd.append("-q")
    if verbose:
        cmd.append("-v")

    cmd.append(env_exec[0])

    click.echo(cmd, err=True)
    sys.exit(subprocess.run(cmd).returncode)
