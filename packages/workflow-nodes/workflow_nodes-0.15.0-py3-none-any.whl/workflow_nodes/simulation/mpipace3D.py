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
from xmlhelpy import Integer
from xmlhelpy import option

from .main import simulation


@simulation.command()
@option("specificsolver", char="s", description="Specify a certain mpipace3D solver")
@option(
    "numofprocessors",
    char="n",
    param_type=Integer,
    description="Set the number of processors",
    required=True,
)
@option(
    "infile",
    char="I",
    required=True,
    description="Required to specify the starting calues of the simulation embedded"
    " Infile",
)
@option(
    "pathname",
    char="P",
    required=True,
    description="This path specifies the working path where all simulation files will"
    " be written to",
)
@option(
    "force", char="f", description="Force to remove existing outfiles", is_flag=True
)
@option(
    "overwrite",
    char="o",
    description="Give a list of key=value pairs separated by '|' for overwriting or"
    " appending values in the infile. This feature is useful for simulation series.",
)
@option(
    "continuing",
    char="C",
    description="Continue a simulation starting with the last frame.",
    is_flag=True,
)
@option(
    "respawn",
    char="R",
    description="Specify a data set as a starting configuration for the simulation."
    " /path/to/simulation.p3simgeo represents the whole simulation data set to be used",
)
@option(
    "frame",
    char="F",
    description="Frame number to start the simulation for respawn. As a special value"
    " 'end' can be used for the last available frame of all data files.",
)
@option(
    "copy",
    char="c",
    description="Copy previous frames up to the respawn timestep into the outfiles, in"
    " case of a respawn.",
    is_flag=True,
)
@option(
    "append", char="a", is_flag=True, description="Append simulation to an existing one"
)
@option(
    "dopreconditioning",
    char="p",
    description="Preconditioning from infile should be used after respawn.",
    is_flag=True,
)
@option(
    "dofilling",
    char="d",
    description="Filling functions from infile should be used after loading the respawn"
    " data.",
    is_flag=True,
)
@option(
    "logfile",
    char="L",
    description="Specify a file to which the log output data is going to be written to,"
    " otherwise stdout/stderr is used.",
)
@option(
    "msgscript",
    char="M",
    description="Specify a script which will receive messages. This script should send"
    " the messages given as a parameter to the user.",
)
@option(
    "msglevel",
    char="m",
    description="How many messages should be send. 0: start/stop, 1: all",
    param_type=Integer,
)
@option(
    "info", char="i", description="Print program and system information.", is_flag=True
)
@option(
    "verbose",
    char="v",
    description="Enable the output (stderr) of some (helpful) log messages, a higher"
    " level will create more messages.",
    param_type=Integer,
)
@option("showhelp", char="h", description="print help", is_flag=True)
def mpipace3D(
    specificsolver,
    numofprocessors,
    infile,
    pathname,
    force,
    overwrite,
    continuing,
    respawn,
    frame,
    copy,
    append,
    dopreconditioning,
    dofilling,
    logfile,
    msgscript,
    msglevel,
    info,
    verbose,
    showhelp,
):
    """Start a simulation using multiple processors."""
    cmd = ["mpirun", "-np", str(numofprocessors)]

    if specificsolver:
        cmd.append(specificsolver)
    else:
        cmd.append("mpipace3D")

    cmd += ["-I", infile, "-P", pathname]

    if overwrite:
        cmd += ["-o", overwrite]
    if continuing:
        cmd.append("-C")
    if respawn:
        cmd += ["-R", respawn]
    if frame:
        cmd += ["-F", frame]
    if copy:
        cmd.append("-c")
    if append:
        cmd.append("-a")
    if dopreconditioning:
        cmd.append("-p")
    if dofilling:
        cmd.append("-d")
    if logfile:
        cmd += ["-L", logfile]
    if msgscript:
        cmd += ["-M", msgscript]
    if msglevel:
        cmd += ["-m", str(msglevel)]
    if info:
        cmd.append("-i")
    if verbose:
        cmd += ["-v", str(verbose)]
    if showhelp:
        cmd.append("-h")
    if force:
        cmd.append("-f")

    click.echo(" ".join(cmd), err=True)
    sys.exit(subprocess.run(cmd).returncode)
