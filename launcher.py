from Qt.QtWidgets import QApplication,QStyleFactory
from Qt import QtGui
from Qt import QtCore
import sys
from os import path
from PyFlow.App import PyFlow

FILE_DIR = path.dirname(__file__)

SETTINGS_PATH = FILE_DIR + "PyFlow/appConfig.ini"


app = QApplication(sys.argv)


app.setStyle(QStyleFactory.create("plastique"))
app.setStyleSheet("darkorange.stylesheet")


file = QtCore.QFile("darkorange.stylesheet")
file.open(QtCore.QIODevice.ReadOnly|QtCore.QIODevice.Text)
sty =  str(file.readAll())
file.close()

app.setStyle(QStyleFactory.create("plastique"))
app.setStyleSheet(sty)

instance = PyFlow.instance()
app.setActiveWindow(instance)
instance.show()

try:
    sys.exit(app.exec_())
except Exception as e:
    print(e)
