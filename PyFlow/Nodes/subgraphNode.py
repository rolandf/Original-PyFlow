from ..Core.AbstractGraph import *
from ..Core.Settings import *
from ..Core import Node

from Qt.QtWidgets import QMenu
from Qt.QtWidgets import QFileDialog
from Qt import QtWidgets

import os
import json



class subgraphNode(Node):
    def __init__(self, name, graph):
        from ..Core import Widget as Widget

        super(subgraphNode, self).__init__(name, graph)
        self.menu = QMenu()
        self.actionExport = self.menu.addAction('export')
        self.actionExport.triggered.connect(self.export)

        self._graph = Widget.GraphWidget("graph",self.graph().parent)
        self._graph.outPinCreated.connect(self.createOutput)
        self._graph.inPinCreated.connect(self.createInput)      
        self.dlg = MyDialog()
        self.dlg.setStyleSheet(self.graph().parent.styleSheetEditor.getStyleSheet())
        self.dlg.setLayout(QtWidgets.QHBoxLayout())
        self.dlg.layout().addWidget(self._graph)
        self._category = "CustomGraphs"
        self._keywords = "CustomGraphs"
        self._description = "Custom SubGraph"
        #self.bCallable = True
        self.dinOutputs = {}
        self.dinInputs = {}

    def createInput(self,pin):
        p = self.addInputPin(pin.name, DataTypes.Any,constraint="in%s"%pin.name)
        p.setType(pin)
        pin.nameChanged.connect(p.setName)
        pin.constraint = "in%s"%pin.name
        self._Constraints["in%s"%pin.name].append(pin)
        self._graph.inputsItem._Constraints["in%s"%pin.name]=[pin,p]
        pin.OnPinDeleted.connect(self.deletePort)
        pin.dataBeenSet.connect(p.setData)
        pinAffects(pin,p)
        #pinAffects(p,pin) 
        #p.dataBeenSet.connect(pin.setData)
        self.dinInputs[pin]=p    

        for i in self.inputs.values():
            for o in self.outputs.values():
                pinAffects(i, o)             
         
    def createOutput(self,pin):
        p = self.addOutputPin(pin.name, DataTypes.Any,constraint="out%s"%pin.name)
        p.setType(pin)
        pin.nameChanged.connect(p.setName)
        pin.constraint = "out%s"%pin.name
        self._Constraints["out%s"%pin.name].append(pin)
        self._graph.outputsItem._Constraints["out%s"%pin.name]=[pin,p]
        pin.OnPinDeleted.connect(self.deletePort)
        pin.dataBeenSet.connect(p.setData)
        #p.dataBeenSet.connect(pin.setData) 
        pinAffects(pin,p)   
        #pinAffects(p,pin)     
        self.dinOutputs[pin]=p
        for i in self.inputs.values():
            for o in self.outputs.values():
                pinAffects(i, o)
    def serialize(self):
        template =super(subgraphNode, self).serialize()
        graphData = self._graph.getGraphSaveData()
        template["graphData"] = graphData
        return template
    
    def export(self):
        from . import _nodeClasses
        from ..FunctionLibraries import _foos
        from ..SubGraphs import _subgraphClasses
        from .. import SubGraphs       
        existing_nodes = [n for n in _nodeClasses]
        existing_nodes += [n for n in _foos]
        existing_nodes += [n for n in _subgraphClasses]
        
        graphData = self._graph.getGraphSaveData()
        graphData["Type"]="subgraph"
        graphData["category"]=self._category
        graphData["keywords"]=self._keywords
        graphData["description"]=self._description
        name_filter = "Graph files (*.pySubgraph)"

        pth = QFileDialog.getSaveFileName(filter=name_filter)
        if not pth == '':
            file_path = pth
            path,name = os.path.split(file_path)
            name,ext = os.path.splitext(name)
            if name in existing_nodes:
                print("[ERROR] Node {0} already exists! Chose another name".format(name))
                return
            # write to file. delete older if needed
            with open(file_path, "wb") as f:
                def to_serializable(val):
                    return {
                        "name": None
                    }
                    return str(val)                
                json.dump(graphData, f,skipkeys=True,default=to_serializable,indent=2)            
            reload(SubGraphs)
            SubGraphs._getClasses()        
    def contextMenuEvent(self, event):
        self.menu.exec_(event.screenPos())

    def postCreate(self, jsonTemplate):
        
        if "graphData" in jsonTemplate:
            self._graph.loadFromData(jsonTemplate["graphData"])
        # restore pins
        for inp in self._graph.inputsItem.outputs.values():
            self.createInput(inp)
        for out in self._graph.outputsItem.inputs.values():
            self.createOutput(out)
        super(subgraphNode, self).postCreate( jsonTemplate)

    def deletePort(self,pin):
        if pin in self.dinInputs:
            self.dinInputs[pin].kill()
            del self.dinInputs[pin]
        elif pin in self.dinOutputs:
            self.dinOutputs[pin].kill()
            del self.dinOutputs[pin]

    @staticmethod
    def pinTypeHints():
        '''
            used by nodebox to suggest supported pins
            when drop wire from pin into empty space
        '''
        return {'inputs': [], 'outputs': []}

    @staticmethod
    def category():
        return 'Common'

    @staticmethod
    def keywords():
        return []

    @staticmethod
    def description():
        '''
            used by property view and node box widgets
        '''
        return 'Encapsulate a graph inside a node'

    def mouseDoubleClickEvent(self, event):
        #Node.mouseDoubleClickEvent( event)
        self.OnDoubleClick(self.mapToScene(event.pos()))
        event.accept()

    def OnDoubleClick(self,pos):
        self.dlg.show()

    def compute(self):
        for key, value in self.dinInputs.iteritems():
            key.setData(value.getData())
        for key, value in self.dinOutputs.iteritems():
            value.setData(key.getData())

class MyDialog(QtWidgets.QDialog):
    # ...
    def __init__(self, parent=None):
        super(MyDialog, self).__init__(parent)

        # when you want to destroy the dialog set this to True
        self._want_to_close = False

    def closeEvent(self, evnt):
        if self._want_to_close:
            super(MyDialog, self).closeEvent(evnt)
        else:
            evnt.ignore()
            self.hide()