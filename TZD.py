from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import serial
import ui_TZD
class TZDUIDIALOG (QDialog, ui_TZD.Ui_Dialog):
	def __init__(self, parent=None):
		super(TZDUIDIALOG,self).__init__(parent)
		self.setupUi(self)
		self.ser = serial.Serial()
		try:
			self.ser.port = 'COM1'
			self.ser.open()
			if self.ser.isOpen:
				self.comboBox.addItem("1")
		except serial.serialutil.SerialException:
			pass

		self.timer = QTimer()		
		self.timer.timeout.connect(self.dataHandler)
		self.worker = None
		self.btnReceive.clicked.connect(self.begin)
		self.btnEnd.clicked.connect(self.endHandler)

	
	def begin(self):
		self.timer.start(300)
	
	def endHandler(self):
		self.timer.stop()
		self.
		
	def dataHandler(self):
		pass
			 
			
		
if __name__== '__main__':
	import sys
	app = QApplication(sys.argv)
	w = TZDUIDIALOG()
	w.show()
	sys.exit(app.exec_())
		
		
		
	
	