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

from xmlhelpy import argument
from xmlhelpy import option

from .main import misc
from workflow_nodes.utils import check_binary


@misc.command()
@argument("file", description="XML file")
@option("schema", description="do validation against the WXS schema")
@option("xpath", description="evaluate the XPath expression, imply --noout")
@option("noout", description="don't output the result tree", is_flag=True)
def xmllint(file, schema, xpath, noout):
    """Wrapper node for xmllint."""
    check_binary("xmllint")

    cmd = ["xmllint"]
    if schema:
        cmd += ["--schema", schema]
    if xpath:
        cmd += ["--xpath", xpath]
    if noout:
        cmd.append("--noout")
    if file:
        cmd.append(file)

    sys.exit(subprocess.run(cmd).returncode)
