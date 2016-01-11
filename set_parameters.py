from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import ui_set_parameters
from TZD import TZDUIWIDGET
import numpy as np
class Set_Parameters_Dialog(QDialog, ui_set_parameters.Ui_Dialog):
	def __init__(self,parent=None):
		super(Set_Parameters_Dialog,self).__init__(parent)
		self.mother = parent
		self.setupUi(self)
		for name in vars(self):
			if name.startswith('lineEdit'):
				editer = getattr(self,name)
				editer.setText('0')
		self.sen_dict = {}
		self.cal_dict = {}
		try:
			self.sense = np.loadtxt("sense.txt")
			self.rcal = np.loadtxt("RCAL.txt")
		except Exception as e:
			self.sense = np.zeros([12,1])
			self.rcal = np.zeros([12,1])
		#self.define_varibles()
		self.pushButton.clicked.connect(self.define_varibles)
		
		for ii in range(12):
			cal = str(self.rcal[ii])
			sen = str(self.sense[ii])
			if int(ii / 4) == 0:
				plate = "A"
			
			elif int(ii / 4) == 1:
				plate = "B"
				
			else:
				plate = "C"
			try:
				line_edit = "".join(["lineEdit",plate,str(ii % 4 + 1)])
				cmd = "".join(["self.",line_edit,".setText(str(",cal,"))"])
				#print (cmd)
				eval (cmd) #"for b in birds: print b" in globals, locals
				line_edit = "".join(["lineEdit",plate,str(ii%4 + 1),"_Sen"])
				cmd = "".join(["self.",line_edit,".setText(str(",sen,"))"])
				eval (cmd)
			except SyntaxError as e:
				#print(e)
				pass
		
	def define_varibles(self):
		for ii in range(12):
			if int(ii / 4) == 0:
				if ii % 4 == 0:
					self.rcal[ii] = self.lineEditA1.text()
					self.sense[ii] = self.lineEditA1_Sen.text()
					#print (self.rcal[ii])
				elif ii % 4 == 1:
					self.rcal[ii] = self.lineEditA2.text()
					self.sense[ii] = self.lineEditA2_Sen.text()
				elif ii % 4 == 2:
					self.rcal[ii] = self.lineEditA3.text()
					self.sense[ii] = self.lineEditA3_Sen.text()
				else: 
					self.rcal[ii] = self.lineEditA4.text()
					self.sense[ii] = self.lineEditA4_Sen.text()
					
			elif int(ii / 4) == 1:
				if ii % 4 == 0:
					self.rcal[ii] = self.lineEditB1.text()
					self.sense[ii] = self.lineEditB1_Sen.text()
				elif ii % 4 == 1:
					self.rcal[ii] = self.lineEditB2.text()
					self.sense[ii] = self.lineEditB2_Sen.text()
				elif ii % 4 == 2:
					self.rcal[ii] = self.lineEditB3.text()
					self.sense[ii] = self.lineEditB3_Sen.text()
				
				else: 
					self.rcal[ii] = self.lineEditB4.text()
					self.sense[ii] = self.lineEditB4_Sen.text()
				
			else:
				if ii % 4 == 0:
					self.rcal[ii] = self.lineEditC1.text()
					self.sense[ii] = self.lineEditC1_Sen.text()
				elif ii % 4 == 1:
					self.rcal[ii] = self.lineEditC2.text()
					self.sense[ii] = self.lineEditC2_Sen.text()
				elif ii % 4 == 2:
					self.rcal[ii] = self.lineEditC3.text()
					self.sense[ii] = self.lineEditC3_Sen.text()
				
				else: 
					self.rcal[ii] = self.lineEditC4.text()
					self.sense[ii] = self.lineEditC4_Sen.text()
			#print(ii,self.rcal[ii])
			
					
					
					
# if __name__== '__main__':
	# import sys
	# app = QApplication(sys.argv)
	# w = Set_Parameters_Dialog()
	# w.show()
	# sys.exit(app.exec_())