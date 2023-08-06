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
@option(
    "one-dimensional-mesh",
    char="a",
    description="Perform 1D mesh generation.",
    is_flag=True,
)
@option(
    "two-dimensional-mesh",
    char="b",
    description="Perform 2D mesh generation.",
    is_flag=True,
)
@option(
    "three-dimensional-mesh",
    char="c",
    description="Perform 3D mesh generation.",
    is_flag=True,
)
@option("geo-file", char="g", description="Specify geo-file name.", required=True)
@option("file", char="o", description="Specify output file name.", required=True)
@option("set-number", char="n", description="Set constant or option number name=value")
@option("save-and-exit", char="s", description="Save mesh, then exit", is_flag=True)
@option("format", char="f", description="Select output mesh format")
def gmsh(
    one_dimensional_mesh,
    two_dimensional_mesh,
    three_dimensional_mesh,
    save_and_exit,
    file,
    set_number,
    format,
    geo_file,
):
    """Wrapper node for gmsh."""
    cmd = ["gmsh"]

    if one_dimensional_mesh:
        cmd.append("-1")
    if two_dimensional_mesh:
        cmd.append("-2")
    if three_dimensional_mesh:
        cmd.append("-3")
    if set_number:
        cmd.append("-setnumber")
        cmd += set_number.split(" ")
    if geo_file:
        cmd.append(geo_file)
    if save_and_exit:
        cmd.append("-save")
    if file:
        cmd += ["-o", file]
    if format:
        cmd += ["format", format]

    sys.exit(subprocess.run(cmd).returncode)
