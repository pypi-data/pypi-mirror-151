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
Creates a new BigQuery database connection.
"""

import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import getml.communication as comm
from getml import constants

from .connection import Connection


def connect_bigquery(
    database_id: str,
    project_id: str,
    google_application_credentials: Union[str, Path],
    time_formats: Optional[List[str]] = None,
    conn_id: str = "default",
):
    """
    Creates a new BigQuery database connection.

    Args:
        database_id (str):
            The ID of the database to connect to.

        project_id (str):
            The ID of the project to connect to.

        google_application_credentials (str or pathlib.Path):
            The path of the google application credentials.
            (Must be located on the machine hosting the getML engine).

        time_formats (List[str], optional):
            The list of formats tried when parsing time stamps.

            The formats are allowed to contain the following
            special characters:

            * %w - abbreviated weekday (Mon, Tue, ...)
            * %W - full weekday (Monday, Tuesday, ...)
            * %b - abbreviated month (Jan, Feb, ...)
            * %B - full month (January, February, ...)
            * %d - zero-padded day of month (01 .. 31)
            * %e - day of month (1 .. 31)
            * %f - space-padded day of month ( 1 .. 31)
            * %m - zero-padded month (01 .. 12)
            * %n - month (1 .. 12)
            * %o - space-padded month ( 1 .. 12)
            * %y - year without century (70)
            * %Y - year with century (1970)
            * %H - hour (00 .. 23)
            * %h - hour (00 .. 12)
            * %a - am/pm
            * %A - AM/PM
            * %M - minute (00 .. 59)
            * %S - second (00 .. 59)
            * %s - seconds and microseconds (equivalent to %S.%F)
            * %i - millisecond (000 .. 999)
            * %c - centisecond (0 .. 9)
            * %F - fractional seconds/microseconds (000000 - 999999)
            * %z - time zone differential in ISO 8601 format (Z or +NN.NN)
            * %Z - time zone differential in RFC format (GMT or +NNNN)
            * %% - percent sign

        conn_id (str, optional):
            The name to be used to reference the connection.
            If you do not pass anything, this will create a new default connection.

    """

    time_formats = time_formats or constants.TIME_FORMATS

    cmd: Dict[str, Any] = {}

    cmd["database_id_"] = database_id
    cmd["project_id_"] = project_id
    cmd["google_application_credentials_"] = os.path.abspath(
        str(google_application_credentials)
    )
    cmd["name_"] = ""
    cmd["type_"] = "Database.new"
    cmd["db_"] = "bigquery"

    cmd["time_formats_"] = time_formats
    cmd["conn_id_"] = conn_id

    sock = comm.send_and_get_socket(cmd)

    # The API expects a password, but in this case there is none
    comm.send_string(sock, "")

    msg = comm.recv_string(sock)

    if msg != "Success!":
        comm.engine_exception_handler(msg)

    return Connection(conn_id=conn_id)
