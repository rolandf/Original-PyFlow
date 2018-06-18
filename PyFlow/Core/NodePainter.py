"""@file NodePainter.py
"""
from Qt import QtCore
from Qt import QtGui
from Qt.QtWidgets import QStyle
from Settings import *


## Determines how to paint the node
class NodePainter(object):
    @staticmethod
    def asConvertNode(node, painter, option, widget):
        pen = QtGui.QPen(QtCore.Qt.black, 0.5)
        if option.state & QStyle.State_Selected:
            pen.setColor(Colors.Yellow)
            pen.setStyle(QtCore.Qt.SolidLine)
        painter.setPen(pen)
        painter.setBrush(node.bg)
        painter.drawRoundedRect(node.boundingRect(), node.roundFactor, node.roundFactor)

    @staticmethod
    def default(node, painter, option, widget):
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QtCore.Qt.darkGray)

        color = node.color
        color.setAlpha(200)
        if node.isSelected():
            color = color.lighter(150)

        linearGrad = QtGui.QRadialGradient(QtCore.QPointF(40, 40), 300)
        linearGrad.setColorAt(0, color)
        linearGrad.setColorAt(1, color.lighter(180))
        br = QtGui.QBrush(linearGrad)
        painter.setBrush(br)
        pen = QtGui.QPen(QtCore.Qt.black, 0.5)
        if option.state & QStyle.State_Selected:
            pen.setColor(Colors.Yellow)
            pen.setStyle(node.opt_pen_selected_type)
        painter.setPen(pen)
        rect = node.childrenBoundingRect()
        rect.setWidth(node.childrenBoundingRect().width())
        rect.setX(node.childrenBoundingRect().x())
        painter.drawRoundedRect(rect, node.sizes[4], node.sizes[5])

    @staticmethod
    def asGraphSides(node, painter, option, widget):
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QtCore.Qt.darkGray)

        color = Colors.NodeBackgrounds
        #if node.isSelected():
        #    color = color.lighter(150)

        linearGrad = QtGui.QRadialGradient(QtCore.QPointF(40, 40), 300)
        linearGrad.setColorAt(0, color)
        linearGrad.setColorAt(1, color.lighter(180))
        br = QtGui.QBrush(linearGrad)
        painter.setBrush(br)
        pen = QtGui.QPen(Colors.Yellow, 0.5)
        #if option.state & QStyle.State_Selected:
        #    pen.setColor(Colors.Yellow)
        #    pen.setStyle(node.opt_pen_selected_type)
        painter.setPen(pen)
        #print node.boundingRect()
        painter.drawRoundedRect(node.boundingRect(), node.sizes[4], node.sizes[5])