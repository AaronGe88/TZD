# -*- coding: utf-8 -*-
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
 
class MplCanvas(FigureCanvas):
	def __init__(self):
		self.fig = plt.figure()
		self.flatax = self.fig.add_axes([0.1,0.1,1,1])
		self.flatax.set_xlabel("time")
		self.flatax.set_ylabel("flatness")
		self.flatax.grid(True)
		self.flatax.set_ylim([0, 200])  
		self.flatax.set_xlim([0, 200]) 
		FigureCanvas.__init__(self, self.fig)
		FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding,QSizePolicy.Expanding)
		FigureCanvas.updateGeometry(self)
		
		self.flat0, = self.flatax.plot([0],[0],'r--')
		self.flat1, = self.flatax.plot([0],[0],'gs')
		self.flat2, = self.flatax.plot([0],[0],'bx')
		self.draw()
		
	def set_lines(self,*args):
		if len(args) is 3:
			length = len(args[0])
			self.flat0.set_xdata(range(length))
			self.flat0.set_ydata(args[0])
			self.flat1.set_xdata(range(length))
			self.flat1.set_ydata(args[1])
			self.flat2.set_xdata(range(length))
			self.flat2.set_ydata(args[2])
			max0 = max(args[0])
			max1 = max(args[1])
			max2 = max(args[2])
			maxx = max([max0,max1,max2])
			xliml,xlimu = self.flatax.get_xlim()
			yliml,ylimu = self.flatax.get_ylim()
			if xlimu < length:
				self.flatax.set_xlim([0,length * 1.5])
			if ylimu < maxx:
				self.flatax.set_ylim([0,maxx * 1.5])
			#self.flatax.draw_artist(self.flat0)
			self.flatax.draw_artist(self.flat1)
			self.flatax.draw_artist(self.flat2)
			
			self.flatax.autoscale_view()
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
	def set_lines(self,*args):
		self.canvas.set_lines(*args)