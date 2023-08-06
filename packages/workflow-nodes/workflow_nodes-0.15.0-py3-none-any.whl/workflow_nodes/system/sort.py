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
@argument("file", description="file to sort")
@option("field-separator", char="t", description="separator of fields")
@option(
    "numeric-sort",
    char="n",
    description="compare according to string numerical value",
    is_flag=True,
)
@option("key", char="k", description="sort via a key")
def sort(file, field_separator, numeric_sort, key):
    """Wrapper node for sort."""
    cmd = ["sort"]

    if numeric_sort:
        cmd.append("-n")
    if field_separator is not None:
        cmd += ["-t", field_separator]
    if key is not None:
        cmd += ["-k", key]

    cmd.append(file)

    click.echo(" ".join(cmd), err=True)
    sys.exit(subprocess.run(cmd).returncode)
