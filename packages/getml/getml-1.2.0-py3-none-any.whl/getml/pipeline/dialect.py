# Copyright 2021 The SQLNet Company GmbH

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

"""
SQL dialects that can be used for the generated code.

One way to productionize a :class:`~getml.Pipeline` is
to transpile its features to production-ready SQL code.
This SQL code can be run on standard cloud infrastructure.
Please also refer to :class:`~getml.pipeline.SQLCode`.

Example:
    .. code-block:: python

        sql_code = my_pipeline.features.to_sql(
            getml.pipeline.dialect.spark_sql)

        # Creates a folder called "my_pipeline"
        # which contains the SQL scripts.
        sql_code.save("my_pipeline")
"""

import re
from typing import Literal, Pattern, get_args

# --------------------------------------------------------------

AllDialects = Literal[
    "bigquery",
    "mysql",
    "postgres",
    "spark sql",
    "sqlite3",
    "tsql",
]

# --------------------------------------------------------------

bigquery = get_args(AllDialects)[0]
"""BigQuery is a proprietary database system used by the Google Cloud.
"""

mysql = get_args(AllDialects)[1]
"""MySQL and its fork MariaDB are among the most popular open-source
database systems.
"""

postgres = get_args(AllDialects)[2]
"""The PostgreSQL or postgres dialect is a popular SQL dialect
used by PostgreSQL and its many derivatives like Redshift
or Greenplum.
"""

spark_sql = get_args(AllDialects)[3]
"""Spark SQL is the SQL dialect used by Apache Spark.

Apache Spark is an open-source, distributed, in-memory
engine for large-scale data processing and a popular
choice for producutionizing machine learning pipelines.
"""

sqlite3 = get_args(AllDialects)[4]
"""The SQLite3 dialect is the default dialect used by getML.

It is recommended for live prediction systems or when the amount
of data handled is unlikely to be too large.
"""

tsql = get_args(AllDialects)[5]
"""TSQL or Transact-SQL is the dialect used by most Microsoft
databases.
"""


# --------------------------------------------------------------


def _drop_table(dialect: AllDialects, key: str) -> str:
    if dialect in (bigquery, mysql, spark_sql):
        return "DROP TABLE IF EXISTS `" + key.upper() + "`"

    if dialect in (postgres, sqlite3):
        return 'DROP TABLE IF EXISTS "' + key.upper() + '"'

    if dialect == tsql:
        return "DROP TABLE IF EXISTS \[" + key.upper() + "\]"

    raise ValueError(
        "Unknown dialect: '"
        + dialect
        + "'. Please choose one of the following: "
        + str(get_args(AllDialects))
    )


# --------------------------------------------------------------


def _table_pattern(dialect: AllDialects) -> Pattern:
    if dialect in (bigquery, mysql, spark_sql):
        return re.compile("CREATE TABLE `(.+)`")

    if dialect in (postgres, sqlite3):
        return re.compile('CREATE TABLE "(.+)"')

    if dialect == tsql:
        return re.compile("INTO \[(.+)\]")

    raise ValueError(
        "Unknown dialect: '"
        + dialect
        + "'. Please choose one of the following: "
        + str(get_args(AllDialects))
    )


# --------------------------------------------------------------
