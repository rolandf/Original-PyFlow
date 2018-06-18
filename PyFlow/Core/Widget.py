from Qt import QtCore
from Qt import QtGui

from Qt.QtGui import QMouseEvent
from Qt.QtWidgets import QGraphicsScene
from Qt.QtWidgets import QAbstractItemView
from Qt.QtWidgets import QGraphicsProxyWidget
from Qt.QtWidgets import QGraphicsWidget
from Qt.QtWidgets import QFileDialog
from Qt.QtWidgets import QListWidget
from Qt.QtWidgets import QFrame
from Qt.QtWidgets import QLineEdit
from Qt.QtWidgets import QStyle
from Qt.QtWidgets import QScrollArea
from Qt.QtWidgets import QRubberBand
from Qt.QtWidgets import QMenu
from Qt.QtWidgets import QSizePolicy
from Qt.QtWidgets import QAction
from Qt.QtWidgets import QTreeWidget, QTreeWidgetItem
from Qt.QtWidgets import QWidget
from Qt.QtWidgets import QLabel
from Qt.QtWidgets import QMainWindow
from Qt.QtWidgets import QVBoxLayout
from Qt.QtWidgets import QGraphicsItem
from Qt.QtWidgets import QGraphicsRectItem
from Qt.QtWidgets import QGraphicsTextItem
from Qt.QtWidgets import QGraphicsPathItem
from Qt.QtWidgets import QGraphicsView
from Qt.QtWidgets import QApplication
from Qt.QtWidgets import QInputDialog
from Qt.QtWidgets import QUndoStack
import math
import platform
import random
from Settings import Colors
from AbstractGraph import *
from Edge import Edge
from Node import Node
from Node import NodeName
from GetVarNode import GetVarNode
from SetVarNode import SetVarNode
from SelectionRect import SelectionRect

from .. import Commands
from .. import FunctionLibraries
from .. import Nodes
from .. import Pins
from os import listdir, path
from .Variable import VariableBase
from time import ctime
import json
import re
import ast

def clearLayout(layout):
    while layout.count():
        child = layout.takeAt(0)
        if child.widget() is not None:
            child.widget().deleteLater()
        elif child.layout() is not None:
            clearLayout(child.layout())


def importByName(module, name):

    if hasattr(module, name):
        try:
            mod = getattr(module, name)
            return mod
        except Exception as e:
            print(e)
            return
    else:
        print("error", name)


def getNodeInstance(module, class_name, nodeName, graph):
    # Check in Nodes module first
    mod = Nodes.getNode(class_name)
    if mod is not None:
        instance = mod(nodeName, graph)
        return instance

    # if not found - continue searching in FunctionLibraries
    foo = FunctionLibraries.findFunctionByName(class_name)
    if foo:
        instance = Node.initializeFromFunction(foo, graph)
        return instance
    return None


class AutoPanController(object):
    def __init__(self, amount=10.0):
        super(AutoPanController, self).__init__()
        self.bAllow = False
        self.amount = amount
        self.autoPanDelta = QtGui.QVector2D(0.0, 0.0)
        self.beenOutside = False

    def Tick(self, rect, pos):
        if self.bAllow:
            if pos.x() < 0:
                self.autoPanDelta = QtGui.QVector2D(-self.amount, 0.0)
                self.beenOutside = True
                self.amount = clamp(abs(pos.x()) * 0.3, 0.0, 25.0)
            if pos.x() > rect.width():
                self.autoPanDelta = QtGui.QVector2D(self.amount, 0.0)
                self.beenOutside = True
                self.amount = clamp(abs(rect.width() - pos.x()) * 0.3, 0.0, 25.0)
            if pos.y() < 0:
                self.autoPanDelta = QtGui.QVector2D(0.0, -self.amount)
                self.beenOutside = True
                self.amount = clamp(abs(pos.y()) * 0.3, 0.0, 25.0)
            if pos.y() > rect.height():
                self.autoPanDelta = QtGui.QVector2D(0.0, self.amount)
                self.beenOutside = True
                self.amount = clamp(abs(rect.height() - pos.y()) * 0.3, 0.0, 25.0)
            if self.beenOutside and rect.contains(pos):
                self.reset()

    def getAmount(self):
        return self.amount

    def getDelta(self):
        return self.autoPanDelta

    def setAmount(self, amount):
        self.amount = amount

    def start(self):
        self.bAllow = True

    def isActive(self):
        return self.bAllow

    def stop(self):
        self.bAllow = False
        self.reset()

    def reset(self):
        self.beenOutside = False
        self.autoPanDelta = QtGui.QVector2D(0.0, 0.0)


class SceneClass(QGraphicsScene):
    def __init__(self, parent):
        super(SceneClass, self).__init__(parent)
        self.setItemIndexMethod(self.NoIndex)
        # self.pressed_port = None
        self.selectionChanged.connect(self.OnSelectionChanged)

    def shoutDown(self):
        self.selectionChanged.disconnect()

    def mousePressEvent(self, event):
        # do not clear selection when panning
        modifiers = event.modifiers()
        if event.button() == QtCore.Qt.RightButton:# or modifiers == QtCore.Qt.ShiftModifier:
            event.accept()
            return
        QGraphicsScene.mousePressEvent(self, event)

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat('text/plain'):
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat('text/plain'):
            event.setDropAction(QtCore.Qt.MoveAction)
            event.accept()
        else:
            event.ignore()

    def OnSelectionChanged(self):
        # selectedNodesUids = self.parent().selectedNodes()
        # cmdSelect = Commands.Select(selectedNodesUids, self.parent())
        # self.parent().undoStack.push(cmdSelect)
        pass

    def dropEvent(self, event):
        if event.mimeData().hasFormat('text/plain'):
            tag, mimeText = event.mimeData().text().split('|')
            name = self.parent().getUniqNodeName(mimeText)
            dropItem = self.itemAt(event.scenePos(), QtGui.QTransform())
            if not dropItem or isinstance(dropItem, Nodes.commentNode.commentNode):
                nodeTemplate = Node.jsonTemplate()
                nodeTemplate['type'] = mimeText
                nodeTemplate['name'] = name
                nodeTemplate['x'] = event.scenePos().x()
                nodeTemplate['y'] = event.scenePos().y()
                nodeTemplate['meta']['label'] = mimeText
                nodeTemplate['uuid'] = None

                if tag == 'Var':
                    modifiers = event.modifiers()
                    if modifiers == QtCore.Qt.NoModifier:
                        nodeTemplate['uuid'] = mimeText
                        nodeTemplate['meta']['var']['uuid'] = mimeText
                        m = QMenu()
                        getterAction = m.addAction('Get')
                        nodeTemplate['type'] = 'GetVarNode'

                        def varGetterCreator():
                            n = self.parent().createNode(nodeTemplate)
                            n.updateNodeShape(label=n.var.name)
                        getterAction.triggered.connect(varGetterCreator)

                        setNodeTemplate = dict(nodeTemplate)
                        setterAction = m.addAction('Set')
                        setNodeTemplate['type'] = 'SetVarNode'
                        setterAction.triggered.connect(lambda: self.parent().createNode(setNodeTemplate))
                        m.exec_(QtGui.QCursor.pos(), None)
                        return
                    if modifiers == QtCore.Qt.ControlModifier:
                        nodeTemplate['type'] = 'GetVarNode'
                        nodeTemplate['uuid'] = mimeText
                        nodeTemplate['meta']['var']['uuid'] = mimeText
                        nodeTemplate['meta']['label'] = self.parent().vars[uuid.UUID(mimeText)].name
                    if modifiers == QtCore.Qt.AltModifier:
                        nodeTemplate['type'] = 'SetVarNode'
                        nodeTemplate['uuid'] = mimeText
                        nodeTemplate['meta']['var']['uuid'] = mimeText
                        nodeTemplate['meta']['label'] = self.parent().vars[uuid.UUID(mimeText)].name

                self.parent().createNode(nodeTemplate)
        else:
            super(SceneClass, self).dropEvent(event)


