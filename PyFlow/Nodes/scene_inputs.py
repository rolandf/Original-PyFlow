from ..Core.AbstractGraph import *
from ..Core.Settings import *
from ..Core import Node
from Qt.QtWidgets import QMenu,QGraphicsItem
from ..Core.Pin import PinWidgetBase
from ..Core.NodePainter import NodePainter
from Qt import QtCore
supportedDataTypesList = tuple([x for x in DataTypes])

class sender(QtCore.QObject):
    pinCreated = QtCore.Signal(object)   

class scene_inputs(Node):
    def __init__(self, name, graph):
        super(scene_inputs, self).__init__(name, graph)
        self.menu = QMenu()
        self.action = self.menu.addAction('add port')
        self.action.triggered.connect(self.addInPin)
        self.setPos(self.graph().mapToScene(self.graph().viewport().rect().x(),self.graph().viewport().rect().y()+50) )
        self.asGraphSides = True
        self.sizes[4] = 0
        self.sizes[5] = 0

        self.setFlag(QGraphicsItem.ItemIsMovable,False)
        self.setFlag(QGraphicsItem.ItemIsFocusable,False)
        self.setFlag(QGraphicsItem.ItemIsSelectable,False)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges,False)
        
        #self.setFlag(QGraphicsItem.ItemIgnoresTransformations)
        self.label().hide() 
        self.sender = sender()    
    def addInPin(self):
        const = len(self.outputs)+1
        p = self.addOutputPin("input_%i"%const, DataTypes.Any,editable=True)
        #p.dynamic = True
        p.setDeletable()
        self.sender.pinCreated.emit(p)

    def contextMenuEvent(self, event):
        self.menu.exec_(event.screenPos())

    @staticmethod
    def pinTypeHints():
        return {'inputs': [], 'outputs': [supportedDataTypesList]}

    @staticmethod
    def category():
        return '__hiden__'

    @staticmethod
    def keywords():
        return []

    @staticmethod
    def description():
        return 'Genertic array'

    def postCreate(self, jsonTemplate):
        Node.postCreate(self, jsonTemplate)

        # restore dynamically created inputs
        for inp in jsonTemplate['outputs']:
            PinWidgetBase.deserialize(self, inp)
            #pinAffects(p, self.out0)
    def boundingRect(self):
        rect = self.childrenBoundingRect()
        rect.setHeight(self.graph().boundingRect.height())
        self.setPos(self.graph().boundingRect.topLeft().x(),self.graph().boundingRect.topLeft().y()+50)
        #rect.setWidth(self.graph().boundingRect.width()/30)
        return rect         
    def paint(self, painter, option, widget):

        NodePainter.asGraphSides(self, painter, option, widget)
        #self.setPos(self.graph().mapToScene(self.graph().viewport().rect().x(),self.graph().viewport().rect().y()+50) )
        
    #def compute(self):
    #    self.out0.setData(list([i.getData() for i in self.inputs.values()]))
