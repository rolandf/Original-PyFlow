from ..Core.Pin import PinWidgetBase
from ..Core.AGraphCommon import *

class AnyPin(PinWidgetBase):
    """doc string for SgPin"""
    def __init__(self, name, parent, dataType, direction, **kwargs):
        super(AnyPin, self).__init__(name, parent, dataType, direction, **kwargs)
        self.setDefaultValue(None)
        self.supportedDataTypesList = tuple([x for x in DataTypes])
        self.origDataType = DataTypes.Any
    def supportedDataTypes(self):
        return self.supportedDataTypesList

    @staticmethod
    def defcolor():
        return Colors.White
    @staticmethod
    def color():
        return Colors.White
    @staticmethod
    def pinDataTypeHint():
        return DataTypes.Any, ''

    def setData(self, data):
        try:
            self._data = data
        except:
            self._data =  self.defaultValue()
        PinWidgetBase.setData(self, self._data)

    def pinConnected(self, other):
        self.updateOnConnection(other)
        PinWidgetBase.pinConnected(self, other)
        self.OnPinConnected.emit(other)

    def pinDisconnected(self, other):
        self.updateOnDisconnection()
        PinWidgetBase.pinDisconnected(self, other)
        self.OnPinConnected.emit(other)         
        

    def updateOnConnection(self,other):
        if self.constraint == None:
            self.setType(other)
        else:
            free = True
            for port in self.parent()._Constraints[self.constraint]:
                if port.hasConnections() and port.dataType != DataTypes.Any:
                    free = False
                    break
            checked = []
            free = self.checkFree(checked)
            if free:
                self.setType(other)               
            for port in self.parent()._Constraints[self.constraint]:
                if port.dataType == DataTypes.Any:
                    self.setSelfType(port)
                    for e in port.edge_list:
                        for p in [e.source(),e.destination()]:
                            if p.dataType == DataTypes.Any and p.dataType != self.dataType:
                                self.setSelfType(p) 
                                p.updateOnConnection(self)       
    def updateOnDisconnection(self):
        if self.constraint == None:
            self.setDefault()
        else:
            checked = []
            free = self.checkFree(checked)
            if free:
                self.setDefault()
                for port in self.parent()._Constraints[self.constraint]:
                    if port != self and port.dataType != DataTypes.Any:                        
                        self.setSelfType(port)  
                        if isinstance(port,AnyPin):
                            port.updateOnDisconnection()  
                        for e in port.edge_list:
                            for p in [e.source(),e.destination()]:
                                if p.dataType != DataTypes.Any:
                                    self.setSelfType(p)
                                    try:
                                        p.updateOnDisconnection() 
                                    except:
                                        continue
            

    def checkFree(self,checked=[],selfChek=True):
        if self.constraint == None or self.dataType == DataTypes.Any:
            return True
        else:
            con  = []
            if selfChek:
                free = not self.hasConnections()
                
                if not free:
                    for edge in self.edge_list:
                        for c in [edge.source(),edge.destination()]:
                            if c not in checked:
                                con.append(c)
            else:
                free = True
                checked.append(self)

            for port in self.parent()._Constraints[self.constraint]+con:
                if port not in checked:
                    checked.append(port)
                    if not isinstance(port,AnyPin):
                        return False
                    else:
                        free = port.checkFree(checked)
                        
            return free


    def call(self):
        super(AnyPin, self).call()
        # pass execution flow forward
        for p in [pin for pin in self.affects if pin.dataType == DataTypes.Exec]:
            p.call()
        # highlight wire
        for e in self.edge_list:
            e.highlight()
            
    def setSelfType(self,port):
        port.dataType = self.dataType 
        port.color = self.color
        port.setDefaultValue(self.defaultValue())
        port.setData(self.defaultValue()) 
        for e in port.edge_list:
            e.setColor( self.color())        
        port.update()         
    def setDefault(self):
        self.dataType = DataTypes.Any
        self.color = self.defcolor
        self.setDefaultValue(None)
        self.setData(None)
        self.update()
    def setType(self,other):
        self.dataType = other.dataType
        self.color = other.color
        self.setData(other.defaultValue())
        self.setDefaultValue(other.defaultValue()) 
        for e in self.edge_list:
            e.setColor( self.color())          
        self.update()     