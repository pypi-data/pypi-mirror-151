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
@argument("string1", description="string to be replaced")
@argument("string2", description="string to be inserted")
@option("path", char="p", required=True, description="Name of the file")
def sed(string1, string2, path):
    """Wrapper node for sed."""
    cmd = ["sed", "-i", f"s/{string1}/{string2}/g", path]

    click.echo(" ".join(cmd), err=True)
    sys.exit(subprocess.run(cmd).returncode)
