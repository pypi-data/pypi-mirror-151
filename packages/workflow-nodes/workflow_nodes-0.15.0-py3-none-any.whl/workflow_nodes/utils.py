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
import shutil
import sys

import click


def check_binary(binary, message="Please make sure it is installed."):
    """Check if a binary is available in the PATH and exit with exit code 1 otherwise.

    :param binary: The binary to check.
    :param message: (optional) A message to specify further details to install the
        missing binary.
    """
    if not shutil.which(binary):
        click.echo(f"'{binary}' not found in PATH. {message}")
        sys.exit(1)


def missing_extra(extra):
    """Alert the user of a missing extra dependency and exit with exit code 1.

    :param extra: The extra dependency that is missing.
    """
    click.echo(
        "Missing one or more required dependencies. Please install them using the"
        f" '{extra}' extra dependency via 'pip3 install workflow-nodes[{extra}]'."
    )
    sys.exit(1)
