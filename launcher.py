from Qt.QtWidgets import QApplication,QStyleFactory
import sys
from os import path
from PyFlow.App import PyFlow
#from stylesheet import editableStyleSheet
FILE_DIR = path.dirname(__file__)

SETTINGS_PATH = FILE_DIR + "PyFlow/appConfig.ini"


app = QApplication(sys.argv)


app.setStyle(QStyleFactory.create("plastique"))



#style = editableStyleSheet()
#app.setStyleSheet( style.getStyleSheet() )

instance = PyFlow.instance()
app.setActiveWindow(instance)
instance.show()

try:
    sys.exit(app.exec_())
except Exception as e:
    print(e)
