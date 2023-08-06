"""
Copyright (C) University of Adelaide, Australia - All Rights Reserved
This source code is protected under proprietary reference only license.
Please refer to the accompanying LICENSE file for further information.
"""

from epics import PV
from numbers import Number
from numpy import *


class HS_PV(PV):
    """A class to interact with an EPICS process variable.

    ``HS_PV`` inherits the class ``PV`` of ``epics`` package (also called
    PyEpics), and implements type checking of the values before they are entered
    into an EPICS channel.

    All the methods of the class ``PV`` are hence available to ``HS_PV``, and a
    user is encouraged to consult PyEpics documentation for the full description
    of the package.

    Currently :func:`~HS_PV.check_type()` is the only method added to this class.
    The method :func:`~HS_PV.put()` is extended to incorporate the type checking
    done by :func:`~HS_PV.check_type()`.

    **Instantiation**

    The simplest way to instantiate the class is just provide ``record_name`` of
    a process variable. The created instance then acts just like ``PV`` class of
    ``pyepics``.

    If ``data_type`` is also given when instantiating, the instance method
    :func:`~HS_PV.put` checks if the value to be put is of the correct type using
    :func:`~HS_PV.check_type`.

    If the value is valid, then ``put`` method of ``PV`` class is called. If not,
    the put request is rejected with a warning message, and the value of the
    process variable stays as it was.

    The accepted names for the data types that can be checked and the meaning of
    each data type are implemented as *dict* ``data_type_verbose``:

    - ``boolean``: ``True`` or ``False``
    - ``pint``: positive *integer*
    - ``nnint``: non-negative *integer*
    - ``int``: *integer*
    - ``string``: *string*
    - ``pfloat``: positive real number
    - ``nnfloat``: non-negative real number
    - ``float``: any real number

    **Instance Variables**

    As this class inherits ``PV`` of ``pyepics``, there are many more instance
    variables that ``HS_PV``

    - ``data_type``: the data type of the process variable

      In order to check the data type, it must be one of the following:
      'boolean', 'pint', 'nnint', 'int', 'string', 'pfloat', 'nnfloat', or
      'float'.

      Setting ``data_type`` to something else won't raise an error but won't
      trigger data type checking.

      :Type: *string*
      :Required by: :func:`~HS_PV.put`, :func:`~HS_PV.check_type`

    - ``data_type_verbose``: *dict* of verbose descriptions of ``data_type`` values.

      This variable is used to produce an appropriate warning message when type
      checking yields ``False``.

      :Type: *dict*
      :Required by: :func:`~HS_PV.put`

    - ``type_checking``: *boolean* to indicate whether to check the data type or not

      :Type: *boolean*
      :Required by: :func:`~HS_PV.put`


    """

    def __init__(self, record_name, data_type=None):

        PV.__init__(self, record_name)

        self.default_value = None
        self.last_value = None
        self.data_type = data_type
        self.data_type_verbose = {}

        self.data_type_verbose["boolean"] = "boolean"
        self.data_type_verbose["pint"] = "positive integer"
        self.data_type_verbose["nnint"] = "non-negative integer"
        self.data_type_verbose["int"] = "integer"
        self.data_type_verbose["string"] = "string"
        self.data_type_verbose["pfloat"] = "positive real number"
        self.data_type_verbose["nnfloat"] = "non-negative real number"
        self.data_type_verbose["float"] = "real number"
        self.type_checking = False

        if (data_type is None) or (data_type == "waveform"):
            self.type_checking = False
        else:
            self.type_checking = True

    def put(
        self,
        value,
        wait=False,
        timeout=30.0,
        use_complete=False,
        callback=None,
        callback_data=None,
    ):
        """Check and enter a value into EPICS PV.

        See the PyEpics documentation for the ``pv.put`` method for the explanations
        of the input parameters other than ``value``.

        When the instance variable ``check_type`` is ``True``, this method calls


        :param value: the value of the process variable to be put into EPICS channel
        :Requires: ``type_checking``
        :Uses: (optional) :func:`~HS_PV.check_type`

        """

        if self.type_checking == True:
            if self.check_type(value):
                return PV.put(
                    self, value, wait, timeout, use_complete, callback, callback_data
                )
            else:
                print("**Warning** " + self.pvname)
                print(
                    "Not a valid data type: "
                    + "the record must be of the type "
                    + self.data_type_verbose[self.data_type]
                    + "."
                )
                print("The record value will not be changed.")
        else:
            return PV.put(
                self, value, wait, timeout, use_complete, callback, callback_data
            )
            self.last_value = value

    # def get(self,
    #         count=None,
    #         as_string=False,
    #         as_numpy=True,
    #         timeout=None,
    #         use_monitor=True):
    #     val = PV.get(self,count,as_string,as_numpy,timeout,use_monitor)

    #     if self.type_checking == True:
    #         if self.check_type(val):
    #             return val
    #         else:
    #             print ('**Warning** ' + self.pvname)
    #             print \
    #                 ('Not a valid data type: ' + \
    #                  'the record must be of the type ' + \
    #                  self.data_type_verbose[self.data_type] + '.')
    #             print('The record value will be reverted the last valid value.')

    def check_type(self, value):
        """Check if the value to be put is of correct data type

        :param value: the value to be checked
        :Returns: ``True`` or ``False``
        :rtype: *boolean*

        """

        if size(value) == 1:
            if self.data_type == "boolean":
                return (value == 0) or (value == 1)
            elif self.data_type == "pint":
                if isinstance(value, Number):
                    return (value == int(value)) and (value > 0)
                else:
                    return False
            elif self.data_type == "nnint":
                if isinstance(value, Number):
                    return (value == int(value)) and (value >= 0)
                else:
                    return False
            elif self.data_type == "int":
                return isinstance(value, Number) and (value == int(value))
            elif self.data_type == "pfloat":
                return isinstance(value, Number) and (value > 0)
            elif self.data_type == "nnfloat":
                return isinstance(value, Number) and (value >= 0)
            elif self.data_type == "float":
                return isinstance(value, Number) and not (isinstance(value, complex))
            elif self.data_type == "string":
                return isinstance(value, str)
        else:
            # TODO: revise to check waveform record as necessary. At the moment
            # the method returns False if the value is an array.

            return False
