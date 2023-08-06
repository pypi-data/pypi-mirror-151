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

from xmlhelpy import option

from .main import system


@system.command()
@option("path", description="Path to be listed.", required=True)
@option("list", description="Show details of directory.", char="l", is_flag=True)
@option("all", description="Show all details.", char="a", is_flag=True)
def ls(path, list, all):
    """Wrapper node for ls."""
    cmd = ["ls", path]

    if list:
        cmd.append("-l")
    if all:
        cmd.append("-a")

    sys.exit(subprocess.run(cmd).returncode)
