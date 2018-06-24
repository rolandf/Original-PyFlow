"""@package Pins
"""
from __future__ import absolute_import
import os
_PINS = {}
from ..Core.AGraphCommon import DataTypes
_suportedTypes = {}
def _REGISTER_PIN_TYPE(pinSubclass):
    '''
    registering pin
    '''
    dType = pinSubclass.pinDataTypeHint()[0]
    if dType not in _PINS:
        _PINS[pinSubclass.pinDataTypeHint()[0]] = pinSubclass
    else:
        raise Exception("Error registering pin type {0}\n pin with ID [{1}] already registered".format(pinSubclass.__name__))

def findPinClassByType(dataType):
        return _PINS[dataType] if dataType in _PINS else None

# append from Pins
for n in os.listdir(os.path.dirname(__file__)):
    if n.endswith(".py") and "__init__" not in n:
        pinName = n.split(".")[0]
        #try:
        exec("from .{0} import {0}".format(pinName))
        exec("pin_class = {0}".format(pinName))
        _REGISTER_PIN_TYPE(pin_class)





def getPinDefaultValueByType(dataType):
    pin = findPinClassByType(dataType)
    if pin:
        return pin.pinDataTypeHint()[1]
    return None


def CreatePin(name, parent, dataType, direction, **kwds):
    pinClass = findPinClassByType(dataType)
    if pinClass is None:
        return None
    inst = pinClass(name, parent, dataType, direction, **kwds)
    return inst
