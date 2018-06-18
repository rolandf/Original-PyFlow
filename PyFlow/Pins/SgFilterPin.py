from ..Core.Pin import PinWidgetBase
from ..Core.AGraphCommon import *

import sys 
sys.path.append(r"C:\Users\pedro\OneDrive\pcTools_v5\pcSequenceExplorer\modules")
from shotgun_api3 import Shotgun

from ..FunctionLibraries import ShotGunLib

class SgFilterPin(PinWidgetBase):
    """doc string for SgPin"""
    def __init__(self, name, parent, dataType, direction, **kwargs):
        super(SgFilterPin, self).__init__(name, parent, dataType, direction, **kwargs)
        self.setDefaultValue(None)

    def supportedDataTypes(self):
        return (DataTypes.SgFilter,)

    @staticmethod
    def color():
        return Colors.DarkYellow

    @staticmethod
    def pinDataTypeHint():
        return DataTypes.SgFilter, ''

    def setData(self, data):
        try:
            if isinstance(data,ShotGunLib.sgFilters):
                self._data = data
            else:
                self._data =  self.defaultValue()
        except:
            self._data =  self.defaultValue()
        PinWidgetBase.setData(self, self._data)
