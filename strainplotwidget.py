# -*- coding: utf-8 -*-
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np
class MplCanvas(FigureCanvas):
	def __init__(self):
		"""
			应变测量的图表
		"""
		self.fig = plt.figure()
		
		self.strain_widget_12 = self.fig.add_subplot(221)
		#self.strain_widget_12 = self.fig.add_axes([0.12,0.1,0.8,0.8])
		self.strain_widget_12.set_xlabel("Time(mm)")
		self.strain_widget_12.set_ylabel("Micro strain")
		self.strain_widget_12.grid(True)
		self.strain_widget_12.set_ylim([0, 0.5])  
		self.strain_widget_12.set_xlim([0, 100]) 
		
		self.strain0, = self.strain_widget_12.plot([0],[0],'r--')
		self.strain1, = self.strain_widget_12.plot([0],[0],'rs')
		self.strain2, = self.strain_widget_12.plot([0],[0],'rx')
		self.strain3, = self.strain_widget_12.plot([0],[0],'ro')
		
		self.strain4, = self.strain_widget_12.plot([0],[0],'b--')
		self.strain5, = self.strain_widget_12.plot([0],[0],'bs')
		self.strain6, = self.strain_widget_12.plot([0],[0],'bx')
		self.strain7, = self.strain_widget_12.plot([0],[0],'bo')
		
		self.strain8, = self.strain_widget_12.plot([0],[0],'k--')
		self.strain9, = self.strain_widget_12.plot([0],[0],'ks')
		self.strain10, = self.strain_widget_12.plot([0],[0],'kx')
		self.strain11, = self.strain_widget_12.plot([0],[0],'ko')
		self.strain_widget_12.set_autoscale_on = True
		"""
			轴向应变测量的图表
		"""
		self.strain_widget_axial = self.fig.add_subplot(222)
		self.strain_widget_axial.set_xlabel(u"Force (KN)")
		self.strain_widget_axial.set_ylabel(u"Micro strain")
		self.strain_widget_axial.grid(True)
		self.strain_widget_axial.set_ylim([0, 0.5])  
		self.strain_widget_axial.set_xlim([0, 10]) 
		self.strain_widget_axial.set_autoscale_on = True
		"""
			弯曲应变方位角
		"""
		self.strain_widget_theta = self.fig.add_subplot(223,polar=True) 
		#self.strain_widget_theta.rgrids(np.arange(0.5,2,0.5),angle=45)
		self.strain_widget_theta.grid(True)
		self.strain_widget_theta.set_theta_zero_location("N")
		self.strain_widget_theta.set_theta_direction(-1)
		self.strain_widget_theta.set_rmax(1.0)
		#self.strain_widget_theta.set_r
		#self.strain_widget_theta.set_rgrids(1.0)#, labels=None, angle=None, fmt=None, **kwargs)
		#self.strain_widget_axial.set_rmax(2.0)
		#self.strain_widget_axial.set_xlim([0, 10]) 
		#plt.plot(theta,2*np.ones_like(theta),lw=2)  
		#plt.plot(theta,theta/6,'--',lw=2)
		# self.strain_theta_A, = self.strain_widget_theta.plot([0],[0],'ro')
		# self.strain_theta_B, = self.strain_widget_theta.plot([0],[0],'b*')
		# self.strain_theta_C, = self.strain_widget_theta.plot([0],[0],'k--')
		self.strain_widget_theta.set_autoscale_on = True
		"""
			弯曲应变机器分量图
		"""
		self.strain_widget_bend = self.fig.add_subplot(224)
		self.strain_widget_bend.set_xlabel(u"Axial strain")
		self.strain_widget_bend.set_ylabel(u"Bending strain")
		self.strain_widget_bend.grid(True)
		self.strain_widget_bend.set_autoscale_on = True
		
		self.strain_widget_bend.set_ylim([0, 0.5])  
		self.strain_widget_bend.set_xlim([0, 10]) 
		self.strain_bending_A, = self.strain_widget_bend.plot([0],[0],'ro')
		self.strain_bending_B, = self.strain_widget_bend.plot([0],[0],'b*')
		self.strain_bending_C, = self.strain_widget_bend.plot([0],[0],'k--')
		
		FigureCanvas.__init__(self, self.fig)
		FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding,QSizePolicy.Expanding)
		FigureCanvas.updateGeometry(self)
		
		self.draw()
		
	def show_strains(self,args):
		if len(args == 1):
			#print(args.shape)
			xval = args.shape[0]
			self.strain0.set_xdata(range(xval))
			self.strain0.set_ydata(args[:,0])
			self.strain1.set_xdata(range(xval))
			self.strain1.set_ydata(args[:,1])
			self.strain2.set_xdata(range(xval))
			self.strain2.set_ydata(args[:,2])
			self.strain3.set_xdata(range(xval))
			self.strain3.set_ydata(args[:,3])
			
			self.strain4.set_xdata(range(xval))
			self.strain4.set_ydata(args[:,4])
			self.strain5.set_xdata(range(xval))
			self.strain5.set_ydata(args[:,5])
			self.strain6.set_xdata(range(xval))
			self.strain6.set_ydata(args[:,6])
			self.strain7.set_xdata(range(xval))
			self.strain7.set_ydata(args[:,7])
			
			self.strain8.set_xdata(range(xval))
			self.strain8.set_ydata(args[:,8])
			self.strain9.set_xdata(range(xval))
			self.strain9.set_ydata(args[:,9])
			self.strain10.set_xdata(range(xval))
			self.strain10.set_ydata(args[:,10])
			self.strain11.set_xdata(range(xval))
			self.strain11.set_ydata(args[:,11])
			
			maxx = np.amax(args)
			
			xliml,xlimu = self.strain_widget_12.get_xlim()
			yliml,ylimu = self.strain_widget_12.get_ylim()
			if xlimu < xval:
				self.strain_widget_12.set_xlim([0,xval * 1.5])
			if ylimu < maxx:
				self.strain_widget_12.set_ylim([0,maxx * 1.5])
			#self.strain_widget_12.draw_artist(self.flat0)
			# self.strain_widget_12.draw_artist(self.strain01)
			# self.strain_widget_12.draw_artist(self.flat2)
			
			self.strain_widget_12.autoscale_view()
			self.draw()
		else:
			raise ValueError("Wrong arguements")
		
	def show_strain_widget_axial(self,*args):
		try:
			array_forces, strain_axial = args
		except ValueError as e:
			print(e)
		print(len(self.strain_widget_axial.lines))
		for _ in range(len(self.strain_widget_axial.lines)):
			self.strain_widget_axial.lines.remove(self.strain_widget_axial.lines[0])
		# self.strain_A.set_xdata(array_forces)
		# self.strain_A.set_ydata(strain_axial[:,0])
		# print(array_forces,strain_axial)
		# self.strain_B.set_xdata(array_forces)
		# self.strain_B.set_ydata(strain_axial[:,1])
		# self.strain_C.set_xdata(array_forces)
		# self.strain_C.set_ydata(strain_axial[:,2])
		print(len(self.strain_widget_axial.lines))
		strain_A, = self.strain_widget_axial.plot(array_forces,strain_axial[:,0],\
												color = "r",linestyle = "solid", marker = "o")
		strain_B, = self.strain_widget_axial.plot(array_forces,strain_axial[:,1],\
												color = "b",linestyle = "--", marker = "s")
		strain_C, = self.strain_widget_axial.plot(array_forces,strain_axial[:,2],\
												color = "k",linestyle = "-.", marker = "d")
		
		max_y = np.amax(strain_axial)
		max_x = np.amax(array_forces)
		xliml,xlimu = self.strain_widget_axial.get_xlim()
		yliml,ylimu = self.strain_widget_axial.get_ylim()
		if xlimu < max_x:
			self.strain_widget_axial.set_xlim([0,max_x * 1.5])
		if ylimu < max_y:
			self.strain_widget_axial.set_ylim([0,max_y * 1.5])
		self.strain_widget_axial.autoscale_view()
		self.draw()
		
	def show_strain_bending(self,*args):
		try:
			axial_0strain, axial_180strain, strain_bend = args
		except ValueError as e:
			print(e)
		
		strain_axial = (axial_0strain + axial_180strain) / 2
		self.strain_bending_A.set_xdata(strain_axial[:,0])
		self.strain_bending_A.set_ydata(strain_bend[:,0])
		
		self.strain_bending_B.set_xdata(strain_axial[:,1])
		self.strain_bending_B.set_ydata(strain_bend[:,1])
		
		self.strain_bending_C.set_xdata(strain_axial[:,2])
		self.strain_bending_C.set_ydata(strain_bend[:,2])
		
		max_y = np.amax(strain_bend)
		max_x = np.amax(strain_axial)
		xliml,xlimu = self.strain_widget_bend.get_xlim()
		yliml,ylimu = self.strain_widget_bend.get_ylim()
		if xlimu < max_x:
			self.strain_widget_bend.set_xlim([0,max_x * 1.5])
		if ylimu < max_y:
			self.strain_widget_bend.set_ylim([0,max_y * 1.5])
		self.strain_widget_bend.autoscale_view()
		self.draw()
		
	def show_strain_angle(self, *args):
		try:
			angle_mc, = args
			print(angle_mc)
		except ValueError as e:
			print(e)
		r = np.array(np.arange(0, 1, 0.1))
		
		# for line in self.strain_widget_theta.lines:
			# self.strain_widget_theta.lines.remove(line)
		for ii in range(len(self.strain_widget_theta.lines)):
			self.strain_widget_theta.lines.remove(self.strain_widget_theta.lines[0])
		theta_A = np.zeros([r.size])
		theta_B = np.zeros([r.size])
		theta_C = np.zeros([r.size])
		
		theta_A[:] = angle_mc[0]
		
		theta_B[:] = angle_mc[1] 
		theta_C[:] = angle_mc[2] 
		
		strain_theta_A, = self.strain_widget_theta.plot(theta_A, r,'ro')
		strain_theta_B, = self.strain_widget_theta.plot(theta_B, r, 'bs')
		strain_theta_C, = self.strain_widget_theta.plot(theta_C, r, 'kd')
		# print(self.strain_theta_A)
		# self.strain_theta_A.set_thetadata(theta_A)
		# self.strain_theta_A.set_rdata(r)
		# self.strain_theta_B.set_xdata(theta_B)
		# self.strain_theta_B.set_ydata(r)
		# self.strain_theta_C.set_xdata(theta_C)
		# self.strain_theta_C.set_ydata(r)
		# print(theta_A,r)
		self.strain_widget_theta.autoscale_view()
		self.draw()
		
		
class StrainPlotWidget(QWidget):
	def __init__(self, parent = None):
		super(StrainPlotWidget,self).__init__(parent)
		self.canvas = MplCanvas()
		self.vbl = QVBoxLayout()
		self.vbl.addWidget(self.canvas)
		self.setLayout(self.vbl)
		
	def show_strains(self,args):
		self.canvas.show_strains(args)
		
	def show_strain_axial(self, *args):
		self.canvas.show_strain_widget_axial(*args)
		
	def show_strain_bending(self, *args):
		self.canvas.show_strain_bending(*args)
	
	def show_strain_angle(self, * args):
		self.canvas.show_strain_angle(*args)