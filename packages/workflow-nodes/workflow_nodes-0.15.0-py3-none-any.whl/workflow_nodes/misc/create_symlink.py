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


@misc.command()
@option("target", char="t", description="Symlink target (default is current directory)")
@option("path", char="p", description="Path where the symlink should be stored.")
@option("name", char="n", description="Name of the Desktop entry", required=True)
@option(
    "force",
    char="f",
    description="Force symlink creation (overwrite if exists)",
    is_flag=True,
)
def create_symlink(target, path, name, force):
    """Create a symlink."""
    symlink_target = target if target is not None else Path.cwd()
    symlink_path = Path(path).expanduser() if path is not None else Path.cwd()
    symlink_path = symlink_path.joinpath(name)

    click.echo(f"Creating symlink {symlink_path} pointing to {symlink_target}")
    cmd = ["ln", "-s"]

    if force:
        click.echo("Overwriting if existing")
        # ln's -f argument only works together with -n (no dereference)
        cmd.append("-fn")

    cmd += [str(symlink_target), str(symlink_path)]

    exit_code = subprocess.run(cmd).returncode
    click.echo("done")
    sys.exit(exit_code)
