from ..Core.Pin import PinWidgetBase
from ..Core.AGraphCommon import *

from shotgun_api3 import Shotgun


class SgPin(PinWidgetBase):
    """doc string for SgPin"""
    def __init__(self, name, parent, dataType, direction, **kwargs):
        super(SgPin, self).__init__(name, parent, dataType, direction, **kwargs)
        self.setDefaultValue(None)

    def supportedDataTypes(self):
        return (DataTypes.Sg,)

    @staticmethod
    def color():
        return Colors.Yellow

    @staticmethod
    def pinDataTypeHint():
        return DataTypes.Sg, ''

    # ISerializable interface
    def serialize(self):
        data = super(SgPin, self).serialize()
        data["value"] = None
        return data

    def setData(self, data):
        try:
            if isinstance(data,Shotgun):
                self._data = data
            else:
                self._data =  self.defaultValue()
        except:
            self._data =  self.defaultValue()
        PinWidgetBase.setData(self, self._data)

