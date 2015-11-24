from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from threading import Thread
from queue import Queue
import serial
import ui_TZD
import numpy as np
class TZDUIWIDGET (QDialog, ui_TZD.Ui_Form):
	def __init__(self, parent=None):
		super(TZDUIWIDGET,self).__init__(parent)
		self.setupUi(self)
		self.ser = serial.Serial()
		self.byte_queue = Queue()
		self.results = Queue()
		self.adcs = Queue()
		self.running = False
		try:
			self.ser.port = 'COM1'
			self.ser.open()
			if self.ser.isOpen:
				self.comboBox.addItem("1")
		except serial.serialutil.SerialException:
			pass

		self.timer = QTimer()		
		self.timer.timeout.connect(self.onTimer)
		self.btnReceive.clicked.connect(self.begin)
		self.btnEnd.clicked.connect(self.endHandler)
		#test 
		self.index = 0
	def begin(self):
		
		
		self.timer.start(50)
		# self.running = True
		# thread1 = Thread(target = self.read_from_serial,args=(self.byte_queue,))
		# thread1.start()
		# thread2 = Thread(target = self.find_effective_data,args=(self.byte_queue,self.results,))
		# thread2.start()
		# thread3 = Thread(target = self.data_process,args=(self.results,self.adcs))
		# thread3.start()
	def endHandler(self):
		self.timer.stop()
		#self.ser.close()
	
	def onTimer(self):
		# size = self.adcs.qsize()
		# for i in range(0,size):
			# self.adcs.get()
		self.index += 1
		line1 = []
		line2 = []
		line3 = []
		for ii in range(self.index):
			line1.append(ii * 2 + np.random.randn())
			line2.append(ii * 3 + np.random.randn())
			line3.append(ii * 4 + np.random.randn())
		self.widget.set_lines(line1,line2,line3)
			
		
	def read_from_serial(self,out_q):
		while self.running:
			b = self.ser.read()
			out_q.put(b)
		
	def find_effective_data(self,in_q,out_q2):
		while True:
			effective = []
			data = in_q.get()
			if data is not 0xFE:
				continue
			effective.append(data)
			data = in_q.get()
			if data is not 0x0C:
				continue
			for _ in range(0,40):
				data = in_q.get()
				effective.append(data)
			if effective[-1] is not 0xFF:
				continue
			out_q2.put(effective)
			in_q.task_done()
			
			
	# def worker(self,jobs,results):
		# while True:
			# block = job.get()
			# try:
				# result = dataProcess(block)
		
	def data_process(self,in_q2,out_q3):
		while True:
			data = in_q2.get()
			n = 0x00
			for i in range(1,38):
				n = n ^ data[i]
			if data[40] is not n:
				continue
			j = 0x00
			for i in range(1,38):
				j = j + data[i]
			t = data[39]
			t = t * 256 + data[38]
			if t is not j :
				continue
		adcs = []
		for j in range(2,39,3):
			i32 = data[j+2] 
			i32 = i32 << 8
			i32 = i32 + data[j+1];
			i32 = i32 << 8
			i32 = i32 + data[j];
			adcs.append(i32 / 8)
		out_q3.put(adcs)
		in_q2.task_done()
			
			
			
				
				
if __name__== '__main__':
	import sys
	app = QApplication(sys.argv)
	w = TZDUIWIDGET()
	w.show()
	sys.exit(app.exec_())
		
		
		
	
	