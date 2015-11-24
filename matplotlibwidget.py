# -*- coding: utf-8 -*-
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
 
class MplCanvas(FigureCanvas):
	def __init__(self):
		self.fig = plt.figure()
		self.flatax = self.fig.add_axes([0,0,10,1])
		self.flatax.set_xlabel("time")
		self.flatax.set_ylabel("flatness")
		FigureCanvas.__init__(self, self.fig)
		FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding,QSizePolicy.Expanding)
		FigureCanvas.updateGeometry(self)
		self.setlines([0],[0],[0])
	def setlines(self,*args):
		if len(args) is 3:
			self.flatax.plot(args[0],'r--',args[1],'gs',args[2],'bx')
			self.draw()
		else:
			raise ValueError("Wrong arguements")
		


class MatplotlibWidget(QWidget):
	def __init__(self, parent = None):
		super(MatplotlibWidget,self).__init__(parent)
		self.canvas = MplCanvas()
		self.vbl = QVBoxLayout()
		self.vbl.addWidget(self.canvas)
		self.setLayout(self.vbl)
		