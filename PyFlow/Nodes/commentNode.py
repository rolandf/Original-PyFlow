"""@file CommentNode.py
"""
from ..Core.AbstractGraph import *
from ..Core.Settings import *
from ..Core import Node
from ..Core import Edge
from ..Core import NodeName

from types import MethodType
from Qt.QtWidgets import QGraphicsTextItem
from Qt.QtWidgets import QGraphicsItem
from Qt.QtWidgets import QGraphicsItemGroup
from Qt.QtWidgets import QStyle
from Qt.QtWidgets import QLabel
from Qt.QtWidgets import QLineEdit
from Qt.QtWidgets import QTextBrowser
from Qt.QtWidgets import QPushButton
from Qt.QtWidgets import QMenu
from Qt.QtWidgets import QColorDialog
from Qt import QtGui
from Qt import QtCore


class commentNodeName(NodeName):
    """doc string for commentNodeName"""
    def __init__(self, parent, bUseTextureBg=False, color=Colors.AbsoluteBlack):
        super(commentNodeName, self).__init__(parent, bUseTextureBg, color=color)
        self.color = color
        self.color.setAlpha(80)
        self.setAcceptHoverEvents(True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        self.setDefaultTextColor(QtGui.QColor(255, 255, 255, 255))
        self.roundCornerFactor = 5
        self.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)
        self.width = self.document().documentLayout().documentSize().width()

    def keyPressEvent(self, event):

        QGraphicsTextItem.keyPressEvent(self, event)
        modifires = event.modifiers()
        key = event.key()

        if key == QtCore.Qt.Key_Escape:
            # clear selection
            cursor = QtGui.QTextCursor(self.document())
            cursor.clearSelection()
            self.setTextCursor(cursor)
            # finish editing
            self.setEnabled(False)
            self.setEnabled(True)
        elif not key == QtCore.Qt.Key_Backspace:
            # if backspace is pressed do not change width
            width = self.document().documentLayout().documentSize().width()
            self.h = self.document().documentLayout().documentSize().height()
            # change width if needed
            if width >= self.parentItem().rect.width():
                self.width = width
                self.adjustSizes()

        self.width = self.parentItem().rect.width()
        self.setTextWidth(self.width)
        self.update()

    def adjustSizes(self):
        self.parentItem().rect.setRight(self.width)
        self.setTextWidth(self.width)
        self.h = self.document().documentLayout().documentSize().height()
        self.update()
        self.parentItem().update()

    def paint(self, painter, option, widget):
        QGraphicsTextItem.paint(self, painter, option, widget)
        r = QtCore.QRectF(option.rect)
        r.setWidth(self.width)
        r.setX(0.25)
        r.setY(0.25)
        b = QtGui.QLinearGradient(0, 0, 0, r.height())
        b.setColorAt(0, QtGui.QColor(0, 0, 0, 0))
        b.setColorAt(0.25, self.color)
        b.setColorAt(1, self.color)
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(b)

        r.setHeight(r.height()-1)  
        painter.drawRoundedRect(1, 1, r.width(), r.height(), self.roundCornerFactor, self.roundCornerFactor, QtCore.Qt.AbsoluteSize)
        painter.drawRect(1, r.height() * 0.5 + 2, r.width(), r.height() * 0.5)

        #painter.drawRoundedRect(r, self.roundCornerFactor, self.roundCornerFactor)

    def hoverEnterEvent(self, event):
        NodeName.hoverEnterEvent(self, event)