class NodeBoxLineEdit(QLineEdit):
    def __init__(self, parent, events=True):
        super(NodeBoxLineEdit, self).__init__(parent)
        self.setParent(parent)
        self._events = events
        self.parent = parent
        self.setLocale(QtCore.QLocale(QtCore.QLocale.English,
                       QtCore.QLocale.UnitedStates))
        self.setObjectName("le_nodes")
        style = "background-color: rgb(80, 80, 80);" +\
                "border-radius: 2px;" +\
                "font-size: 14px;" +\
                "border-color: black; border-style: outset; border-width: 1px;"
        self.setStyleSheet(style)
        self.setPlaceholderText("enter node name..")


class NodeBoxTreeWidget(QTreeWidget):
    def __init__(self, parent):
        super(NodeBoxTreeWidget, self).__init__(parent)
        style = "background-color: rgb(40, 40, 40);" +\
                "selection-background-color: rgb(50, 50, 50);" +\
                "border-radius: 2px;" +\
                "font-size: 14px;" +\
                "border-color: black; border-style: outset; border-width: 1px;"
        self.setStyleSheet(style)
        self.setParent(parent)
        self.setFrameShape(QFrame.NoFrame)
        self.setFrameShadow(QFrame.Sunken)
        self.setObjectName("tree_nodes")
        self.setSortingEnabled(True)
        self.setDragEnabled(True)
        self.setColumnCount(1)
        self.setHeaderHidden(True)
        self.setDragDropMode(QAbstractItemView.DragOnly)
        self.setAnimated(True)
        self.categoryPaths = {}

    def _isCategoryExists(self, category_name, categories):
        bFound = False
        if category_name in categories:
            return True
        if not bFound:
            for c in categories:
                sepCatNames = c.split('|')
                if len(sepCatNames) == 1:
                    if category_name == c:
                        return True
                else:
                    for i in range(0, len(sepCatNames)):
                        c = '|'.join(sepCatNames)
                        if category_name == c:
                            return True
                        sepCatNames.pop()
        return False

    def insertNode(self, nodeCategoryPath, name, doc=None):
        nodePath = nodeCategoryPath.split('|')
        categoryPath = ''
        # walk from tree top to bottom, creating folders if needed
        # also writing all paths in dict to avoid duplications
        for folderId in range(0, len(nodePath)):
            folderName = nodePath[folderId]
            if folderId == 0:
                categoryPath = folderName
                if categoryPath not in self.categoryPaths:
                    rootFolderItem = QTreeWidgetItem(self)
                    rootFolderItem.bCategory = True
                    rootFolderItem.setFlags(QtCore.Qt.ItemIsEnabled)
                    rootFolderItem.setText(0, folderName)
                    rootFolderItem.setBackground(folderId, QtGui.QColor(80, 85, 80))
                    self.categoryPaths[categoryPath] = rootFolderItem
            else:
                parentCategoryPath = categoryPath
                categoryPath += '|{}'.format(folderName)
                if categoryPath not in self.categoryPaths:
                    childCategoryItem = QTreeWidgetItem(self.categoryPaths[parentCategoryPath])
                    childCategoryItem.setFlags(QtCore.Qt.ItemIsEnabled)
                    childCategoryItem.bCategory = True
                    childCategoryItem.setText(0, folderName)
                    childCategoryItem.setBackground(0, QtGui.QColor(80, 85, 80))
                    self.categoryPaths[categoryPath] = childCategoryItem
        # create node under constructed folder
        nodeItem = QTreeWidgetItem(self.categoryPaths[categoryPath])
        nodeItem.bCategory = False
        nodeItem.setText(0, name)
        if doc:
            nodeItem.setToolTip(0, doc)

    def refresh(self, dataType=None, pattern='', pinType=None):
        self.clear()
        self.categoryPaths = {}

        for libName in FunctionLibraries.libs():
            foos = FunctionLibraries.getLib(libName)
            for name, foo in foos:
                fooArgNames = inspect.getargspec(foo).args
                fooInpTypes = []
                fooOutTypes = []
                if foo.__annotations__['nodeType'] == NodeTypes.Callable:
                    fooInpTypes.append(DataTypes.Exec)
                    fooOutTypes.append(DataTypes.Exec)

                # consider return type if not None
                if foo.__annotations__['return'] is not None:
                    fooOutTypes.append(foo.__annotations__['return'][0])

                for index in range(len(fooArgNames)):
                    dType = foo.__annotations__[fooArgNames[index]]
                    # if tuple - this means ref pin type (output) + default value
                    # eg: (3, True) - bool with True default val
                    if isinstance(dType, tuple):
                        fooOutTypes.append(dType[0])
                    else:
                        fooInpTypes.append(dType)

                nodeCategoryPath = foo.__annotations__['meta']['Category']
                keywords = foo.__annotations__['meta']['Keywords']
                checkString = name + nodeCategoryPath + ''.join(keywords)
                if pattern.lower() in checkString.lower():
                    # create all nodes items if clicked on canvas
                    if dataType is None:
                        self.insertNode(nodeCategoryPath, name, foo.__doc__)
                    else:
                        if pinType == PinDirection.Output:
                            if dataType in fooInpTypes:
                                self.insertNode(nodeCategoryPath, name, foo.__doc__)
                        else:
                            if dataType in fooOutTypes:
                                self.insertNode(nodeCategoryPath, name, foo.__doc__)

        for node_file_name in Nodes.getNodeNames():
            node_class = Nodes.getNode(node_file_name)
            nodeCategoryPath = node_class.category()

            checkString = node_file_name + nodeCategoryPath + ''.join(node_class.keywords())
            if pattern.lower() not in checkString.lower():
                continue
            if dataType is None:
                self.insertNode(nodeCategoryPath, node_file_name, node_class.description())
            else:
                # if pressed pin is output pin
                # filter by nodes input types
                if pinType == PinDirection.Output:
                    if dataType in node_class.pinTypeHints()['inputs']:
                        self.insertNode(nodeCategoryPath, node_file_name, node_class.description())
                else:
                    # if pressed pin is input pin
                    # filter by nodes output types
                    if dataType in node_class.pinTypeHints()['outputs']:
                        self.insertNode(nodeCategoryPath, node_file_name, node_class.description())
        # expand all categories
        if dataType is not None:
            for categoryItem in self.categoryPaths.values():
                categoryItem.setExpanded(True)

    def keyPressEvent(self, event):
        super(NodeBoxTreeWidget, self).keyPressEvent(event)
        key = event.key()
        if key == QtCore.Qt.Key_Return:
            itm = self.currentItem()
            if not itm.bCategory:
                nodeClassName = self.currentItem().text(0)
                name = self.parent().graph().getUniqNodeName(nodeClassName)
                pos = self.parent().graph().mapToScene(self.parent().graph().mouseReleasePos)
                nodeTemplate = Node.jsonTemplate()
                nodeTemplate['type'] = nodeClassName
                nodeTemplate['name'] = name
                nodeTemplate['x'] = pos.x()
                nodeTemplate['y'] = pos.y()
                nodeTemplate['meta']['label'] = nodeClassName
                nodeTemplate['uuid'] = None
                self.parent().graph().createNode(nodeTemplate)

    def mousePressEvent(self, event):
        super(NodeBoxTreeWidget, self).mousePressEvent(event)
        item_clicked = self.currentItem()
        if not item_clicked:
            event.ignore()
            return
        pressed_text = item_clicked.text(0)

        if pressed_text in self.categoryPaths.keys():
            event.ignore()
            return
        drag = QtGui.QDrag(self)
        mime_data = QtCore.QMimeData()
        pressed_text = "Node|" + pressed_text
        mime_data.setText(pressed_text)
        drag.setMimeData(mime_data)
        drag.exec_()


