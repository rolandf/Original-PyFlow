from ..Core.AbstractGraph import *
from ..Core.Settings import *
from ..Core import Node
from Qt.QtWidgets import QMenu
from ..Core.Pin import PinWidgetBase

supportedDataTypesList = tuple([x for x in DataTypes])
class makeArray(Node):
    def __init__(self, name, graph):
        super(makeArray, self).__init__(name, graph)
        self.out0 = self.addOutputPin('Array', DataTypes.Array)
        self.menu = QMenu()
        self.action = self.menu.addAction('add input')
        self.action.triggered.connect(self.addInPin)

    def addInPin(self):
        if len(self.inputs)== 0 :
            p = self.addInputPin(str(len(self.inputs)), DataTypes.Any,constraint="1")
        else:
            p = self.addInputPin(str(len(self.inputs)), DataTypes.Any,constraint="1")
            p.setType(self.inputs.items()[0][1])
        p.setDeletable()
        pinAffects(p, self.out0)


    def contextMenuEvent(self, event):
        self.menu.exec_(event.screenPos())

    @staticmethod
    def pinTypeHints():
        return {'inputs': supportedDataTypesList, 'outputs': [DataTypes.Array]}

    @staticmethod
    def category():
        return 'GenericTypes'

    @staticmethod
    def keywords():
        return []

    @staticmethod
    def description():
        return 'Genertic array'

    def postCreate(self, jsonTemplate):
        Node.postCreate(self, jsonTemplate)

        # restore dynamically created inputs
        for inp in jsonTemplate['inputs']:
            p = PinWidgetBase.deserialize(self, inp)
            pinAffects(p, self.out0)

    def compute(self):
        self.out0.setData(list([i.getData() for i in self.inputs.values()]))
