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
from workflow_nodes.utils import check_binary


@environment.environment()
@option(name="user", description="Username", requires=["host"])
@option(name="host", description="Specifies the host address", requires=["user"])
@option(
    name="confighost",
    description="Use a predefined host from the ssh config",
    excludes=["host", "user"],
)
@option(name="port", description="Specifiy a certain port", param_type=Integer)
@option("x-server", char="X", description="Enables X11-forwarding", is_flag=True)
@option(
    "disable-shell-sourcing",
    char="u",
    is_flag=True,
    description="Disables sourcing the configuration files ~/.profile and ~/.bashrc",
)
def ssh(user, host, confighost, port, x_server, disable_shell_sourcing, env_exec):
    """Execute a tool on a remote computer using SSH."""
    check_binary("ssh-askpass")
    check_binary("setsid")

    if confighost and user:
        click.echo("Please set either a confighost OR a user-host combination")
        sys.exit(1)

    cmd = ["setsid", "ssh"]

    if user and host:
        address = f"{user}@{host}"
        cmd.append(address)
    elif confighost:
        cmd.append(confighost)
    if port:
        cmd += ["-p", port]
    if x_server:
        cmd.append("-X")
    if not disable_shell_sourcing:
        cmd.append(
            "for FILE in /etc/bash.bashrc /etc/profile $HOME/.bashrc $HOME/.profile; do"
            f" test -f $FILE && source $FILE; done; {env_exec[0]}"
        )
    else:
        cmd.append(env_exec[0])

    click.echo(cmd, err=True)
    sys.exit(subprocess.run(cmd).returncode)
