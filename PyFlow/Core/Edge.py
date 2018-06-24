"""@file Edge.py
Edge is a cubic spline curve. It represents connecton between two pins.
"""
from Qt import QtCore
from Qt import QtGui
from Qt.QtWidgets import QGraphicsPathItem
from Settings import Colors
from AbstractGraph import *
import weakref
from uuid import UUID, uuid4


## Connection between pins
class Edge(QGraphicsPathItem):
    def __init__(self, source, destination, graph):
        QGraphicsPathItem.__init__(self)
        self._uid = uuid4()
        self.graph = weakref.ref(graph)
        self.source = weakref.ref(source)
        self.destination = weakref.ref(destination)
        self.setAcceptedMouseButtons(QtCore.Qt.LeftButton)
        self.setAcceptHoverEvents(True)

        self.mPath = QtGui.QPainterPath()

        self.cp1 = QtCore.QPointF(0.0, 0.0)
        self.cp2 = QtCore.QPointF(0.0, 0.0)

        self.setZValue(-1)

        self.color = self.source().color()

        self.thikness = 1
        if source.dataType == DataTypes.Exec and destination.dataType == DataTypes.Exec:
            self.thikness = 2

        self.pen = QtGui.QPen(self.color, self.thikness, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin)

        points = self.getEndPoints()
        self.updateCurve(points[0], points[1])

        self.setPen(self.pen)

        self.source().update()
        self.destination().update()
        self.fade = 0.0

    def setColor(self, color):
        self.pen.setColor(color)
        self.color = color

    def Tick(self):
        if self.fade > 0:
            self.pen.setWidthF(self.thikness + self.fade * 2)
            r = abs(lerp(self.color.red(), Colors.Yellow.red(), clamp(self.fade, 0, 1)))
            g = abs(lerp(self.color.green(), Colors.Yellow.green(), clamp(self.fade, 0, 1)))
            b = abs(lerp(self.color.blue(), Colors.Yellow.blue(), clamp(self.fade, 0, 1)))
            self.pen.setColor(QtGui.QColor.fromRgb(r, g, b))
            self.fade -= 0.1
            self.update()

    def highlight(self):
        self.fade = 1.0

    @property
    def uid(self):
        return self._uid

    @uid.setter
    def uid(self, value):
        if self._uid in self.graph().edges:
            self.graph().edges[value] = self.graph().edges.pop(self._uid)
            self._uid = value

    @staticmethod
    def deserialize(data, graph):
        srcUUID = UUID(data['sourceUUID'])
        dstUUID = UUID(data['destinationUUID'])
        # if srcUUID in graph.pins and dstUUID in graph.pins:
        srcPin = graph.pins[srcUUID]
        dstPin = graph.pins[dstUUID]
        edge = graph._addEdge(srcPin, dstPin)
        edge.uid = uuid.UUID(data['uuid'])

    def serialize(self):
        script = {'sourceUUID': str(self.source().uid),
                  'destinationUUID': str(self.destination().uid),
                  'sourceName': self.source().getName(),
                  'destinationName': self.destination().getName(),
                  'uuid': str(self.uid)
                  }
        return script

    def __str__(self):
        return '{0}.{1} >>> {2}.{3}'.format(self.source().parent().name,
                                            self.source().name,
                                            self.destination().parent().name,
                                            self.destination().name)

    def hoverEnterEvent(self, event):
        super(Edge, self).hoverEnterEvent(event)
        self.pen.setWidthF(self.thikness + (self.thikness / 1.5))
        self.update()

    def getEndPoints(self):
        
        p1 = self.source().boundingRect().center() + self.source().scenePos()
        p2 = self.destination().boundingRect().center() + self.destination().scenePos()
        return p1, p2

    def mousePressEvent(self, event):
        super(Edge, self).mousePressEvent(event)
        event.accept()

    def mouseReleaseEvent(self, event):
        super(Edge, self).mouseReleaseEvent(event)
        event.accept()

    def mouseMoveEvent(self, event):
        super(Edge, self).mouseMoveEvent(event)
        event.accept()

    def hoverLeaveEvent(self, event):
        super(Edge, self).hoverLeaveEvent(event)
        self.pen.setWidthF(self.thikness)
        self.update()

    def source_port_name(self):
        return self.source().getName()

    def shape(self):
        qp = QtGui.QPainterPathStroker()
        qp.setWidth(10.0)
        qp.setCapStyle(QtCore.Qt.SquareCap)
        return qp.createStroke(self.path())

    def updateCurve(self, p1, p2):
        xDistance = p2.x() - p1.x()
        multiply = 3
        self.mPath = QtGui.QPainterPath()

        direction = QtGui.QVector2D(p1) - QtGui.QVector2D(p2)
        direction.normalize()

        self.mPath.moveTo(p1)
        if xDistance < 0:
            self.mPath.cubicTo(QtCore.QPoint(p1.x() + xDistance / -multiply, p1.y()), QtCore.QPoint(p2.x() - xDistance / -multiply, p2.y()), p2)
        else:
            self.mPath.cubicTo(QtCore.QPoint(p1.x() + xDistance / multiply, p1.y()), QtCore.QPoint(p2.x() - xDistance / 2, p2.y()), p2)

        self.setPath(self.mPath)

    def destination_port_name(self):
        return self.destination().getName()

    def paint(self, painter, option, widget):
        self.setPen(self.pen)
        p1, p2 = self.getEndPoints()
        xDistance = p2.x() - p1.x()
        vDistance = p2.y() - p1.y()

        offset = (abs(xDistance) * 0.1)/4
        defOffset = 200
        #if abs(xDistance) < defOffset:
        offset = defOffset / 3

        if abs(vDistance) < 40:
            offset = abs(xDistance) * 0.3

        multiply = 2
        self.mPath = QtGui.QPainterPath()
        self.mPath.moveTo(p1)

        if xDistance < 0:
            self.cp1 = QtCore.QPoint(p1.x() + offset, p1.y())
            self.cp2 = QtCore.QPoint(p2.x() - offset, p2.y())
        else:
            self.cp2 = QtCore.QPoint(p2.x() - offset, p2.y())
            self.cp1 = QtCore.QPoint(p1.x() + offset, p1.y())

        self.mPath.cubicTo(self.cp1, self.cp2, p2)
        self.setPath(self.mPath)
        super(Edge, self).paint(painter, option, widget)