## Comment node
#
# Can drag intersected nodes.
# You can also specify color and resize it.
class commentNode(Node, NodeBase):
    def __init__(self, name, graph, bUseTextureBg=False, headColor=Colors.AbsoluteBlack):
        super(commentNode, self).__init__(name, graph, headColor=headColor)
        self.color = Colors.AbsoluteBlack
        self.color.setAlpha(80)
        self.nodesToMove = {}
        self.edgesToHide = []       
        self.nodesNamesToMove = []
        self.pinsToMove = {}
        self.commentInputs = []
        self.commentOutpus = []
        self.lastNodePos = self.scenePos()
        self.rect = self.childrenBoundingRect()
        self.initialRectWidth = 0.0
        self.initialRectHeight = 0.0
        self.mousePressPos = self.scenePos()
        self.resizeDirection = (0, 0)
        self.bResize = False
        self.bMove = False
        self.minWidth = 100.0
        self.minHeight = 100.0
        self.lastMousePos = QtCore.QPointF()
        self.setZValue(-2)
        self.expanded = True

    def onChangeColor(self):
        res = QColorDialog.getColor(self.color, None, 'Comment node color setup')
        if res.isValid():
            res.setAlpha(80)
            self.color = res
            self.label().color = res
            self.update()
            self.label().update()

    def serialize(self):
        template = Node.serialize(self)
        if self.expanded:
            bottom = self.rect.bottom()
        else:
            bottom = self.prevRect
        template['meta']['commentNode'] = {
            'w': self.rect.right(),
            'h': bottom,
            'labelHeight': self.label().h,
            'text': self.label().toPlainText(),
            'color': (self.color.getRgb()),
            'expanded':self.expanded,
            'nodesToMove':[str(n.uid) for n in self.nodesToMove]
        }
        return template

    def postCreate(self, jsonTemplate):
        Node.postCreate(self, jsonTemplate)
        # restore text and size
        width = self.minWidth
        height = self.minHeight
        labelHeight = self.label().h
        text = self.__class__.__name__
        # initial color is black
        color = self.color
        self.rect.setBottom(height)
        self.rect.setRight(width)        
        try:
            # if copied in runtime
            width = jsonTemplate['meta']['commentNode']['w']
            height = jsonTemplate['meta']['commentNode']['h']
            labelHeight = jsonTemplate['meta']['commentNode']['labelHeight']
            text = jsonTemplate['meta']['commentNode']['text']
            color = QtGui.QColor(*jsonTemplate['meta']['commentNode']['color'])

            self.rect.setBottom(height)
            self.rect.setRight(width)
            if "nodesToMove" in jsonTemplate['meta']['commentNode']:
                self.nodesNamesToMove =  jsonTemplate['meta']['commentNode']["nodesToMove"]   
                for nodename in  self.nodesNamesToMove:
                    n = self.graph().nodes[uuid.UUID(nodename)]
                    uuid.UUID(nodename)
                    if n != None and n not in self.nodesToMove:
                        self.nodesToMove[n]=n.scenePos()
                self.nodesNamesToMove = []                      
            if "expanded" in jsonTemplate['meta']['commentNode']:
                self.expanded = jsonTemplate['meta']['commentNode']["expanded"]

        except:
            pass            

    
        self.color = color
        self.update()
        self.scene().removeItem(self.label())
        delattr(self, 'label')
        self.label = weakref.ref(commentNodeName(self, False, Colors.White))
        self.label().setPlainText(text)
        self.label().width = self.rect.width()
        self.label().h = labelHeight
        self.label().color = color
        self.label().update()
        self.label().adjustSizes()

    @staticmethod
    def isInRange(mid, val, width=10):
        '''check if val inside strip'''
        leftEdge = mid - width
        rightEdge = mid + width
        return leftEdge <= val <= rightEdge

    def boundingRect(self):
        return self.rect

    def mousePressEvent(self, event):
        QGraphicsItem.mousePressEvent(self, event)
        self.mousePressPos = event.scenePos()
        self.lastNodePos = self.scenePos()
        pBottomRight = self.rect.bottomRight()
        bottomRightRect = QtCore.QRectF(pBottomRight.x() - 6, pBottomRight.y() - 6, 5, 5)
        # detect where on the node
        if bottomRightRect.contains(event.pos()) and self.expanded:
            self.initialRectWidth = self.rect.width()
            self.initialRectHeight = self.rect.height()
            self.resizeDirection = (1, 1)
            self.setFlag(QGraphicsItem.ItemIsMovable, False)
            self.bResize = True
        elif event.pos().x() > (self.rect.width() - 20) and self.expanded:
            self.initialRectWidth = self.rect.width()
            self.resizeDirection = (1, 0)
            self.setFlag(QGraphicsItem.ItemIsMovable, False)
            self.bResize = True
        elif (event.pos().y() + self.label().defaultHeight) > (self.rect.height() - 30) and self.expanded:
            self.initialRectHeight = self.rect.height()
            self.resizeDirection = (0, 1)
            self.setFlag(QGraphicsItem.ItemIsMovable, False)
            self.bResize = True
        if self.expanded:
            self.nodesToMove.clear()
            self.updateChildrens(self.collidingItems())                         
        else:
            nodes = []
            for nodename in  self.nodesNamesToMove:
                nodes.append(self.graph().nodes[nodename])            
            self.updateChildrens(nodes)

    def updateChildrens(self,nodes):
        self.commentInputs =[]
        self.commentOutpus = []
        self.edgesToHide = []   
        self.pinsToMove.clear()  
        self.nodesNamesToMove = []
        edges = []   
        for node in [i for i in nodes if isinstance(i, Node) and not isinstance(i, commentNode)]:
            self.nodesNamesToMove.append(node.uid)
            self.nodesToMove[node] = node.scenePos()
            node.groupNode = self
            for i in node.inputs.values() :
                self.pinsToMove[i] = i.scenePos()
                self.commentInputs.append(i)
            for i in node.outputs.values():
                self.pinsToMove[i] = i.scenePos()
                self.commentOutpus.append(i)
        for node in self.nodesToMove:
            for i in node.inputs.values()+node.outputs.values():
                for edg in i.edge_list:
                    if edg.source().parent() in self.nodesToMove and edg.destination().parent() in self.nodesToMove:
                        self.edgesToHide.append(edg)     

        #for edge in [i for i in self.collidingItems() if isinstance(i, Edge) and not isinstance(i, commentNode)]:
        #    if edge.source().parent() in self.nodesToMove and edge.destination().parent() in self.nodesToMove:
        #        self.edgesToHide.append(edge)         

    def mouseMoveEvent(self, event):
        QGraphicsItem.mouseMoveEvent(self, event)
        delta = self.lastMousePos - event.pos()
        self.lastNodePos = self.scenePos()
        # resize
        if self.bResize:
            delta = event.scenePos() - self.mousePressPos
            if self.resizeDirection == (1, 0):
                # right edge resize
                newWidth = delta.x() + self.initialRectWidth
                if newWidth > self.minWidth:
                    self.label().width = newWidth
                    self.rect.setRight(newWidth)
                    self.label().adjustSizes()

            elif self.resizeDirection == (0, 1):
                newHeight = delta.y() + self.initialRectHeight
                newHeight = max(newHeight, self.label().h + 20.0)
                if newHeight > self.minHeight:
                    # bottom edge resize
                    self.rect.setHeight(newHeight)
            elif self.resizeDirection == (1, 1):
                newWidth = delta.x() + self.initialRectWidth
                #newWidth = roundup(newWidth, self.graph().grid_size)

                newHeight = delta.y() + self.initialRectHeight
                newHeight = max(newHeight, self.label().h + 20.0)
                if newHeight > self.minHeight and newWidth > self.minWidth:
                    self.label().width = newWidth
                    self.rect.setRight(newWidth)
                    self.label().setTextWidth(newWidth)
                    self.rect.setHeight(newHeight)

            self.update()
            self.label().update()
        self.lastMousePos = event.pos()

    def mouseDoubleClickEvent(self, event):
        super(commentNode, self).mouseDoubleClickEvent( event)
        self.OnDoubleClick(self.mapToScene(event.pos()))
        event.accept()        

    def OnDoubleClick(self, pos):
        if self.expanded:
            self.expanded = False
            self.prevRect = self.rect.bottom()
            self.rect.setBottom(self.label().h/2)

            
            for node in self.nodesToMove:
                node.hide()
            
            for pin in self.pinsToMove:
                if pin in self.commentInputs:
                    pin.prevPos = QtCore.QPointF(self.scenePos().x()-8,self.scenePos().y())-pin.scenePos()
                elif pin in self.commentOutpus:
                    pin.prevPos =QtCore.QPointF(self.scenePos().x()+self.boundingRect().width()-8,self.scenePos().y())-pin.scenePos()                    
                pin.translate(pin.prevPos.x(),pin.prevPos.y()) 
                pin.update()
            
            for edge in self.edgesToHide:
                edge.hide()
        else:
            self.expanded = True
            self.rect.setBottom(self.prevRect)
            for node in self.nodesToMove:
                node.show() 
            for pin in self.pinsToMove:
                pin.translate(-pin.prevPos.x(),-pin.prevPos.y())  
            for edge in self.edgesToHide:
                edge.show()                               
        self.update()           

    @staticmethod
    def getNodesRect(nodes):
        rectangles = []

        if len(nodes) == 0:
            return None

        for n in nodes:
            rectangles.append(n.sceneBoundingRect())

        minx_arr = [i.left() for i in rectangles]
        maxx_arr = [i.right() for i in rectangles]
        miny_arr = [i.top() for i in rectangles]
        maxy_arr = [i.bottom() for i in rectangles]

        min_x = min(minx_arr)
        min_y = min(miny_arr)

        max_x = max(maxx_arr)
        max_y = max(maxy_arr)

        return QtCore.QRect(QtCore.QPoint(min_x, min_y), QtCore.QPoint(max_x, max_y))

    def mouseReleaseEvent(self, event):
        QGraphicsItem.mouseReleaseEvent(self, event)
        self.bResize = False

    def paint(self, painter, option, widget):
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QtCore.Qt.darkGray)

        color = Colors.NodeBackgrounds
        if self.isSelected():
            color = color.lighter(150)

        painter.setBrush(self.color)
        pen = QtGui.QPen(QtCore.Qt.black, 0.5)
        if option.state & QStyle.State_Selected:
            pen.setColor(self.graph().window().styleSheetEditor.style.MainColor)
            pen.setStyle(QtCore.Qt.SolidLine)
        painter.setPen(pen)
        painter.drawRoundedRect(self.rect, self.sizes[4], self.sizes[5])

        pen.setColor(Colors.White)
        painter.setPen(pen)

        # draw bottom right resizer
        pBottomRight = self.rect.bottomRight()
        bottomRightRect = QtCore.QRectF(pBottomRight.x() - 6, pBottomRight.y() - 6, 5, 5)
        painter.drawLine(bottomRightRect.bottomLeft(), bottomRightRect.topRight())

        bottomRightRect.setRight(bottomRightRect.left() + bottomRightRect.width() / 2)
        bottomRightRect.setBottom(bottomRightRect.top() + bottomRightRect.height() / 2)
        painter.drawLine(bottomRightRect.bottomLeft(), bottomRightRect.topRight())

        pen.setWidth(1)
        painter.setPen(pen)

        # draw right resizer
        midY = self.rect.center().y()
        pTop = QtCore.QPoint(self.rect.width() - 5, midY - 5)
        pBottom = QtCore.QPoint(self.rect.width() - 5, midY + 5)
        painter.drawLine(pTop, pBottom)

        # draw bottom resizer
        midX = self.rect.center().x()
        pLeft = QtCore.QPoint(midX - 5, self.rect.bottom() - 5)
        pRight = QtCore.QPoint(midX + 5, self.rect.bottom() - 5)
        painter.drawLine(pLeft, pRight)

    def onUpdatePropertyView(self, formLayout):

        # name
        le_name = QLineEdit(self.getName())
        le_name.setReadOnly(True)
        if self.label().IsRenamable():
            le_name.setReadOnly(False)
            le_name.returnPressed.connect(lambda: self.setName(le_name.text()))
        formLayout.addRow("Name", le_name)

        # uid
        leUid = QLineEdit(str(self.uid))
        leUid.setReadOnly(True)
        formLayout.addRow("Uuid", leUid)

        # type
        leType = QLineEdit(self.__class__.__name__)
        leType.setReadOnly(True)
        formLayout.addRow("Type", leType)

        # pos
        le_pos = QLineEdit("{0} x {1}".format(self.pos().x(), self.pos().y()))
        formLayout.addRow("Pos", le_pos)

        pb = QPushButton("...")
        pb.clicked.connect(self.onChangeColor)
        formLayout.addRow("Color", pb)

        doc_lb = QLabel()
        doc_lb.setStyleSheet("background-color: black;")
        doc_lb.setText("Description")
        formLayout.addRow("", doc_lb)
        doc = QTextBrowser()
        doc.setOpenExternalLinks(True)
        doc.setHtml(self.description())
        formLayout.addRow("", doc)

    @staticmethod
    def category():
        return 'Common'

    @staticmethod
    def keywords():
        return []

    @staticmethod
    def description():
        return 'Can drag intersected nodes. You can also specify color and resize it.'
