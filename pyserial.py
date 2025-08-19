import serial
device = serial.Serial("COM6",9600)

led=0
mot=0



cad = "1,180"
device.write(cad.encode("ascii"))

device.close