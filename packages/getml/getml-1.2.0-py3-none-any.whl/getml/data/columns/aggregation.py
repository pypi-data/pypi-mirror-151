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
Lazily evaluated aggregation over a column.
"""

from typing import Any, Dict

import getml.communication as comm


class Aggregation:
    """
    Lazily evaluated aggregation over a column.

    Example:

    .. code-block:: python

        >>> my_data_frame["my_column"].avg()
        3.0
    """

    def __init__(self, alias, col, agg_type):
        self.cmd: Dict[str, Any] = {}
        self.cmd["as_"] = alias
        self.cmd["col_"] = col.cmd
        self.cmd["type_"] = agg_type

    # -----------------------------------------------------------------------------

    def __repr__(self):
        return str(self)

    # -----------------------------------------------------------------------------

    def __str__(self):
        val = self.get()
        return self.cmd["type_"].upper() + " aggregation, value: " + str(val) + "."

    # --------------------------------------------------------------------------

    def get(self):
        """
        Receives the value of the aggregation over the column.
        """

        # -------------------------------------------

        cmd: Dict[str, Any] = {}

        cmd["name_"] = ""
        cmd["type_"] = "FloatColumn.aggregate"

        cmd["aggregation_"] = self.cmd

        # -------------------------------------------

        sock = comm.send_and_get_socket(cmd)

        msg = comm.recv_string(sock)

        # -------------------------------------------

        if msg != "Success!":
            sock.close()
            comm.engine_exception_handler(msg)

        mat = comm.recv_float_matrix(sock)

        # -------------------------------------------

        sock.close()

        # -------------------------------------------

        return mat.ravel()[0]
