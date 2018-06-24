from ..Core.AbstractGraph import *
from ..Core.Settings import *
from ..Core import Node
from Qt import QtGui
from Qt.QtWidgets import QPushButton
from Qt.QtWidgets import QGraphicsProxyWidget
from Qt.QtWidgets import QFileDialog
from Qt.QtWidgets import QMenu
from ..Core.CodeEditor import WCodeEditor
import weakref
import uuid
from types import MethodType
from collections import OrderedDict
import inspect
import os
from os import listdir, path, startfile



class pythonNode(Node, NodeBase):
    def __init__(self, name, graph):
        super(pythonNode, self).__init__(name, graph)
        self.menu = QMenu()
        self.actionEdit = self.menu.addAction('edit')
        self.actionEdit.triggered.connect(self.openEditor)
        self.actionEdit.setIcon(QtGui.QIcon(':/icons/resources/py.png'))
        self.actionExport = self.menu.addAction('export')
        self.actionExport.triggered.connect(self.export)
        self.editorUUID = None
        self.bKillEditor = True
        self.label().icon = QtGui.QImage(':/icons/resources/py.png')
        self.currentComputeCode = Node.jsonTemplate()['computeCode']
        self.color = Colors.NodeNameRect

    @staticmethod
    def pinTypeHints():
        return {'inputs': [], 'outputs': []}

    def computeCode(self):
        return self.currentComputeCode

    def openEditor(self):
        self.editorUUID = uuid.uuid4()
        self.graph().codeEditors[self.editorUUID] = WCodeEditor(self.graph(), self, self.editorUUID)
        self.graph().codeEditors[self.editorUUID].show()

    def kill(self):
        if self.editorUUID in self.graph().codeEditors:
            ed = self.graph().codeEditors.pop(self.editorUUID)
            ed.deleteLater()
        Node.kill(self)

    @staticmethod
    def category():
        return 'Utils'

    def postCreate(self, jsonTemplate):
        # restore compute
        self.currentComputeCode = jsonTemplate['computeCode']
        foo = WCodeEditor.wrapCodeToFunction('compute', jsonTemplate['computeCode'])
        exec(foo)
        self.compute = MethodType(compute, self, Node)

        # restore pins
        for inpJson in jsonTemplate['inputs']:
            pin = None
            if inpJson['dataType'] == DataTypes.Exec:
                pin = self.addInputPin(inpJson['name'], inpJson['dataType'], self.compute, inpJson['bLabelHidden'])
                pin.uid = uuid.UUID(inpJson['uuid'])
            else:
                pin = self.addInputPin(inpJson['name'], inpJson['dataType'], None, inpJson['bLabelHidden'])
                pin.uid = uuid.UUID(inpJson['uuid'])
            pin.setData(inpJson['value'])
        for outJson in jsonTemplate['outputs']:
            pin = self.addOutputPin(outJson['name'], outJson['dataType'], None, outJson['bLabelHidden'])
            pin.uid = uuid.UUID(outJson['uuid'])
            pin.setData(outJson['value'])

        self.bCallable = self.isCallable()

        Node.postCreate(self, jsonTemplate)

        # restore node label
        self.label().setPlainText(jsonTemplate['meta']['label'])

    def wrapCodeToFunction(self,fooName, code):
        foo = "def {}(self):".format(fooName)
        lines = [i for i in code.split('\n') if len(i) > 0]
        for line in lines:
            foo += '\n\t\t{}'.format(line)
        return foo
    def export(self):
        # restore compute
        #print self.currentComputeCode
        foo = self.wrapCodeToFunction('compute', self.currentComputeCode)

        inputs = []
        portString = ""
        for obj in self.inputs.values():
            if obj.dataType == DataTypes.Exec:
                comp = "self.compute"
            else:
                comp = "None"
            portString += """\n        self.{0} = self.addInputPin("{0}", {1},{2},hideLabel={3})""".format(obj.name,str(obj.dataType),comp,obj.bLabelHidden)

        for obj in self.outputs.values():
            comp = "None"
            portString += """\n        self.{0} = self.addOutputPin("{0}", {1},hideLabel={2})""".format(obj.name,str(obj.dataType),obj.bLabelHidden)

        self._implementPlugin(self.name,portString,foo)        

    def contextMenuEvent(self, event):
        self.menu.exec_(event.screenPos())

    @staticmethod
    def keywords():
        return ['Code', 'Expression']

    @staticmethod
    def description():
        return 'default description'

    def _implementPlugin(self,name, ports,computeCode):
        from . import _nodeClasses
        from ..FunctionLibraries import _foos
        from ..SubGraphs import _subgraphClasses
        from .. import SubGraphs       
        existing_nodes = [n for n in _nodeClasses]
        existing_nodes += [n for n in _foos]
        existing_nodes += [n for n in _subgraphClasses]
        from .. import Nodes
        #file_path = "{0}/{1}.py".format(os.path.dirname(__file__), name)
        #existing_nodes = [n.split(".")[0] for n in os.listdir(os.path.dirname(__file__)) if n.endswith(".py") and "__init__" not in n]
        name_filter = "Node Files (*.py)"
        pth = QFileDialog.getSaveFileName(filter=name_filter)
        if not pth == '':
            file_path = pth
            path,name = os.path.split(file_path)
            name,ext = os.path.splitext(name)
            if name in existing_nodes:
                print("[ERROR] Node {0} already exists! Chose another name".format(name))
                return

            NodeTemplate = """from ..Core.AbstractGraph import *
from ..Core.Settings import *
from ..Core import Node

class {0}(Node):
    def __init__(self, name, graph):
        super({0}, self).__init__(name, graph){1}

        for i in self.inputs.values():
            for o in self.outputs.values():
                pinAffects(i, o)        
    @staticmethod
    def pinTypeHints():
        '''
            used by nodebox to suggest supported pins
            when drop wire from pin into empty space
        '''
        return {{'inputs': [DataTypes.Bool], 'outputs': [DataTypes.Bool]}}

    @staticmethod
    def category():
        '''
            used by nodebox to place in tree
            to make nested one - use '|' like this ( 'CatName|SubCatName' )
        '''
        return 'Common'

    @staticmethod
    def keywords():
        '''
            used by nodebox filter while typing
        '''
        return []

    @staticmethod
    def description():
        '''
            used by property view and node box widgets
        '''
        return 'default description'
    {2}    
""".format(name,ports,computeCode)


            # write to file. delete older if needed
            with open(file_path, "wb") as f:
                f.write(NodeTemplate)
            print("[INFO] Node {0} been created.\nIn order to appear in node box, restart application.".format(name))
            startfile(file_path)
            reload(Nodes)
            Nodes._getClasses()        
            