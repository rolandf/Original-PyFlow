# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:/GIT/nodes/PyFlow/FloatVector3InputWidget_ui.ui'
#
# Created: Sun Mar 11 18:19:07 2018
#      by: pyside2-uic 2.0.0 running on PySide2 5.6.0~a1
#
# WARNING! All changes made in this file will be lost!

from Qt import QtCompat, QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(271, 25)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout_4.setSpacing(5)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.dsbX = QtWidgets.QDoubleSpinBox(Form)
        self.dsbX.setMinimumSize(QtCore.QSize(0, 0))
        self.dsbX.setMaximumSize(QtCore.QSize(80, 16777215))
        self.dsbX.setObjectName("dsbX")
        self.horizontalLayout.addWidget(self.dsbX)
        self.horizontalLayout_4.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.dsbY = QtWidgets.QDoubleSpinBox(Form)
        self.dsbY.setMinimumSize(QtCore.QSize(0, 0))
        self.dsbY.setMaximumSize(QtCore.QSize(80, 16777215))
        self.dsbY.setObjectName("dsbY")
        self.horizontalLayout_2.addWidget(self.dsbY)
        self.horizontalLayout_4.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.dsbZ = QtWidgets.QDoubleSpinBox(Form)
        self.dsbZ.setMaximumSize(QtCore.QSize(80, 16777215))
        self.dsbZ.setObjectName("dsbZ")
        self.horizontalLayout_3.addWidget(self.dsbZ)
        self.horizontalLayout_4.addLayout(self.horizontalLayout_3)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.pbReset = QtWidgets.QPushButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pbReset.sizePolicy().hasHeightForWidth())
        self.pbReset.setSizePolicy(sizePolicy)
        self.pbReset.setMaximumSize(QtCore.QSize(25, 25))
        self.pbReset.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/resources/reset.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pbReset.setIcon(icon)
        self.pbReset.setObjectName("pbReset")
        self.horizontalLayout_4.addWidget(self.pbReset)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtCompat.translate("Form", "Form", None, -1))
        self.label.setText(QtCompat.translate("Form", "x", None, -1))
        self.label_2.setText(QtCompat.translate("Form", "y", None, -1))
        self.label_3.setText(QtCompat.translate("Form", "z", None, -1))
        self.pbReset.setToolTip(QtCompat.translate("Form", "Reset to defaults", None, -1))

from .. import nodes_res_rc