class NodesBox(QWidget):
    """doc string for NodesBox"""
    def __init__(self, parent, graph=None):
        super(NodesBox, self).__init__(parent)
        self.graph = weakref.ref(graph)
        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setContentsMargins(4, 4, 4, 4)
        self.lineEdit = NodeBoxLineEdit(self)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout.addWidget(self.lineEdit)
        self.treeWidget = NodeBoxTreeWidget(self)
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.headerItem().setText(0, "1")
        self.verticalLayout.addWidget(self.treeWidget)
        self.lineEdit.textChanged.connect(self.leTextChanged)
        self.treeWidget.refresh()
        self.installEventFilter(self)

    def sizeHint(self):
        return QtCore.QSize(400, 250)

    def expandCategory(self):
        for i in self.treeWidget.categoryPaths:
            self.treeWidget.setItemExpanded(self.treeWidget.categoryPaths[i], True)

    def leTextChanged(self):
        if self.lineEdit.text() == '':
            self.lineEdit.setPlaceholderText("enter node name..")
            self.treeWidget.refresh()
            return
        self.treeWidget.refresh(None, self.lineEdit.text())
        self.expandCategory()
        

    def eventFilter(self, object, event):
        if event.type() == QtCore.QEvent.WindowActivate:
            pass
            #print "widget window has gained focus"
        elif event.type()== QtCore.QEvent.WindowDeactivate:
            self.hide()
        elif event.type()== QtCore.QEvent.FocusIn:
            pass
            #print "widget has gained keyboard focus"
        elif event.type()== QtCore.QEvent.FocusOut:
            pass
            #print "widget has lost keyboard focus"


        return False

