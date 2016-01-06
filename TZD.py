# coding=utf-8
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from threading import Thread
from queue import Queue
import serial
import ui_TZD
import numpy as np

class TZDUIWIDGET (QMainWindow, ui_TZD.Ui_Form):
	def __init__(self, parent=None):
		#GUI
		super(TZDUIWIDGET,self).__init__(parent)
		self.setupUi(self)
		#u"串口"
		self.ser = serial.Serial()
		
		#u"测量标识"
		self._running = False
		
		try:
			self.ser.port = 'COM3'
			self.ser.open()
			if self.ser.isOpen:
				self.comboBox.addItem("3")
		except serial.serialutil.SerialException as e:
			#print(str(e))
			self.textBrowser_info.setText(str(e))
		
		#u"计时器"
		self.timer = QTimer()		
		self.timer.timeout.connect(self.onTimer)
		
		#u"开始测量"
		self.btnReceive.clicked.connect(self.on_btn_begin)
		#u"结束测量"
		self.btnEnd.clicked.connect(self.on_btn_end)
		#u"设置参数"
		self.btnSetParameters.clicked.connect(self.set_parameters)
		#self.btnZero.clicked.connect(self.on_btn_zeros)
		#u"添加测量力"
		self.btn_add_force.clicked.connect(self.on_btn_add_force)
		self.btn_apply_force.clicked.connect(self.on_btn_apply_force)
		
		self.forces =  QStandardItemModel(self.tableView_force)
		self.forces.setColumnCount(2)
	 
		self.forces.setHeaderData(0,Qt.Horizontal,u"拉力(KN) 0") 
		self.forces.setHeaderData(1,Qt.Horizontal,u"拉力(KN) 180")
		self.tableView_force.setSelectionBehavior(QAbstractItemView.SelectRows)
		self.tableView_force.setModel(self.forces)
		self.tableView_force.resizeRowsToContents
		self.tableView_force.setSelectionBehavior(QAbstractItemView.SelectItems)
		
		
		try:
			self.sense = np.loadtxt("sense.txt")
			self.rcal = np.loadtxt("RCAL.txt")
		except ValueError as e:
			#print(e)
			self.set_parameters(self)
			
		
		
		try:
			for ii,f in enumerate(self.read_forces()):
				self.forces.setItem(ii,0,QStandardItem(f[0]))
				self.forces.setItem(ii,1,QStandardItem(f[0]))
			
		except TypeError as e:
			self.forces.setItem(0,0,QStandardItem("0"))
			msbox = QMessageBox(QMessageBox.Warning,u"警告",str(e), QMessageBox.Cancel);  
			msbox.exec_()
			msbox.destroy()
			
		self.index_row = 0
		self.index_force = 0.0
		self.index_angle = 0
		self.textBrowser_info.setText(u"请首先应用拉力测试数据")
	
	def read_forces(self):
		import csv
		try:
			with open("forces.csv") as f:
				f_cvs = csv.reader(f)
				for row in f_cvs:
					yield row
		except Exception as e:
			#print(str(e))
			self.textBrowser_info.setText(str(e))
				
			
			
	def on_btn_add_force(self):
		selection = self.tableView_force.selectionModel()
		#selected = selection.selectedIndexes()
		indexes = selection.selectedRows();
		if indexes:
			self.forces.insertRow(indexes[0].row(),QStandardItem());
		
	def on_btn_apply_force(self):
		import csv
		list_forces = []
		with open("forces.csv","w",newline = "") as f:
			f_csv = csv.writer(f,delimiter = ",")
			for ii in range(0,self.forces.rowCount()):
				f_csv.writerow([self.forces.item(ii).text(),])
				list_forces.append(float(self.forces.item(ii).text()))
		self.array_forces = np.array(list_forces)
		#0 和 180度 应变值
		self.strains_0degree = np.zeros([self.array_forces.size,12],dtype = np.float64)
		self.strains_180degree = np.zeros([self.array_forces.size,12],dtype = np.float64)
		
		#轴向应变 a
		self.strain_0axial = np.zeros([self.array_forces.size,3],dtype = np.float64)
		self.strain_180axial = np.zeros([self.array_forces.size,3],dtype = np.float64)
		
		#弯曲应变 B_mc, B_sp
		self.strain_bend_mc = np.zeros([self.array_forces.size,3],dtype = np.float64)
		self.strain_bend_sp = np.zeros([self.array_forces.size,3],dtype = np.float64)
		
		#方位角
		self.strain_theta_mc = np.zeros([self.array_forces.size,3],dtype = np.float64)
		self.strain_theta_sp = np.zeros([self.array_forces.size,3],dtype = np.float64)
		
		self.textBrowser_info.setText(u"数据确认成功")
		
		
	def on_btn_begin(self):
	
		selection = self.tableView_force.selectionModel()
		#selected = selection.selectedIndexes()
		index = selection.currentIndex();
		try:
			self.index_row = index.row()
			self.index_force = float(self.forces.item(index.row(),index.column()).text())
			self.index_angle = 0 if index.column() == 0 else 180
			
		except IndexError as e:
			#msbox = QMessageBox(QMessageBox.Warning,u"警告",u"请选择拉力", QMessageBox.Cancel);  
			#msbox.exec_()  
			self.textBrowser_info.setText(u"请选择拉力")
		else:
			#提示当前测量数据
			str_tip = "当前拉力: {0}, 测量角度： {1}".format(self.index_force,self.index_angle)
			#uni_tip = str_tip.encode("utf-8")
			self.textBrowser_info.setText(str_tip)
			
			#u"打开串口"
			if not self.ser.isOpen():
				self.ser.open()
			self.timer.start(500)
			
			self.byte_queue = Queue()
			self.results = Queue()
			self.adcs = Queue()
			self._running = True
			thread1 = Thread(target = self.read_from_serial,args=(self.byte_queue,))
			thread2 = Thread(target = self.find_effective_data,args=(self.byte_queue,self.results,))
			thread3 = Thread(target = self.data_process,args=(self.results,self.adcs))
				#thread1 = Thread(target = self.read_from_serial,args=(self.byte_queue,))
			thread1.setDaemon(True)
			thread2.setDaemon(True)
			thread3.setDaemon(True)
			thread1.start()
				#thread2 = Thread(target = self.find_effective_data,args=(self.byte_queue,self.results,))
			thread2.start()
				#thread3 = Thread(target = self.data_process,args=(self.results,self.adcs))
			thread3.start()
			self.is_zero = True
		

	def on_btn_end(self):
		self._running = False
		try:
			self.ser.close()
			self.timer.stop()
		except Exception as e:
			self.textBrowser_info.setText(str(e))
		else:
			self.textBrowser_info.setText(u"串口已关闭！\n计时器已关闭")
		if self.index_force == 0.0:
			self.mean_adcs0 = np.mean(self.cur_adcs,axis = 0) 
			#print(self.mean_adcs0)
			try:
				if np.isnan(self.mean_adcs0):
						#msbox = QMessageBox(QMessageBox.Warning,u"警告",u"", QMessageBox.Cancel);  
						#msbox.exec_()
						#print(self.mean_adcs0)
					self.textBrowser_info.setText(u"串口无信号\n请结束测量检测串口")
			except ValueError as e:
				self.textBrowser_info.setText(u"串口连接正常")
				if not np.isnan(self.mean_adcs0.any()):
					str_tip = "".join([u"0点设置成功\n",str(self.mean_adcs0)])
					self.textBrowser_info.setText(str_tip)
		else:
			try:
				mean_strain = np.mean(self.this_strain,axis = 0)
				#三个平面的轴向应变
				aA = np.mean(mean_strain[0:4])
				aB = np.mean(mean_strain[4:8])
				aC = np.mean(mean_strain[8:12])
				if self.is_serial_valid == False:
					tip = "".join([u"串口无信号\n请结束测量检测串口"])
				else:
					if self.index_angle == .0:
						self.strains_0degree[self.index_row,:] = mean_strain
						self.strain_0axial[self.index_row,:] = np.array([aA,aB,aC])
						#print(self.strain_0axial)
						tip = "".join([u"测试成功\n",str(self.strains_0degree)])
					else:
						
						self.strains_180degree[self.index_row,:] = mean_strain
						self.strain_180axial[self.index_row,:] = np.array([aA,aB,aC])
						#print(self.strain_180axial)
						tip = "".join([u"测试成功\n",str(self.strains_180degree)])
				self.textBrowser_info.setText(tip)
			except AttributeError as e:
				self.textBrowser_info.setText(u"请先点击应用")
				self.textBrowser_info.setText(str(e))
				
			try:
				if self.strain_0axial[self.index_row,0] != 0 and \
					self.strain_180axial[self.index_row,0] != 0:
					strain_axial = (self.strain_0axial + self.strain_180axial) / 2
				elif self.strain_180axial[self.index_row,0] != 0:
					strain_axial = self.strain_180axial
				else :
					strain_axial = self.strain_0axial
				print(strain_axial.shape)
			except Exception as e:
				print (e)
			
			try:
				self.plot_strain_axial(self.array_forces,strain_axial)
			except Exception as e:
				print(e)
				
			try:
				if self.strain_0axial[self.index_row,0] != 0.0 and\
					self.strain_180axial[self.index_row,0] != 0.0:
					#三个截面
					for ii in range(0,3):
						#弯曲应变 0度
						b_0  = self.strains_0degree[self.index_row,4*ii:4*ii+4] - \
							self.strain_0axial[self.index_row,ii] 
						print(self.strains_0degree[self.index_row,4*ii:4*ii+4])
						#弯曲应变 180度
						b_180 = self.strains_180degree[self.index_row,4*ii:4*ii+4] - \
							self.strain_180axial[self.index_row,ii]
						#机器分量
						b_mc = (b_0 - b_180) / 2
						#试件分量
						b_sp = (b_0 + b_180) / 2
						self.strain_bend_mc[self.index_row,ii] = np.sqrt(np.sum(b_mc ** 2) / 2)
						self.strain_bend_sp[self.index_row,ii] = np.sqrt(np.sum(b_sp ** 2) / 2)
						#方位角
						B_mc_float = np.sum(b_mc ** 2) / 2
						print("B_mc_float\n",B_mc_float)
						B_sp_float = np.sum(b_mc ** 2) / 2
						#P71 方位角机器分量
						theta_0 = (b_mc[1] - b_mc[3]) / \
							np.fabs(b_mc[1] - b_mc[3]) * \
							np.arccos(b_mc[0] / B_mc_float)
						theta_1 = (b_mc[2] - b_mc[0]) / \
							np.fabs(b_mc[2] - b_mc[0]) * \
							np.arccos(b_mc[1] / B_mc_float) + np.pi / 2
							
						theta_2 = (b_mc[3] - b_mc[1]) / \
							np.fabs(b_mc[3] - b_mc[1]) * \
							np.arccos(b_mc[2] / B_mc_float) + np.pi
						
						theta_3 = (b_mc[0] - b_mc[2]) / \
							np.fabs(b_mc[0] - b_mc[2]) * \
							np.arccos(b_mc[3] / B_mc_float) + 1.5 * np.pi
						theta_mc = np.sum([theta_0, theta_1, theta_2, theta_3]) / 4
						
						self.strain_theta_mc[self.index_row, ii] = theta_mc
						
						#P71 方位角机试件分量
						theta_0 = (b_sp[1] - b_sp[3]) / \
							np.fabs(b_sp[1] - b_sp[3]) * \
							np.arccos(b_sp[0] / B_sp_float)
						theta_1 = (b_sp[2] - b_sp[0]) / \
							np.fabs(b_sp[2] - b_sp[0]) * \
							np.arccos(b_sp[1] / B_sp_float) + np.pi / 2
							
						theta_2 = (b_sp[3] - b_sp[1]) / \
							np.fabs(b_sp[3] - b_sp[1]) * \
							np.arccos(b_sp[2] / B_sp_float) + np.pi
						
						theta_3 = (b_sp[0] - b_sp[3]) / \
							np.fabs(b_sp[0] - b_sp[3]) * \
							np.arccos(b_sp[3] / B_sp_float) + 1.5 * np.pi
						theta_sp = np.sum([theta_0, theta_1, theta_2, theta_3]) / 4
						self.strain_theta_sp[self.index_row, ii] = theta_sp
						
					#print(self.strain_bend_mc,"\n",self.strain_bend_sp)
					#绘制弯曲应变机器分量
					self.widget_strain.show_strain_bending(self.strain_0axial,\
															self.strain_180axial,\
															self.strain_bend_mc)
					#绘制方位角机器分量
					#print("theta MC\n",self.strain_theta_mc[self.index_row,:])
					self.widget_strain.show_strain_angle(self.strain_theta_mc[self.index_row,:])
														
			except AttributeError as e:
				#print(e)
				tip = "".join([str(e),u"请先点击应用"]) 
				self.textBrowser_info.setText(tip)
			
		
	def onTimer(self):
		import copy	
		#if self.index_force == 0.0:
		size = self.adcs.qsize()
		list_adcs = []
		try:
			for ii in range(0,size):
				list_adcs.append(self.adcs.get())
			array_adcs = np.array(list_adcs)
			#print(array_adcs,"\n array_adcs")
			if  self.is_zero == True:
				self.cur_adcs = array_adcs
				self.is_zero = False
			else:
				
				self.cur_adcs = np.concatenate((self.cur_adcs,array_adcs),axis = 0)
				#print("cur_adcs\n",self.cur_adcs)
		except Exception as e:
			self.textBrowser_info.setText(str(e))
			
		if self.index_force != 0.0:
			try:
				self.cur_adcs_minused = self.cur_adcs - self.mean_adcs0
				#print(self.mean_adcs0)
				#print(self.all_adcs_minused.shape)
			except ValueError as e:
				#msbox = QMessageBox(QMessageBox.Warning,u"警告",u"串口无信号/t请结束测量检测串口", QMessageBox.Cancel);  
				#msbox.exec_()  
				#self.on_btn_end()
				self.is_serial_valid = False
				self.textBrowser_info.setText(u"串口无信号\n请重试")
			except AttributeError as e:
				#print(e)
				#msbox = QMessageBox(QMessageBox.Warning,u"警告",u"请首先测试0拉力", QMessageBox.Cancel);  
				#msbox.exec_() 
				#self.on_btn_end()
				self.textBrowser_info.setText(u"请首先测试0拉力")
				self.is_serial_valid = False
			else:
				self.is_serial_valid = True
			if self.sense.size == 12 and self.rcal.size ==12 :
				try:
					self.this_strain = self.cur_adcs_minused / self.rcal / self.sense
					self.plot_strains(self.this_strain)
				except AttributeError as e:
					tip = "".join([u"请首先测试0拉力\n",str(e)])
					self.textBrowser_info.setText(tip)
				except ValueError as e:
					self.textBrowser_info.setText(str(e))
			
				
		
	def plot_strains(self,strain):
		self.widget_strain.show_strains(strain)
	
	def plot_strain_axial(self,*strain_axial):
		self.widget_strain.show_strain_axial(*strain_axial)
		
	def read_from_serial(self,out_q):
		while self._running != 0:
			b = self.ser.read()
			try:
				out_q.put(hex(ord(b)))
			except serial.SerialException as e:
				print(str(e))
			
		
	def find_effective_data(self,in_q,out_q2):
		while True:
			effective = []
			#data = hex(eval(in_q.get()))
			data = int(in_q.get(),16)
			
			if data != 0xfe:
				#print('data error FE')
				continue
			effective.append(data)
			#print(data,1)
			data = int(in_q.get(),16)
			#print(data)
			if data != 0x0C:
				#print('data error 0C')
				continue
			effective.append(data)
			#print(data,2)
			for _ in range(0,40):
				data = int(in_q.get(),16)
				#print(data)
				effective.append(data)
				#print(data,'2~41')
			if effective[-1] != 0xFF:
				#print('data error FF')
				continue
			out_q2.put(effective)
			in_q.task_done()
			
		
	def data_process(self,in_q2,out_q3):
		while True:
			data = in_q2.get()
			n = 0
			for i in range(1,38):
				n = n ^ data[i]
			#print(n)
			#print(data[40])
			if data[40] != n:
				continue
			j = 0
			for i in range(1,38):
				j = j + data[i]
			t = data[39]
			t = t * 256 + data[38]
			if t != j :
				#print(t,'-',j)
				continue
			
			adcs = []
			for j in range(2,38,3):
				i32 = data[j+2] 
				i32 = i32 << 8
				i32 = i32 + data[j+1];
				i32 = i32 << 8
				i32 = i32 + data[j];
				adcs.append(i32 / 8)
			out_q3.put(adcs)
			in_q2.task_done()
			
	def set_parameters(self):
		from set_parameters import Set_Parameters_Dialog
		dlg = Set_Parameters_Dialog(parent = self)
		if dlg.exec_():
			self.sense = dlg.array_sense
			self.cal = dlg.array_cal
		dlg.destroy()
		
		
			
				
				
if __name__== '__main__':
	import sys
	app = QApplication(sys.argv)
	w = TZDUIWIDGET()
	w.show()
	sys.exit(app.exec_())
		
		
		
	
	