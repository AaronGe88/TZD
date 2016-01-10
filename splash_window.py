# coding=utf-8
from PyQt5 import QtGui,QtCore
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys,time
class SplashScreen(QSplashScreen):
	def __init__(self):
		super(SplashScreen, self).__init__(QPixmap("./source/logo.png"))  #���������ͼƬ

     #Ч�� fade =1 ����   fade= 2  ������  t sleep ʱ�� ����
	def effect(self):
		self.setWindowOpacity(0)
		t = 0
		while t <= 50:
			newOpacity = self.windowOpacity() + 0.02     #���õ���
			if newOpacity > 1:
				break
			
			self.setWindowOpacity(newOpacity)
			self.show()
			t -= 1
			time.sleep(0.04)

		time.sleep(1)
		t = 0
		while t <= 50:
			newOpacity = self.windowOpacity() - 0.02         #���õ���
			if newOpacity < 0:
				break
			
			self.setWindowOpacity(newOpacity)
			t += 1
			time.sleep(0.04)