MANIP_MODE_NONE = 0
MANIP_MODE_SELECT = 1
MANIP_MODE_PAN = 2
MANIP_MODE_MOVE = 3
MANIP_MODE_ZOOM = 4
from Qt.QtWidgets import QGraphicsLinearLayout
class GraphWidget(QGraphicsView, Graph):

    _manipulationMode = MANIP_MODE_NONE

    _backgroundColor = Colors.SceneBackground #QtGui.QColor(50, 50, 50)
    _gridPenS = Colors.GridColor
    _gridPenL = Colors.GridColorDarker
    _gridSizeFine = 30
    _gridSizeCourse = 300

    _mouseWheelZoomRate = 0.0005

    def __init__(self, name, parent=None):
        super(GraphWidget, self).__init__()
        Graph.__init__(self, name)
        self.setDragMode(QGraphicsView.RubberBandDrag)
        self.undoStack = QUndoStack(self)
        self.parent = parent
        self.parent.actionClear_history.triggered.connect(self.undoStack.clear)
        self.parent.listViewUndoStack.setStack(self.undoStack)
        self.menu = QMenu()
        self.setScene(SceneClass(self))
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.pressed_item = None
        self.released_item = None
        self.bPanMode = False
        self.groupers = []
        self._isPanning = False
        self._mousePressed = False
        self._shadows = False
        self._scale = 1.0
        self._panSpeed = 1.0
        self.minimum_scale = 0.5
        self.maximum_scale = 2.0
        self.setViewportUpdateMode(self.FullViewportUpdate)
        self.setCacheMode(QGraphicsView.CacheBackground)

        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setAcceptDrops(True)
        self.setAttribute(QtCore.Qt.WA_AlwaysShowToolTips)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)

        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.setRenderHint(QtGui.QPainter.TextAntialiasing)

        #self.scene().setSceneRect(QtCore.QRect(0, 0, 10000, 10000))
        self.scene().setSceneRect(QtCore.QRectF(0, 0, 10, 10))
        self._grid_spacing = 50
        self.factor = 1
        self.factor_diff = 0
        self.setWindowTitle(self.tr(name))

        self._current_file_name = 'Untitled'
        self._file_name_label = QGraphicsTextItem()
        self._file_name_label.setZValue(5)
        self._file_name_label.setEnabled(False)
        self._file_name_label.setFlag(QGraphicsTextItem.ItemIgnoresTransformations)
        self._file_name_label.setDefaultTextColor(Colors.White)
        self._file_name_label.setPlainText(self._current_file_name)

        self.scene().addItem(self._file_name_label)

        self.real_time_line = QGraphicsPathItem(None, self.scene())

        self.real_time_line.name = 'RealTimeLine'
        self.real_time_line.setPen(QtGui.QPen(Colors.Green, 1.0, QtCore.Qt.DashLine))
        self.mousePressPose = QtCore.QPoint(0, 0)
        self.mousePos = QtCore.QPointF(0, 0)
        self._lastMousePos = QtCore.QPointF(0, 0)
        self._right_button = False
        self._is_rubber_band_selection = False
        self._draw_real_time_line = False
        self._update_items = False
        self._resize_group_mode = False
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.centerOn(QtCore.QPointF(self.sceneRect().width() / 2, self.sceneRect().height() / 2))
        self.initialScrollBarsPos = QtGui.QVector2D(self.horizontalScrollBar().value(), self.verticalScrollBar().value())
        # self.registeredCommands = {}
        # self.registerCommands()
        self._sortcuts_enabled = True
        # self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.grid_size = 10
        self.drawGrigSize = self.grid_size * 2
        self.current_rounded_pos = QtCore.QPointF(0.0, 0.0)
        self.autoPanController = AutoPanController()
        self._bRightBeforeShoutDown = False

        self.node_box = NodesBox(None, self)
        self.node_box.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint)
        self.codeEditors = {}
        self.nodesMoveInfo = {}

        self.boundingRect = self.rect()
        self.addInputNode()

        self.installEventFilter(self)

    def showNodeBox(self, dataType=None, pinType=None):
        self.node_box.show()
        self.node_box.move(QtGui.QCursor.pos())
        self.node_box.treeWidget.refresh(dataType, '', pinType)
        self.node_box.lineEdit.setText("")
        if dataType is None:
            self.node_box.lineEdit.setFocus()

    def shoutDown(self):
        for ed in self.codeEditors.values():
            ed.deleteLater()
        for node in self.getNodes():
            node.kill()
        self.scene().shoutDown()
        self.scene().clear()
        self.node_box.hide()
        self.node_box.lineEdit.clear()

    def moveScrollbar(self, delta):
        x = self.horizontalScrollBar().value() + delta.x()
        y = self.verticalScrollBar().value() + delta.y()
        self.horizontalScrollBar().setValue(x)
        self.verticalScrollBar().setValue(y)

    def setScrollbarsPositions(self, horizontal, vertical):
        try:
            self.horizontalScrollBar().setValue(horizontal)
            self.verticalScrollBar().setValue(vertical)
        except Exception as e:
            print(e)

    def mouseDoubleClickEvent(self, event):
        QGraphicsView.mouseDoubleClickEvent(self, event)
        self.OnDoubleClick(self.mapToScene(event.pos()))
        event.accept()

    def OnDoubleClick(self, pos):
        
        #print self.pressed_item.__class__
        if self.pressed_item and isinstance(self.pressed_item, NodeName):
            if self.pressed_item.IsRenamable():
                name, result = QInputDialog.getText(self, "New name dialog", "Enter new name:")
                if result:
                    self.pressed_item.parentItem().setName(name)
                    self.updatePropertyView(self.pressed_item.parentItem())

    def __del__(self):
        self.tick_timer.stop()

    def findPin(self, uid):
        if uid in self.pins:
            pin = self.pins[uid]
            self.centerOn(pin)
            pin.highlight()

    def Tick(self, deltaTime):
        #if self.autoPanController.isActive():
        #    self.moveScrollbar(self.autoPanController.getDelta())
        for n in self.getNodes():
            n.Tick(deltaTime)
        for e in self.edges.values():
            e.Tick()

    def notify(self, message, duration):
        self.parent.statusBar.showMessage(message, duration)
        print(message)

    def screenShot(self):
        name_filter = "Image (*.png)"
        fName = QFileDialog.getSaveFileName(filter=name_filter)
        if not fName == '':
            print("save screen to {0}".format(fName))
            img = QtGui.QPixmap.grabWidget(self)
            img.save(fName, quality=100)

    def isShortcutsEnabled(self):
        return self._sortcuts_enabled

    def disableSortcuts(self):
        self._sortcuts_enabled = False

    def enableSortcuts(self):
        self._sortcuts_enabled = True

    def findPin(self, pinName):
        node = self.getNodeByName(pinName.split(".")[0])
        if node:
            attr = node.getPinByName(pinName.split(".")[1])
            return attr
        return None

    def getGraphSaveData(self):
        data = {self.name: {'nodes': [], 'edges': [], 'variables': []}}
        # save nodes
        data[self.name]['nodes'] = [node.serialize() for node in self.getNodes()]
        # save edges
        data[self.name]['edges'] = [e.serialize() for e in self.edges.values()]
        # variables
        data[self.name]['variables'] = [v.serialize() for v in self.vars.values()]
        return data

    def save(self, save_as=False):
        if save_as:
            name_filter = "Graph files (*.json)"
            pth = QFileDialog.getSaveFileName(filter=name_filter)
            if not pth == '':
                self._current_file_name = pth
            else:
                self._current_file_name = "Untitled"
        else:
            if not path.isfile(self._current_file_name):
                name_filter = "Graph files (*.json)"
                pth = QFileDialog.getSaveFileName(filter=name_filter)
                if not pth == '':
                    self._current_file_name = pth
                else:
                    self._current_file_name = "Untitled"

        if self._current_file_name in ["", "Untitled"]:
            return

        if not self._current_file_name == '':
            with open(self._current_file_name, 'w') as f:
                graphData = self.getGraphSaveData()
                def to_serializable(val):
                    return {
                        "name": None
                    }
                    return str(val)                
                json.dump(graphData, f,skipkeys=True,default=to_serializable)

            self._file_name_label.setPlainText(self._current_file_name)
            print(str("// saved: '{0}'".format(self._current_file_name)))

    def save_as(self):
        self.save(True)

    def addInputNode(self):
        #self.inputsItem = Node("__scene_inputs__",self)
        self.inputsItem = getNodeInstance(Nodes, "scene_inputs", "__scene_inputs__", self)
        Graph.addNode(self, self.inputsItem, {"x":0,"y":0})
        self.scene().addItem(self.inputsItem)
      
    def new_file(self):
        self._current_file_name = 'Untitled'
        self._file_name_label.setPlainText('Untitled')
        for node in self.getNodes():
            node.kill()
        self.vars.clear()
        self.parent.variablesWidget.listWidget.clear()
        self.undoStack.clear()
        self._clearPropertiesView()
        self.addInputNode()

    def load(self):
        name_filter = "Graph files (*.json)"
        fpath = QFileDialog.getOpenFileName(filter=name_filter)
        if not fpath == '':
            with open(fpath, 'r') as f:
                data = json.load(f)
                self.new_file()
                # vars
                for varJson in data[self.name]['variables']:
                    try:
                        VariableBase.deserialize(varJson, self)
                    except Exception as e:
                        print(varJson)
                        print(e)                           
                # nodes
                for nodeJson in data[self.name]['nodes']:
                    try:
                        if nodeJson["name"] != "__scene_inputs__":
                            Node.deserialize(nodeJson, self)
                        else:
                            self.inputsItem.kill()
                            self.inputsItem = Node.deserialize(nodeJson, self)
                    except Exception as e:
                        print(nodeJson)
                        print(e)
                # edges
                for edgeJson in data[self.name]['edges']:
                    try:
                        Edge.deserialize(edgeJson, self)
                    except Exception as e:
                        print(edgeJson)
                        print(e)                        
                self._current_file_name = fpath
                self._file_name_label.setPlainText(self._current_file_name)
                self.frame()
                self.undoStack.clear()

    def getPinByFullName(self, full_name):
        node_name = full_name.split('.')[0]
        pinName = full_name.split('.')[1]
        node = self.getNodeByName(node_name)
        if node:
            Pin = node.getPinByName(pinName)
            if Pin:
                return Pin

    def frame(self):
        nodes_rect = self.getNodesRect()
        if nodes_rect:
            self.centerOn(nodes_rect.center())

    def getNodesRect(self, selected=False):
        rectangles = []
        if selected:
            for n in [n for n in self.getNodes() if n.isSelected()]:
                n_rect = QtCore.QRectF(n.scenePos(),
                                       QtCore.QPointF(n.scenePos().x() + float(n.w),
                                                      n.scenePos().y() + float(n.h)))
                rectangles.append([n_rect.x(), n_rect.y(), n_rect.bottomRight().x(), n_rect.bottomRight().y()])
        else:
            for n in self.getNodes():
                n_rect = QtCore.QRectF(n.scenePos(),
                                       QtCore.QPointF(n.scenePos().x() + float(n.w),
                                                      n.scenePos().y() + float(n.h)))
                rectangles.append([n_rect.x(), n_rect.y(), n_rect.bottomRight().x(), n_rect.bottomRight().y()])

        arr1 = [i[0] for i in rectangles]
        arr2 = [i[2] for i in rectangles]
        arr3 = [i[1] for i in rectangles]
        arr4 = [i[3] for i in rectangles]
        if any([len(arr1) == 0, len(arr2) == 0, len(arr3) == 0, len(arr4) == 0]):
            return None
        min_x = min(arr1)
        max_x = max(arr2)
        min_y = min(arr3)
        max_y = max(arr4)

        return QtCore.QRect(QtCore.QPoint(min_x, min_y), QtCore.QPoint(max_x, max_y))

    def selectedNodes(self):
        return [i for i in self.getNodes() if i.isSelected()]

    def killSelectedNodes(self):
        selectedNodes = self.selectedNodes()
        if self.isShortcutsEnabled() and len(selectedNodes) > 0:
            cmdRemove = Commands.RemoveNodes(selectedNodes, self)
            self.undoStack.push(cmdRemove)
            clearLayout(self.parent.formLayout)

    def keyPressEvent(self, event):
        modifiers = event.modifiers()
        if all([event.key() == QtCore.Qt.Key_N, modifiers == QtCore.Qt.ControlModifier]):
            self.new_file()
        if all([event.key() == QtCore.Qt.Key_C, modifiers == QtCore.Qt.NoModifier]):
            if self.isShortcutsEnabled():
                # create comment node
                rect = Nodes.commentNode.commentNode.getNodesRect(self.selectedNodes())
                if rect:
                    rect.setTop(rect.top() - 20)
                    rect.setLeft(rect.left() - 20)

                    rect.setRight(rect.right() + 20)
                    rect.setBottom(rect.bottom() + 20)

                nodeTemplate = Node.jsonTemplate()
                nodeTemplate['type'] = Nodes.commentNode.commentNode.__name__
                nodeTemplate['name'] = self.getUniqNodeName(Nodes.commentNode.commentNode.__name__)

                if rect:
                    nodeTemplate['x'] = rect.topLeft().x()
                    nodeTemplate['y'] = rect.topLeft().y()
                else:
                    nodeTemplate['x'] = self.mapToScene(self.mousePos).x()
                    nodeTemplate['y'] = self.mapToScene(self.mousePos).y()
                nodeTemplate['meta']['label'] = Nodes.commentNode.commentNode.__name__
                nodeTemplate['uuid'] = None
                instance = self.createNode(nodeTemplate)
                if rect:
                    instance.rect.setRight(rect.width())
                    instance.rect.setBottom(rect.height())
                    instance.label().width = rect.width()
                    instance.label().adjustSizes()

        if all([event.key() == QtCore.Qt.Key_Left, modifiers == QtCore.Qt.ControlModifier | QtCore.Qt.ShiftModifier]):
            self.alignSelectedNodes(Direction.Left)
            return
        if all([event.key() == QtCore.Qt.Key_Up, modifiers == QtCore.Qt.ControlModifier | QtCore.Qt.ShiftModifier]):
            self.alignSelectedNodes(Direction.Up)
            return
        if all([event.key() == QtCore.Qt.Key_Right, modifiers == QtCore.Qt.ControlModifier | QtCore.Qt.ShiftModifier]):
            self.alignSelectedNodes(Direction.Right)
            return
        if all([event.key() == QtCore.Qt.Key_Down, modifiers == QtCore.Qt.ControlModifier | QtCore.Qt.ShiftModifier]):
            self.alignSelectedNodes(Direction.Down)
            return

        if all([event.key() == QtCore.Qt.Key_Z, modifiers == QtCore.Qt.ControlModifier]):
            if self.isShortcutsEnabled():
                self.undoStack.undo()
        if all([event.key() == QtCore.Qt.Key_Y, modifiers == QtCore.Qt.ControlModifier]):
            if self.isShortcutsEnabled():
                self.undoStack.redo()
        if all([event.key() == QtCore.Qt.Key_R, modifiers == QtCore.Qt.ControlModifier]):
            self.reset_scale()
        if all([event.key() == QtCore.Qt.Key_S, modifiers == QtCore.Qt.ControlModifier]):
            self.save()
        if all([event.key() == QtCore.Qt.Key_O, modifiers == QtCore.Qt.ControlModifier]):
            self.load()
        if all([event.key() == QtCore.Qt.Key_S, modifiers == QtCore.Qt.ControlModifier | QtCore.Qt.ShiftModifier]):
            self.save_as()
        if all([event.key() == QtCore.Qt.Key_F, modifiers == QtCore.Qt.ControlModifier]):
            self.frame()
        if event.key() == QtCore.Qt.Key_Delete:
            self.killSelectedNodes()
        if all([event.key() == QtCore.Qt.Key_D, modifiers == QtCore.Qt.ControlModifier]):
            self.duplicateNodes()
        if all([event.key() == QtCore.Qt.Key_C, modifiers == QtCore.Qt.ControlModifier]):
            self.copyNodes()
        if all([event.key() == QtCore.Qt.Key_V, modifiers == QtCore.Qt.ControlModifier]):
            self.pasteNodes()
        QGraphicsView.keyPressEvent(self, event)

    def duplicateNodes(self):
        selectedNodes = [i for i in self.getNodes() if i.isSelected()]

        if len(selectedNodes) > 0:
            diff = QtCore.QPointF(self.mapToScene(self.mousePos)) - selectedNodes[0].scenePos()
            newNodes = []
            oldNodes = []
            edges = []
            for n in selectedNodes:
                new_node = n.clone()
                n.setSelected(False)
                new_node.setSelected(True)
                new_node.setPos(new_node.scenePos() + diff)
                newNodes.append(new_node)
                oldNodes.append(n)
                for i in n.inputs.values()+n.outputs.values():
                    edges += i.edge_list                
            
            for e in edges:
                if e.source().parent() in oldNodes and e.destination().parent() in oldNodes:
                    nsrc =  newNodes[oldNodes.index(e.source().parent())].getPinByName(e.source().name)
                    ndst =  newNodes[oldNodes.index(e.destination().parent())].getPinByName(e.destination().name)
                    self.addEdge(nsrc,ndst)
                elif e.source().parent() not in oldNodes and e.source().dataType != DataTypes.Exec:
                    nsrc =  e.source()
                    ndst =  newNodes[oldNodes.index(e.destination().parent())].getPinByName(e.destination().name)
                    self.addEdge(nsrc,ndst)           

    def copyNodes(self):
        QApplication.clipboard().clear()
        nodes = []
        oldNodes = []
        selectedNodes = [i for i in self.getNodes() if i.isSelected()]
        edges = []
        for n in selectedNodes:
            oldNodes.append(n)
            nodes.append(n.serialize())
            for i in n.inputs.values()+n.outputs.values():
                edges += i.edge_list
        fullEdges = []
        for e in edges:
            if e.source().parent() in oldNodes and e.destination().parent() in oldNodes:
                fullEdges.append({"full":True,"sourcenode":e.source().parent().name,"sourcePin":e.source().name,"destinationNode":e.destination().parent().name,"destinationPin":e.destination().name})
            elif e.source().parent() not in oldNodes and e.source().dataType != DataTypes.Exec:
                fullEdges.append({"full":False,"sourcenode":e.source().parent().name,"sourcePin":e.source().name,"destinationNode":e.destination().parent().name,"destinationPin":e.destination().name})
        ret = {"nodes":nodes,"edges":fullEdges}             

        QApplication.clipboard().setText(str(ret))

    def pasteNodes(self):
        
        try:
            nodes = ast.literal_eval(QApplication.clipboard().text())
            if not nodes.has_key("nodes") or not nodes.has_key("edges"):
                return
        except:
            return
        diff = QtCore.QPointF(self.mapToScene(self.mousePos)) - QtCore.QPointF(nodes["nodes"][0]["x"],nodes["nodes"][0]["y"])
        self.clearSelection()
        newNodes = {}

        for node in nodes["nodes"]:
            oldName = node["name"]
            node["name"] = self.getUniqNodeName(node["name"])
            node['uuid'] = str(uuid.uuid4())
            for inp in node['inputs']:
                inp['uuid'] = str(uuid.uuid4())
            for out in node['outputs']:
                out['uuid'] = str(uuid.uuid4())            
            n = self.createNode(node)
            newNodes[oldName]=n
            n.setSelected(True)
            n.setPos(n.scenePos() + diff)
        for edge in nodes["edges"]:
            if edge["full"]:
                nsrc = newNodes[edge["sourcenode"]].getPinByName(edge["sourcePin"])
                ndst = newNodes[edge["destinationNode"]].getPinByName(edge["destinationPin"])
                self.addEdge(nsrc,ndst)
            else:
                nsrc = self.getNodeByName(edge["sourcenode"])
                if nsrc != None:
                    nsrc = nsrc.getPinByName(edge["sourcePin"])
                    if nsrc != None:
                        ndst = newNodes[edge["destinationNode"]].getPinByName(edge["destinationPin"])
                        self.addEdge(nsrc,ndst)


        
    def alignSelectedNodes(self, direction):
        ls = [n for n in self.getNodes() if n.isSelected()]
        nodesMoveInfo = {}
        # {'from': [], 'to': []}
        for node in ls:
            nodesMoveInfo[node.uid] = {'from': node.scenePos(), 'to': QtCore.QPointF()}

        x_positions = [p.scenePos().x() for p in ls]
        y_positions = [p.scenePos().y() for p in ls]

        if direction == Direction.Left:
            if len(x_positions) == 0:
                return
            x = min(x_positions)
            for n in ls:
                p = n.scenePos()
                p.setX(x)
                nodesMoveInfo[n.uid]['to'] = p

        if direction == Direction.Right:
            if len(x_positions) == 0:
                return
            x = max(x_positions)
            for n in ls:
                p = n.scenePos()
                p.setX(x)
                nodesMoveInfo[n.uid]['to'] = p

        if direction == Direction.Up:
            if len(y_positions) == 0:
                return
            y = min(y_positions)
            for n in ls:
                p = n.scenePos()
                p.setY(y)
                nodesMoveInfo[n.uid]['to'] = p

        if direction == Direction.Down:
            if len(y_positions) == 0:
                return
            y = max(y_positions)
            for n in ls:
                p = n.scenePos()
                p.setY(y)
                nodesMoveInfo[n.uid]['to'] = p

        self.undoStack.push(Commands.Move(dict(nodesMoveInfo), self))

    def findGoodPlaceForNewNode(self):
        polygon = self.mapToScene(self.viewport().rect())
        ls = polygon.toList()
        point = QtCore.QPointF((ls[1].x() - ls[0].x()) / 2, (ls[3].y() - ls[2].y()) / 2)
        point += ls[0]
        point.setY(point.y() + polygon.boundingRect().height() / 3)
        point += QtCore.QPointF(float(random.randint(50, 200)), float(random.randint(50, 200)))
        return point

    def keyReleaseEvent(self, event):
        QGraphicsView.keyReleaseEvent(self, event)

    def pan(self, delta):
        rect = self.sceneRect()
        rect.translate(-delta.x(), -delta.y())
        self.setSceneRect(rect)

    def nodeFromInstance(self,instance):
        if isinstance(instance,Node):
            return instance
        node = instance
        while  (isinstance(node, QGraphicsItem) or isinstance(node, QGraphicsWidget) or isinstance(node, QGraphicsProxyWidget) )and node.parentItem() != None:
            node = node.parentItem() 
        return node 

    def removeItemByName(self, name):
        [self.scene().removeItem(i) for i in self.scene().items() if hasattr(i, 'name') and i.name == name]

    def clearSelection(self):
        for node in self.selectedNodes():
            node.setSelected(False)       

    def mousePressEvent(self, event):    
        node = None
        self.pressed_item = self.itemAt(event.pos())
        if not self.pressed_item or self.nodeFromInstance(self.pressed_item) == self.inputsItem and not isinstance(self.pressed_item, PinBase):
            if event.button() == QtCore.Qt.LeftButton:
                self._manipulationMode = MANIP_MODE_SELECT
                self._selectionRect = SelectionRect(graph=self, mouseDownPos=self.mapToScene(event.pos()))
                self._mouseDownSelection = self.selectedNodes()
                super(GraphWidget, self).mousePressEvent(event)
            elif event.button() == QtCore.Qt.MiddleButton or event.button() == QtCore.Qt.MiddleButton and modifiers == QtCore.Qt.NoModifier:
                self.viewport().setCursor(QtCore.Qt.OpenHandCursor)
                self._manipulationMode = MANIP_MODE_PAN
                self._lastPanPoint = self.mapToScene(event.pos())                
            elif event.button() == QtCore.Qt.RightButton:
                self.viewport().setCursor(QtCore.Qt.SizeHorCursor)
                self._manipulationMode = MANIP_MODE_ZOOM
                self._lastMousePos = event.pos()
                self._lastTransform = QtGui.QTransform(self.transform())
                self._lastSceneRect = self.sceneRect()
                self._lastSceneCenter = self._lastSceneRect.center()
                self._lastScenePos = self.mapToScene(event.pos())
                self._lastOffsetFromSceneCenter = self._lastScenePos - self._lastSceneCenter
            else:
                super(GraphWidget, self).mousePressEvent(event) 
            self.node_box.hide()
        else:
            

            self.mousePressPose = event.pos()
            if not isinstance(self.pressed_item, NodesBox) and self.node_box.isVisible():
                self.node_box.hide()
                self.node_box.lineEdit.clear()

            modifiers = event.modifiers()
            if isinstance(self.pressed_item, QGraphicsItem):
                #self.autoPanController.start()
                if isinstance(self.pressed_item, PinBase):
                    if event.button() == QtCore.Qt.LeftButton:
                        self.pressed_item.parent().setFlag(QGraphicsItem.ItemIsMovable, False)
                        self.pressed_item.parent().setFlag(QGraphicsItem.ItemIsSelectable, False)
                        self._draw_real_time_line = True
                    if modifiers == QtCore.Qt.AltModifier:
                        self.removeEdgeCmd(self.pressed_item.edge_list)
                else:
                    super(GraphWidget, self).mousePressEvent(event)
                    if isinstance(self.pressed_item,Nodes.commentNode.commentNode):
                        node = self.nodeFromInstance(self.pressed_item)
                        if node.bResize:
                            return

                    if (event.button() == QtCore.Qt.MidButton or event.button() == QtCore.Qt.LeftButton):
                        self._manipulationMode = MANIP_MODE_MOVE
                        self._lastDragPoint =self.mapToScene(event.pos())
                    if event.button() == QtCore.Qt.MidButton:    
                        if modifiers != QtCore.Qt.ShiftModifier:
                            self.clearSelection()
                        self.pressed_node = self.nodeFromInstance(self.pressed_item)
                        self.pressed_node.setSelected(True)
                        selectedNodes = self.selectedNodes()    
                        if len(selectedNodes) > 0:                               
                            for node in  selectedNodes:
                                compute_order = self.getEvaluationOrder(node)                                     
                                for layer in reversed(sorted([i for i in compute_order.keys()])):
                                    for n in compute_order[layer]:
                                        n.setSelected(True)
                                node.setSelected(True)
                                if isinstance(node,Nodes.commentNode.commentNode):
                                    for n in node.nodesToMove:
                                        n.setSelected(True)
                    else:
                        self.pressed_item.setSelected(True)

    def mouseMoveEvent(self, event):

        self.mousePos = event.pos()

        if self._draw_real_time_line:
            if isinstance(self.pressed_item, PinBase):
                if self.pressed_item.parentItem().isSelected():
                    self.pressed_item.parentItem().setSelected(False)
            if self.real_time_line not in self.scene().items():
                self.scene().addItem(self.real_time_line)

            p1 = self.pressed_item.scenePos() + self.pressed_item.boundingRect().center()
            p2 = self.mapToScene(self.mousePos)

            distance = p2.x() - p1.x()
            multiply = 3
            path = QtGui.QPainterPath()
            path.moveTo(p1)
            path.cubicTo(QtCore.QPoint(p1.x() + distance / multiply, p1.y()), QtCore.QPoint(p2.x() - distance / 2, p2.y()), p2)
            self.real_time_line.setPath(path)

        modifiers = event.modifiers()

        if self._manipulationMode == MANIP_MODE_SELECT:
            dragPoint = self.mapToScene(event.pos())
            self._selectionRect.setDragPoint(dragPoint)
            # This logic allows users to use ctrl and shift with rectangle
            # select to add / remove nodes.
            if modifiers == QtCore.Qt.ControlModifier:
                for node in self.getNodes():
                    if node != self.inputsItem:
                        if node in self._mouseDownSelection:
                            if node.isSelected() and self._selectionRect.collidesWithItem(node):
                                node.setSelected(False)
                            elif not node.isSelected() and not self._selectionRect.collidesWithItem(node):
                                node.setSelected(True)
                        else:
                            if not node.isSelected() and self._selectionRect.collidesWithItem(node):
                                node.setSelected(True)
                            elif node.isSelected() and not self._selectionRect.collidesWithItem(node):
                                if node not in self._mouseDownSelection:
                                    node.setSelected(False)

            elif modifiers == QtCore.Qt.ShiftModifier:
                for node in self.getNodes():
                    if node != self.inputsItem:
                        if not node.isSelected() and self._selectionRect.collidesWithItem(node):
                            node.setSelected(True)
                        elif node.isSelected() and not self._selectionRect.collidesWithItem(node):
                            if node not in self._mouseDownSelection:
                                node.setSelected(False)

            else:
                self.clearSelection()
                for node in self.getNodes():
                    if node != self.inputsItem:
                        if not node.isSelected() and self._selectionRect.collidesWithItem(node):
                            node.setSelected(True)
                        elif node.isSelected() and not self._selectionRect.collidesWithItem(node):
                            node.setSelected(False)

        elif self._manipulationMode == MANIP_MODE_MOVE :
            newPos = self.mapToScene(event.pos())
            delta = newPos - self._lastDragPoint
            self._lastDragPoint = self.mapToScene(event.pos())
            selectedNodes = self.selectedNodes()
            # Apply the delta to each selected node
            for node in selectedNodes:
                if node != self.inputsItem:
                    if isinstance(node,Nodes.commentNode.commentNode):
                        for n in node.nodesToMove:
                            if not n.isSelected():
                                n.translate(delta.x(), delta.y())
                    node.translate(delta.x(), delta.y())

        elif self._manipulationMode == MANIP_MODE_PAN:
            delta = self.mapToScene(event.pos()) - self._lastPanPoint
            rect = self.sceneRect()
            rect.translate(-delta.x(), -delta.y())
            self.setSceneRect(rect)
            self._lastPanPoint = self.mapToScene(event.pos())

        elif self._manipulationMode == MANIP_MODE_ZOOM:

           # How much
            delta = event.pos() - self._lastMousePos
            #self._lastMousePos = event.pos()
            zoomFactor = 1.0
            if delta.x() > 0:
                zoomFactor = 1.0 + delta.x() / 100.0
            else:
                zoomFactor = 1.0 / (1.0 + abs(delta.x()) / 100.0)

            # Limit zoom to 3x
            if self._lastTransform.m22() * zoomFactor >= 2.0:
                return

            # Reset to when we mouse pressed
            self.setSceneRect(self._lastSceneRect)
            self.setTransform(self._lastTransform)

            # Center scene around mouse down
            rect = self.sceneRect()
            rect.translate(self._lastOffsetFromSceneCenter)
            self.setSceneRect(rect)

            # Zoom in (QGraphicsView auto-centers!)
            self.scale(zoomFactor, zoomFactor)

            newSceneCenter = self.sceneRect().center()
            newScenePos = self.mapToScene(self._lastMousePos)
            newOffsetFromSceneCenter = newScenePos - newSceneCenter

            # Put mouse down back where is was on screen
            rect = self.sceneRect()
            rect.translate(-1 * newOffsetFromSceneCenter)
            self.setSceneRect(rect)

            # Call udpate to redraw background
            self.update()


        else:
            super(GraphWidget, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        super(GraphWidget, self).mouseReleaseEvent(event)

        #self.autoPanController.stop()
        self.mouseReleasePos = event.pos()
        self.released_item = self.itemAt(event.pos())
        self._resize_group_mode = False

        for n in self.getNodes():
            n.setFlag(QGraphicsItem.ItemIsMovable)
            n.setFlag(QGraphicsItem.ItemIsSelectable)

        if self._draw_real_time_line:
            self._draw_real_time_line = False
            if self.real_time_line in self.scene().items():
                self.removeItemByName('RealTimeLine')
        elif self._manipulationMode == MANIP_MODE_PAN:
            self.viewport().setCursor(QtCore.Qt.ArrowCursor)
            self._manipulationMode = MANIP_MODE_NONE

        elif self._manipulationMode == MANIP_MODE_SELECT:
            # If users simply clicks in the empty space, clear selection.
            if self.mapToScene(event.pos()) == self._selectionRect.pos():
                self.clearSelection()
            self._selectionRect.destroy()
            self._selectionRect = None
            self._manipulationMode = MANIP_MODE_NONE

        elif self._manipulationMode == MANIP_MODE_MOVE:
            self._manipulationMode = MANIP_MODE_NONE

        elif self._manipulationMode == MANIP_MODE_ZOOM:
            self.viewport().setCursor(QtCore.Qt.ArrowCursor)
            self._manipulationMode = MANIP_MODE_NONE
        if event.button() == QtCore.Qt.RightButton:
            # show nodebox only if drag is small and no items under cursor
            if self.pressed_item is None or isinstance(self.pressed_item, Nodes.commentNode.commentNode):
                dragDiff = self.mapToScene(self.mousePressPose) - self.mapToScene(event.pos())
                if all([abs(i) < 0.4 for i in [dragDiff.x(), dragDiff.y()]]):
                    self.showNodeBox()
        elif event.button() == QtCore.Qt.LeftButton and not isinstance(self.released_item, PinBase):
            if isinstance(self.pressed_item, PinBase):
                # node box tree pops up
                # with nodes taking supported data types of pressed Pin as input
                self.showNodeBox(self.pressed_item.dataType, self.pressed_item.direction)

        p_itm = self.pressed_item
        r_itm = self.released_item
        do_connect = True
        for i in [p_itm, r_itm]:
            if not i:
                do_connect = False
                break
            if not isinstance(i, PinBase):
                do_connect = False
                break
        if p_itm and r_itm:
            if p_itm != r_itm:
                if isinstance(p_itm, PinBase) and isinstance(r_itm, PinBase):
                    if cycle_check(p_itm, r_itm):
                        print('cycles are not allowed')
                        do_connect = False

        if do_connect:
            if p_itm != r_itm:
                self.addEdge(p_itm, r_itm)

        selectedNodes = self.selectedNodes()
        if len(selectedNodes) != 0 and event.button() == QtCore.Qt.LeftButton:
            self.tryFillPropertiesView(selectedNodes[0])
        elif event.button() == QtCore.Qt.LeftButton:
            self._clearPropertiesView()

    def tryFillPropertiesView(self, obj):
        '''
            toDO: obj should implement interface class
            with onUpdatePropertyView method
        '''
        if hasattr(obj, 'onUpdatePropertyView'):
            self._clearPropertiesView()
            obj.onUpdatePropertyView(self.parent.formLayout)

    def _clearPropertiesView(self):
        clearLayout(self.parent.formLayout)

    def propertyEditingFinished(self):
        le = QApplication.instance().focusWidget()
        if isinstance(le, QLineEdit):
            nodeName, attr = le.objectName().split('.')
            node = self.getNodeByName(nodeName)
            Pin = node.getPinByName(attr)
            Pin.setData(le.text())

    def wheelEvent(self, event):
        (xfo, invRes) = self.transform().inverted()
        topLeft = xfo.map(self.rect().topLeft())
        bottomRight = xfo.map(self.rect().bottomRight())
        center = ( topLeft + bottomRight ) * 0.5
        zoomFactor = 1.0 + event.delta() * self._mouseWheelZoomRate

        transform = self.transform()

        # Limit zoom to 3x
        if transform.m22() * zoomFactor >= 2.0:
            return

        self.scale(zoomFactor, zoomFactor)

        # Call udpate to redraw background
        self.update()        

    def drawBackground(self, painter, rect):

        super(GraphWidget, self).drawBackground(painter, rect)
        self.boundingRect = rect
        #self.inputsItem.setPos(rect.topLeft().x(),rect.topLeft().y()+50)
        self.inputsItem.update()
        #update(QRectF(x, y, width, height))

        polygon = self.mapToScene(self.viewport().rect())
        self._file_name_label.setPos(polygon[0])

        #self.inputsItem.setPos(self.mapToScene(self.viewport().rect().x(),self.viewport().rect().y()+50) )
        self.inputsItem.setPos(self.boundingRect.topLeft().x(),self.boundingRect.topLeft().y()+50)

        color = self._backgroundColor
        painter.fillRect(rect, QtGui.QBrush(color))

        left = int(rect.left()) - (int(rect.left()) % self._gridSizeFine)
        top = int(rect.top()) - (int(rect.top()) % self._gridSizeFine)

        # Draw horizontal fine lines
        gridLines = []
        painter.setPen(self._gridPenS)
        y = float(top)
        while y < float(rect.bottom()):
            gridLines.append(QtCore.QLineF( rect.left(), y, rect.right(), y ))
            y += self._gridSizeFine
        painter.drawLines(gridLines)

        # Draw vertical fine lines
        gridLines = []
        painter.setPen(self._gridPenS)
        x = float(left)
        while x < float(rect.right()):
            gridLines.append(QtCore.QLineF( x, rect.top(), x, rect.bottom()))
            x += self._gridSizeFine
        painter.drawLines(gridLines)

        # Draw thick grid
        left = int(rect.left()) - (int(rect.left()) % self._gridSizeCourse)
        top = int(rect.top()) - (int(rect.top()) % self._gridSizeCourse)

        # Draw vertical thick lines
        gridLines = []
        painter.setPen(self._gridPenL)
        x = left
        while x < rect.right():
            gridLines.append(QtCore.QLineF( x, rect.top(), x, rect.bottom() ))
            x += self._gridSizeCourse
        painter.drawLines(gridLines)

        # Draw horizontal thick lines
        gridLines = []
        painter.setPen(self._gridPenL)
        y = top
        while y < rect.bottom():
            gridLines.append(QtCore.QLineF( rect.left(), y, rect.right(), y ))
            y += self._gridSizeCourse
        painter.drawLines(gridLines)


    def consoleHelp(self):
        msg = """///// AVAILABLE NODES LIST /////\n\n"""

        for f in listdir(path.dirname(Nodes.__file__)):
            if f.endswith(".py") and "init" not in f:
                msg += "{0}\n".format(f.split(".")[0])

        msg += "\n"

        msg += """///// AVAILABLE COMMANDS /////\n"""
        msg += "\t<<< Builtin >>>\n"
        for c in self.parent.consoleInput.builtinCommands:
            msg += (c + "\n")
        msg += "\t<<< Plugins >>>\n"
        for c in self.registeredCommands:
            msg += (c + " - {0}\n".format(self.registeredCommands[c].usage()))

        if self.parent:
            print(msg)

    def getVarByName(self, name):
        var = None
        for v in self.vars.values():
            if v.name == name:
                var = v
        return var

    def createVariableSetter(self, jsonTemplate):
        try:
            var = self.vars[uuid.UUID(jsonTemplate['meta']['var']['uuid'])]
            instance = SetVarNode(var.name, self, var)
            return instance
        except:
            print "Error on Variable DataTypes"
    def createVariableGetter(self, jsonTemplate):
        try:
            var = self.vars[uuid.UUID(jsonTemplate['meta']['var']['uuid'])]
            instance = GetVarNode(var.name, self, var)
            return instance
        except:
            print "Error on Variable DataTypes"

    def _createNode(self, jsonTemplate):
        nodeInstance = getNodeInstance(Nodes, jsonTemplate['type'], jsonTemplate['name'], self)

        # If not found, check variables
        if nodeInstance is None:

            if jsonTemplate['type'] == 'GetVarNode':
                nodeInstance = self.createVariableGetter(jsonTemplate)
            if jsonTemplate['type'] == 'SetVarNode':
                nodeInstance = self.createVariableSetter(jsonTemplate)

        # set pins data
        for inpJson in jsonTemplate['inputs']:
            pin = nodeInstance.getPinByName(inpJson['name'], PinSelectionGroup.Inputs)
            if pin:
                pin.uid = uuid.UUID(inpJson['uuid'])
                pin.setData(inpJson['value'])
                if inpJson['bDirty']:
                    pin.setDirty()
                else:
                    pin.setClean()

        for outJson in jsonTemplate['outputs']:
            pin = nodeInstance.getPinByName(outJson['name'], PinSelectionGroup.Outputs)
            if pin:
                pin.uid = uuid.UUID(outJson['uuid'])
                pin.setData(outJson['value'])
                if outJson['bDirty']:
                    pin.setDirty()
                else:
                    pin.setClean()

        if nodeInstance is None:
            raise ValueError("node class not found!")
        else:
            self.addNode(nodeInstance, jsonTemplate)
            nodeInstance.postCreate(jsonTemplate)
            return nodeInstance

    def createNode(self, jsonTemplate):
        cmd = Commands.CreateNode(self, jsonTemplate)
        self.undoStack.push(cmd)
        return cmd.nodeInstance

    def addNode(self, node, jsonTemplate=None):
        Graph.addNode(self, node, jsonTemplate)
        self.scene().addItem(node)

    def _addEdge(self, src, dst):
        result = Graph.addEdge(self, src, dst)
        if result:
            if src.direction == PinDirection.Input:
                src, dst = dst, src
            edge = Edge(src, dst, self)
            src.edge_list.append(edge)
            dst.edge_list.append(edge)
            self.scene().addItem(edge)
            self.edges[edge.uid] = edge
            return edge
        return None

    def addEdge(self, src, dst):
        if self.canConnectPins(src, dst):
            cmd = Commands.ConnectPin(self, src, dst)
            self.undoStack.push(cmd)

    def removeEdgeCmd(self, edges):
        cmdRemoveEdges = Commands.RemoveEdges(self, [e.serialize() for e in edges])
        self.undoStack.push(cmdRemoveEdges)

    def removeEdge(self, edge):
        Graph.removeEdge(self, edge)
        edge.source().update()
        edge.destination().update()
        self.edges.pop(edge.uid)
        edge.prepareGeometryChange()
        self.scene().removeItem(edge)

    def plot(self):
        Graph.plot(self)
        print('>>>>>>> {0} <<<<<<<\n{1}\n'.format(self.name, ctime()))
        if self.parent:
            for n in self.getNodes():
                print(n.name)
                for i in n.inputs.values() + n.outputs.values():
                    print('|--- {0} data - {1} affects on {2} affected by {3} DIRTY {4}, uid - {5}'.format(i.getName(),
                          i.currentData(),
                          [p.getName() for p in i.affects],
                          [p.getName() for p in i.affected_by],
                          i.dirty,
                          str(i.uid)))
            print('Variables\n----------')
            for k, v in self.vars.iteritems():
                msg = '{0} - {1}, uid - {2}'.format(v.name, v.value, str(v.uid))
                print(msg)
            print('Pins\n-----------------')
            for pinUid, pin in self.pins.iteritems():
                msg = '{0} - {1}'.format(pinUid, pin.name, str(pin.uid))
                print(msg)
            print('Edges\n-----------------')
            for edgeUid, edge in self.edges.iteritems():
                print(edgeUid, edge)

    def reset_scale(self):
        self.resetMatrix()

    def eventFilter(self, object, event):
        if event.type()== QtCore.QEvent.KeyPress and event.key()== QtCore.Qt.Key_Tab:
            self.showNodeBox()
        return False
