from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import ui_set_parameters
from TZD import TZDUIWIDGET
		
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
		self.define_varibles()
		self.pushButton.clicked.connect(self.define_varibles)
		
	def define_varibles(self):
		if self.checkBox.isChecked():
			value = 0
			for plane in ['A','B','C']:
				for ii in range(1,5):
					try:
						name = 'sen_'+plane+str(ii)
						
						value = float(self.lineEdit_all_Sen.text())
						#value = float()
						self.sen_dict[name] = value
					except:
						print('error')
			for name in vars(self):
				if name.startswith('lineEdit') and name.endswith('Sen'):
					editer = getattr(self,name)
					editer.setText(str(value))
		else:
			for name in vars(self):
				if name.startswith('lineEdit'):
					if name.endswith('Sen'):
						attr_name = "sen_"
						name_array = name.split('_')
						name_index = name_array[0][-1]
						try:
							index = int(name_index)
						except:
							continue
						name_plane = name_array[0][-2]
						attr_name += name_plane + name_index
						try:
							editer = getattr(self,name)
							value_text = editer.text()
							value = float(value_text)
							self.sen_dict[attr_name] = value
						except:
							continue
					else:
						name_index = name[-1]

						try:
							int(name_index)
						except:
							continue
						name_plane = name[-2]
						attr_name = 'cal_' + name_plane + name_index
						
						try:
							editer = getattr(self,name)
							value_text = editer.text()
							value = float(value_text)
							self.cal_dict[attr_name] = value
						except:
							continue		
		
			
					
					
					
# if __name__== '__main__':
	# import sys
	# app = QApplication(sys.argv)
	# w = Set_Parameters_Dialog()
	# w.show()
	# sys.exit(app.exec_())