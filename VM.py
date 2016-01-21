import serial
import random
index = 10000
ser = serial.Serial()
ser.baudrate = 9600
ser.port = 1
ser.open()
while index != 0:
	data = [254,]
	data.append(12)

	for ii in range(2,38):
		v = random.randint(0,25)
		data.append(v)
	n = 0
	for ii in range(1,38):
		n = n + data[ii]
		
	t39 = int(n / 256)
	t38 = n % 256
	data.append(t38)
	data.append(t39)

	del n
	t40 = 0
	for ii in range(1,38):
		t40 = t40 ^ data[ii]
	data.append(t40)
	data.append(255)
	print(data)
	byte_data = bytearray(data)
	ser.write(byte_data )
	index -= 1
	print (index)
ser.close()