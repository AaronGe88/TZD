# -*- coding: utf-8 -*-
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np
class MplCanvas(FigureCanvas):
	def __init__(self):
		self.fig = plt.figure()
		self.flatax = self.fig.add_axes([0.12,0.1,0.8,0.8])
		self.flatax.set_xlabel("Time(mm)")
		self.flatax.set_ylabel("Strain")
		self.flatax.grid(True)
		self.flatax.set_ylim([0, 0.5])  
		self.flatax.set_xlim([0, 100]) 
		FigureCanvas.__init__(self, self.fig)
		FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding,QSizePolicy.Expanding)
		FigureCanvas.updateGeometry(self)
		
		self.flat0, = self.flatax.plot([0],[0],'r--')
		self.flat1, = self.flatax.plot([0],[0],'rs')
		self.flat2, = self.flatax.plot([0],[0],'rx')
		self.flat3, = self.flatax.plot([0],[0],'ro')
		
		self.flat4, = self.flatax.plot([0],[0],'b--')
		self.flat5, = self.flatax.plot([0],[0],'bs')
		self.flat6, = self.flatax.plot([0],[0],'bx')
		self.flat7, = self.flatax.plot([0],[0],'bo')
		
		self.flat8, = self.flatax.plot([0],[0],'k--')
		self.flat9, = self.flatax.plot([0],[0],'ks')
		self.flat10, = self.flatax.plot([0],[0],'kx')
		self.flat11, = self.flatax.plot([0],[0],'ko')
		
		
		self.draw()
		
	def set_lines(self,args):
		if len(args == 1):
			print(args.shape)
			xval = args.shape[0]
			self.flat0.set_xdata(range(xval))
			self.flat0.set_ydata(args[:,0])
			self.flat1.set_xdata(range(xval))
			self.flat1.set_ydata(args[:,1])
			self.flat2.set_xdata(range(xval))
			self.flat2.set_ydata(args[:,2])
			self.flat3.set_xdata(range(xval))
			self.flat3.set_ydata(args[:,3])
			
			self.flat4.set_xdata(range(xval))
			self.flat4.set_ydata(args[:,4])
			self.flat5.set_xdata(range(xval))
			self.flat5.set_ydata(args[:,5])
			self.flat6.set_xdata(range(xval))
			self.flat6.set_ydata(args[:,6])
			self.flat7.set_xdata(range(xval))
			self.flat7.set_ydata(args[:,7])
			
			self.flat8.set_xdata(range(xval))
			self.flat8.set_ydata(args[:,8])
			self.flat9.set_xdata(range(xval))
			self.flat9.set_ydata(args[:,9])
			self.flat10.set_xdata(range(xval))
			self.flat10.set_ydata(args[:,10])
			self.flat11.set_xdata(range(xval))
			self.flat11.set_ydata(args[:,11])
			
			maxx = np.amax(args)
			
			xliml,xlimu = self.flatax.get_xlim()
			yliml,ylimu = self.flatax.get_ylim()
			if xlimu < xval:
				self.flatax.set_xlim([0,xval * 1.5])
			if ylimu < maxx:
				self.flatax.set_ylim([0,maxx * 1.5])
			#self.flatax.draw_artist(self.flat0)
			self.flatax.draw_artist(self.flat1)
			self.flatax.draw_artist(self.flat2)
			
			self.flatax.autoscale_view()
			self.draw()
		else:
			raise ValueError("Wrong arguements")
		

class StrainPlotWidget(QWidget):
	def __init__(self, parent = None):
		super(StrainPlotWidget,self).__init__(parent)
		self.canvas = MplCanvas()
		self.vbl = QVBoxLayout()
		self.vbl.addWidget(self.canvas)
		self.setLayout(self.vbl)
	def set_lines(self,args):
		self.canvas.set_lines(args)