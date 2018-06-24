"""@file Pin.py
"""
from Qt import QtCore
from Qt import QtGui
from Qt.QtWidgets import QGraphicsWidget
from Qt.QtWidgets import QMenu
from Qt.QtWidgets import QApplication
from AbstractGraph import *
from Settings import *


class PinWidgetBase(QGraphicsWidget, PinBase):
    '''
    This is base class for all ui pins
    '''

    ## Event called when pin is connected
    OnPinConnected = QtCore.Signal(object)   
    ## Event called when pin is disconnected
    OnPinDisconnected = QtCore.Signal(object)
    ## Event called when data been set
    dataBeenSet = QtCore.Signal(object)
    ## Event called when pin name changes
    nameChanged = QtCore.Signal(str)
    ## Event called when setUserStruct called
    # used by enums
    userStructChanged = QtCore.Signal(object)
    ## Event called when pin is deleted
    OnPinDeleted = QtCore.Signal(object)
    ## Event called when pin is deleted
    OnPinChanged = QtCore.Signal(object)    
    def __init__(self, name, parent, dataType, direction, **kwargs):
        QGraphicsWidget.__init__(self)
        PinBase.__init__(self, name, parent, dataType, direction, **kwargs)
        self.setParentItem(parent)
        self.setCursor(QtCore.Qt.CrossCursor)
        ## context menu for pin
        self.menu = QMenu()
        ## Disconnect all connections
        self.actionDisconnect = self.menu.addAction('disconnect all')
        self.actionDisconnect.triggered.connect(self.disconnectAll)
        ## Copy UUID to buffer
        self.actionCopyUid = self.menu.addAction('copy uid')
        self.actionCopyUid.triggered.connect(self.saveUidToClipboard)

        ## Call exec pin
        self.actionCall = self.menu.addAction('execute')
        self.actionCall.triggered.connect(self.call)
        self.newPos = QtCore.QPointF()
        self.setFlag(QGraphicsWidget.ItemSendsGeometryChanges)
        self.setCacheMode(self.DeviceCoordinateCache)
        self.setAcceptHoverEvents(True)
        self.setZValue(2)
        self.width = 8 + 1
        self.height = 8 + 1
        self.hovered = False
        self.startPos = None
        self.endPos = None
        self._container = None
        self._execPen = QtGui.QPen(Colors.Exec, 0.5, QtCore.Qt.SolidLine)
        self.setGeometry(0, 0, self.width, self.height)
        self._dirty_pen = QtGui.QPen(Colors.DirtyPen, 0.5, QtCore.Qt.DashLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin)
        
        self.pinImage = QtGui.QImage(':/icons/resources/array.png')
        self.bLabelHidden = False
        self.bAnimate = False
        self._val = 0
        self.constraint = None
        self.dynamic = False
        self._isEditable = False
        
    def updateConstraint(self,constraint):
        self.constraint = constraint
        if self.parent()._Constraints.has_key(constraint):
            self.parent()._Constraints[constraint].append(self)
        else:
            self.parent()._Constraints[constraint] = [self]
                   
    def setUserStruct(self, inStruct):
        PinBase.setUserStruct(self, inStruct)
        self.userStructChanged.emit(inStruct)

    def setDeletable(self):
        self.deletable = True
        self.actionRemove = self.menu.addAction('remove')
        self.actionRemove.triggered.connect(self.kill)

    def setName(self, newName):
        super(PinWidgetBase, self).setName(newName)
        self.nameChanged.emit(newName)

    def setData(self, value):
        PinBase.setData(self, value)
        self.dataBeenSet.emit(value)
    @property
    def dataType(self):
        return self._dataType
    @dataType.setter
    def dataType(self, value):
        self._dataType = value
        
    def setDataType(self,value):
        self.dataType = value
    def highlight(self):
        self.bAnimate = True
        t = QtCore.QTimeLine(900, self)
        t.setFrameRange(0, 100)
        t.frameChanged[int].connect(self.animFrameChanged)
        t.finished.connect(self.animationFinished)
        t.start()

    def animFrameChanged(self, value):
        self.width = clamp(math.sin(self._val) * 9, 4.5, 25)
        self.update()
        self._val += 0.1

    def animationFinished(self):
        self.width = 9
        self.update()
        self._val = 0

    @staticmethod
    def color():
        return QtGui.QColor()
        
    def call(self):
        PinBase.call(self)

    def kill(self):
        self.OnPinDeleted.emit(self)
        PinBase.kill(self)
        self.disconnectAll()
        if hasattr(self.parent(), self.name):
            delattr(self.parent(), self.name)
        if self._container is not None:
            self.parent().graph().scene().removeItem(self._container)
            if self.direction == PinDirection.Input:
                self.parent().inputsLayout.removeItem(self._container)
            else:
                self.parent().outputsLayout.removeItem(self._container)
        #print self.parent().outputs

    @staticmethod
    def deserialize(owningNode, jsonData):

        name = jsonData['name']
        dataType = jsonData['dataType']

        direction = jsonData['direction']
        value = jsonData['value']
        uid = uuid.UUID(jsonData['uuid'])
        bLabelHidden = jsonData['bLabelHidden']
        bDirty = jsonData['bDirty']
        deletable = jsonData['deletable']
        if 'editable' in jsonData:
            editable = jsonData['editable']
        else:
            editable = False
        p = None
        if direction == PinDirection.Input:
            p = owningNode.addInputPin(name, dataType, hideLabel=bLabelHidden,editable=editable)
            p.uid = uid
        else:
            p = owningNode.addOutputPin(name, dataType, hideLabel=bLabelHidden,editable=editable)
            p.uid = uid
        if deletable:
            p.setDeletable() 
        if "curr_dataType" in jsonData and jsonData["curr_dataType"] != dataType:
            from ..Pins import CreatePin
            a = CreatePin("", None, jsonData["curr_dataType"], 0)
            p.setType(a)
            del a            
            
        p.setData(value)
        return p

    def serialize(self):
        data = PinBase.serialize(self)
        data['bLabelHidden'] = self.bLabelHidden
        data["editable"] = self._isEditable
        return data

    def ungrabMouseEvent(self, event):
        super(PinWidgetBase, self).ungrabMouseEvent(event)

    def get_container(self):
        return self._container

    #def translate(self, x, y):
    #    super(PinWidgetBase, self).moveBy(x, y)

    def boundingRect(self):
        if not self.dataType == DataTypes.Exec:
            return QtCore.QRectF(0, -0.5, 8 * 1.5, 8 + 1.0)
        else:
            return QtCore.QRectF(0, -0.5, 10 * 1.5, 10 + 1.0)

    def sizeHint(self, which, constraint):
        return QtCore.QSizeF(self.width, self.height)

    def saveUidToClipboard(self):
        clipboard = QApplication.clipboard()
        clipboard.clear()
        clipboard.setText(str(self.uid))

    def disconnectAll(self):
        trash = []
        for e in self.edge_list:
            if self.uid == e.destination().uid:
                trash.append(e)
            if self.uid == e.source().uid:
                trash.append(e)
        for e in trash:
            self.parent().graph().removeEdge(e)

    def shape(self):
        path = QtGui.QPainterPath()
        path.addEllipse(self.boundingRect())
        return path

    def paint(self, painter, option, widget):
        background_rect = QtCore.QRectF(0, 0, self.width, self.width)
        self.cPos = background_rect
        w = background_rect.width() / 2
        h = background_rect.height() / 2

        linearGrad = QtGui.QRadialGradient(QtCore.QPointF(w, h), self.width / 2.5)
        if not self._connected:
            linearGrad.setColorAt(0, self.color().darker(280))
            linearGrad.setColorAt(0.5, self.color().darker(280))
            linearGrad.setColorAt(0.65, self.color().lighter(130))
            linearGrad.setColorAt(1, self.color().lighter(70))
        else:
            linearGrad.setColorAt(0, self.color())
            linearGrad.setColorAt(1, self.color())

        if self.hovered:
            linearGrad.setColorAt(1, self.color().lighter(200))
        if self.dataType == DataTypes.Array:
            if self.pinImage:
                painter.drawImage(background_rect, self.pinImage)
            else:
                painter.setBrush(Colors.Array)
                rect = background_rect
                painter.drawRect(rect)
        elif self.dataType == DataTypes.Exec:
            painter.setPen(self._execPen)
            if self._connected:
                painter.setBrush(QtGui.QBrush(self.color()))
            else:
                painter.setBrush(QtCore.Qt.NoBrush)
            arrow = QtGui.QPolygonF([QtCore.QPointF(0.0, 0.0),
                                    QtCore.QPointF(self.width / 2.0, 0.0),
                                    QtCore.QPointF(self.width, self.height / 2.0),
                                    QtCore.QPointF(self.width / 2.0, self.height),
                                    QtCore.QPointF(0, self.height)])
            painter.drawPolygon(arrow)
        else:
            painter.setBrush(QtGui.QBrush(linearGrad))
            rect = background_rect.setX(background_rect.x())
            painter.drawEllipse(background_rect)

    def contextMenuEvent(self, event):
        self.menu.exec_(event.screenPos())

    def getLayout(self):
        if self.direction == PinDirection.Input:
            return self.parent().inputsLayout
        else:
            return self.parent().outputsLayout

    def hoverEnterEvent(self, event):
        super(PinWidgetBase, self).hoverEnterEvent(event)
        self.update()
        self.hovered = True
        self.setToolTip(str(self.currentData()))
        event.accept()

    def hoverLeaveEvent(self, event):
        super(PinWidgetBase, self).hoverLeaveEvent(event)
        self.update()
        self.hovered = False

    def pinConnected(self, other):
        PinBase.pinConnected(self, other)
        #if self.dynamic:
        #    data = self.serialize()
        #    pin = self.deserialize(self.parent(),data)
        #    pin.dynamic=True
        self.OnPinConnected.emit(other)

    def pinDisconnected(self, other):
        PinBase.pinDisconnected(self, other)
        self.OnPinDisconnected.emit(other)
