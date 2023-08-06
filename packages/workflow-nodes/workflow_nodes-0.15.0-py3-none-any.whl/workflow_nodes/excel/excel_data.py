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
import sys
from pathlib import Path

import click
from xmlhelpy import Integer
from xmlhelpy import option

from .main import excel
from .utils import convert_number


def _write_csv(path, data):
    with Path(path).expanduser().open(mode="a", encoding="utf-8") as result_file:
        writer = csv.writer(
            result_file, delimiter=";", quotechar='"', quoting=csv.QUOTE_NONNUMERIC
        )

        for row in data:
            writer.writerow(row)


@excel.command()
@option(
    "file",
    char="f",
    description="File with values, will be read line by line",
)
@option(
    "single-value",
    char="s",
    description="Single value. Can not be used together with --file|-f",
)
@option("row", char="r", description="Row number", required=True, param_type=Integer)
@option("column", char="c", description="Column name (alphabetical)", required=True)
@option("outfile", char="o", description="Output", default=".excel-values.csv")
def excel_data(file, single_value, row, column, outfile):
    """Prepares data to be added to an Excel document.

    Appends data to a CSV file containing values with target cells.
    """
    data = []

    if not (file or single_value):
        click.echo("Error: No input value or file given.")
        sys.exit(1)

    if file:
        with Path(file).expanduser().open(encoding="utf-8") as f:
            for line in f:
                key = f"{column}{row}"
                value = line.strip("")
                value = convert_number(value)
                data.append([key, value])
                row += 1
    elif single_value:
        key = f"{column}{row}"
        value = convert_number(single_value)
        data.append([key, value])

    _write_csv(outfile, data)
    click.echo(f"Excel data written to {outfile}.")
