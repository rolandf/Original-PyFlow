from Qt import QtWidgets
from Qt import QtCore

from widgets.pc_HueSlider import pc_HueSlider,pc_GradientSlider

if __name__ == '__main__':
	import sys
	sys.path.append("..")
	import stylesheet
else:
	from .. import stylesheet


class StyleSheetEditor(QtWidgets.QWidget):
	"""Style Sheet Editor"""
	Updated = QtCore.Signal()
	def __init__(self,parent=None):
		super(StyleSheetEditor, self).__init__(parent)
		self.style = stylesheet.editableStyleSheet()

		self.setLayout(QtWidgets.QVBoxLayout ())
		self.layout().addWidget(QtWidgets.QLabel("Main Color Hue"))
		self.hueSat = pc_HueSlider(self)
		self.hueSat.valueChanged.connect(self.updateHue)        
		self.layout().addWidget(self.hueSat)
		self.bgColor = pc_GradientSlider(self)
		self.bgColor.setValue(0.1960784313725490196078431372549)
		self.bgColor.valueChanged.connect(self.updateBg)
		self.layout().addWidget(self.bgColor)

		self.setColor(self.style.ORANGE1)
	def setColor(self,color):
		self.hueSat.setColor(color)
	def hue(self):
		return self.hueSat.value()
	def getStyleSheet(self):
		return self.style.getStyleSheet()
	def updateHue(self,value):
		self.style.setHue(self.hueSat.value())
		self.Updated.emit()
	def updateBg(self,value):
		self.style.setBg(self.bgColor.value())
		
		self.Updated.emit()
if __name__ == '__main__':
	import sys
	app = QtWidgets.QApplication(sys.argv)

	a = StyleSheetEditor()
	
	def update():
		print a.bgColor.value()
		app.setStyleSheet( a.getStyleSheet() )


	app.setStyleSheet( a.getStyleSheet() )
	a.Updated.connect(update)
	a.show()

	sys.exit(app.exec_())	