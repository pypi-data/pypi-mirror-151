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
import csv
from pathlib import Path

import click
import openpyxl
from xmlhelpy import option

from .main import excel
from .utils import convert_number


@excel.command()
@option(
    "file", char="f", description="The path to the document to modify", required=True
)
@option(
    "datafile",
    char="d",
    description="Datafile (csv) with row/column numbers and value to insert",
    default=".excel-values.csv",
)
@option(
    "outputfile",
    char="o",
    description="The path to the output file, if not specified overwrite [file]",
)
def excel_add_data(file, datafile, outputfile):
    """Adds data to an existing excel document."""
    in_file = str(Path(file).expanduser().absolute())
    wb = openpyxl.load_workbook(in_file)
    sheet = wb.active
    output_file_path = file if outputfile is None else outputfile
    output_file = str(Path(output_file_path).expanduser().absolute())
    click.echo("sheet opened")

    if datafile:
        with Path(datafile).expanduser().open(encoding="utf-8") as f:
            reader = csv.reader(f, delimiter=";")
            values_inserted = 0
            for (i, line) in enumerate(reader):
                key = line[0]
                value = convert_number(line[1])
                sheet[key] = value
                values_inserted = i
            click.echo(f"\t{values_inserted} values inserted from {datafile}")

    wb.save(output_file)
    click.echo(f"written to {output_file}")
