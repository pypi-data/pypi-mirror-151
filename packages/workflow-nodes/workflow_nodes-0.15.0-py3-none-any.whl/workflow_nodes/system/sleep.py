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

from xmlhelpy import argument
from xmlhelpy import Integer

from .main import system


@system.command()
@argument(
    "number", param_type=Integer, description="The number of seconds to pause for."
)
def sleep(number):
    """Pause for a specific number of seconds."""
    cmd = ["sleep", str(number)]
    sys.exit(subprocess.run(cmd).returncode)
