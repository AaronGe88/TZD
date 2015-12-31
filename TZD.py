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
			self.ser.port = 'COM1'
			self.ser.open()
			if self.ser.isOpen:
				self.comboBox.addItem("1")
		except serial.serialutil.SerialException as e:
			print(str(e))
		
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
		#self.forces.setHeaderData(0,Qt.Horizontal,u"排序")  
		self.forces.setHeaderData(0,Qt.Horizontal,u"拉力(KN) 0") 
		self.forces.setHeaderData(1,Qt.Horizontal,u"拉力(KN) 180")
		self.tableView_force.setSelectionBehavior(QAbstractItemView.SelectRows);
		self.tableView_force.setModel(self.forces)
		self.tableView_force.resizeRowsToContents
		self.tableView_force.setSelectionBehavior(QAbstractItemView.SelectItems)
		try:
			self.sense = np.loadtxt("sense.txt")
			self.rcal = np.loadtxt("RCAL.txt")
		except ValueError as e:
			print(e)
			self.set_parameters(self)
			
		
		
		try:
			for ii,f in enumerate(self.read_forces()):
				self.forces.setItem(ii,0,QStandardItem(f[0]))
				self.forces.setItem(ii,1,QStandardItem(f[0]))
			
		except TypeError as e:
			self.forces.setItem(0,0,QStandardItem("0"))
			msbox = QMessageBox(QMessageBox.Warning,u"警告",str(e), QMessageBox.Cancel);  
			msbox.exec_()  
			
			
		self.index_force = 0.0
		self.index_angle = 0
		
		
	def read_forces(self):
		import csv
		try:
			with open("forces.csv") as f:
				f_cvs = csv.reader(f)
				for row in f_cvs:
					yield row
		except Exception as e:
			print(str(e))
				
			
			
	def on_btn_add_force(self):
		selection = self.tableView_force.selectionModel()
		#selected = selection.selectedIndexes()
		indexes = selection.selectedRows();
		if indexes:
			self.forces.insertRow(indexes[0].row(),QStandardItem());
		
	def on_btn_apply_force(self):
		import csv
		self.list_forces = []
		with open("forces.csv","w",newline = "") as f:
			f_csv = csv.writer(f,delimiter = ",")
			for ii in range(0,self.forces.rowCount()):
				f_csv.writerow([self.forces.item(ii).text(),])
				self.list_forces.append(float(self.forces.item(ii).text()))
		self.array_forces = np.array(self.list_forces)
		#0 和 180度 应变值
		self.strains_0degree = np.zeros([self.array_forces.size,12],dtype = np.float64)
		self.strains_180degree = np.zeros([self.array_forces.size,12],dtype = np.float64)
		
			
	def on_btn_begin(self):
			
		selection = self.tableView_force.selectionModel()
		#selected = selection.selectedIndexes()
		index = selection.currentIndex();
		print(index)
		try:
			self.index_force = float(self.forces.item(index.row(),index.column()).text())
			self.index_angle = 0 if index.column() == 0 else 180
			
		
		except IndexError as e:
			msbox = QMessageBox(QMessageBox.Warning,u"警告",u"请选择拉力", QMessageBox.Cancel);  
			msbox.exec_()  
		else:
			#u"打开串口"
			if not self.ser.isOpen():
				self.ser.open()
			self.timer.start(100)
			
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
			print('begin1',self.index_force,self.index_angle)
			self.is_zero = True
		

	def on_btn_end(self):
		self._running = False
		try:
			self.ser.close()
			self.timer.stop()
			print(self.index_force)
			if self.index_force == 0.0:
				self.mean_adcs0 = np.mean(self.cur_adcs,axis = 0)
				if np.isnan(self.mean_adcs0):
					msbox = QMessageBox(QMessageBox.Warning,u"警告",u"串口无信号/t请结束测量检测串口", QMessageBox.Cancel);  
					msbox.exec_()
					print(self.mean_adcs0)
		except Exception as e:
			print(str(e),139)
		else:
			print('stop')
		
		
			
		
	def onTimer(self):
		import copy	
		#if self.index_force == 0.0:
		size = self.adcs.qsize()
		list_adcs = []
		try:
			for ii in range(0,size):
				list_adcs.append(self.adcs.get())
			array_adcs = np.array(list_adcs)
			if  self.is_zero == True:
				self.cur_adcs = array_adcs
				self.is_zero = False
			else:
				#print(self.all_adcs.shape,array_adcs.shape)
				self.cur_adcs = np.concatenate((self.cur_adcs,array_adcs),axis = 0)
				#print(self.all_adcs)
		except Exception as e:
			print(e,163)
		if self.index_force != 0.0:
			try:
				self.cur_adcs_minused = self.cur_adcs - self.mean_adcs0
				#print(self.all_adcs_minused.shape)
			except ValueError as e:
				print(e)#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
				#msbox = QMessageBox(QMessageBox.Warning,u"警告",u"串口无信号/t请结束测量检测串口", QMessageBox.Cancel);  
				#msbox.exec_()  
				#self.on_btn_end()
			except AttributeError as e:
				print(e)
				#msbox = QMessageBox(QMessageBox.Warning,u"警告",u"请首先测试0拉力", QMessageBox.Cancel);  
				#msbox.exec_() 
				#self.on_btn_end()
				
				
			if self.sense.size == 12 and self.rcal.size ==12 :
				try:
					this_strain = self.cur_adcs_minused / self.rcal / self.sense
					self.plot_strains(this_strain)
					mean_strain = np.mean(this_strain,axis = 0)
					print(self.mean_strain)
				except AttributeError as e:
					print(e)
				except ValueError as e:
					print(e)
				
		
	def plot_strains(self,strain):
		self.widget_strain.set_lines(strain)
		
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
				print('data error 1')
				continue
			j = 0
			for i in range(1,38):
				j = j + data[i]
			t = data[39]
			t = t * 256 + data[38]
			if t != j :
				print(t,'-',j)
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
		
		
		
	
	