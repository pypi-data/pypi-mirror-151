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
from xmlhelpy import option

from .main import environment
from workflow_nodes.utils import check_binary


@environment.environment()
@option("name", char="n", default="kadi-workflow-node", description="Name the session")
@option(
    "resume",
    char="r",
    is_flag=True,
    description="Attempt to reattach previous session, if not existent, start new",
    exclude_from_xml=True,  # resume does not work without a terminal (in workflow)
)
def screen(name, resume, env_exec):
    """Execute a tool detached in the background using screen."""
    check_binary("screen")

    # Assemble command
    cmd = ["screen"]
    if resume:
        cmd += ["-d", "-R"]
        if name:
            cmd.append(name)
    else:
        if name:
            cmd += ["-S", name]

        cmd.append("-dm")
        # screen gobbles up everything by itself and doesn't like the strings parsed by
        # subprocess.run(...). Therefore, split with string manipulation
        cmd += env_exec[0].split(" ")

    click.echo(cmd, err=True)
    sys.exit(subprocess.run(cmd).returncode)
