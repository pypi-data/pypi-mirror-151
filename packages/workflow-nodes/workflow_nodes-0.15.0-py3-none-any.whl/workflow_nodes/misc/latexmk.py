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

from .main import misc


@misc.command()
@option("pdf", char="p", is_flag=True, description="Generate pdf by pdflatex.")
@option(
    "change_directory",
    char="c",
    description="Change to directory of source file when processing.",
)
def latexmk(pdf, change_directory):
    """Wrapper node for latexmk."""
    cmd = ["latexmk"]

    if pdf:
        cmd.append("-pdf")
    if change_directory:
        cmd += ["-cd", change_directory]

    sys.exit(subprocess.run(cmd).returncode)
