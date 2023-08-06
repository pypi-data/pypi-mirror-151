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
@option("script", char="s", description="Script to be used.", required=True)
@option("vtk-file", char="v", description="Vtk-file.", required=True)
@option("output-file", char="o", description="Resulting output file.")
def pvbatch(script, vtk_file, output_file):
    """Wrapper node for pvbatch."""
    cmd = ["pvbatch"]

    if script:
        cmd.append(script)
    if vtk_file:
        cmd.append(vtk_file)
    if output_file:
        cmd.append(output_file)

    sys.exit(subprocess.run(cmd).returncode)
