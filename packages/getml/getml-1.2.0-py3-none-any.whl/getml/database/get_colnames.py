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
Lists the colnames of a table held in the database.
"""

import json
from typing import Any, Dict, Optional

import getml.communication as comm

from .connection import Connection


def get_colnames(name: str, conn: Optional[Connection] = None):
    """
    Lists the colnames of a table held in the database.

    Args:
        name (str):
            The name of the table in the database.

        conn (:class:`~getml.database.Connection`, optional):
            The database connection to be used.
            If you don't explicitly pass a connection,
            the engine will use the default connection.
    """
    # -------------------------------------------

    conn = conn or Connection()

    # -------------------------------------------

    cmd: Dict[str, Any] = {}

    cmd["name_"] = name
    cmd["type_"] = "Database.get_colnames"
    cmd["conn_id_"] = conn.conn_id

    # -------------------------------------------

    sock = comm.send_and_get_socket(cmd)

    # -------------------------------------------

    msg = comm.recv_string(sock)

    if msg != "Success!":
        sock.close()
        comm.engine_exception_handler(msg)

    # -------------------------------------------

    arr = json.loads(comm.recv_string(sock))

    sock.close()

    return arr
