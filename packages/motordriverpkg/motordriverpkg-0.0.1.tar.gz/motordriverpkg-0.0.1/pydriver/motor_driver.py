import serial
import struct

class cmd: 
        ADRESS = 120    #0 causes problem need to rectify it
        MOTORSPEED = 0
        GETM1M2ENC = 1
        
class Motordriver:

    def __init__(self, comport, rate) :
        self.comport = comport
        self.rate = rate

    
    def sendcommand(self,command):
        self.port.write(command)

    def motorspeed(self,Leftspeed,Rightspeed):
        self.sendcommand(bytearray([cmd.ADRESS,cmd.MOTORSPEED,Leftspeed,Rightspeed]))
        read=self.port.read(4)
       
    def readencoder(self):
        self.sendcommand(bytearray([cmd.ADRESS,cmd.GETM1M2ENC,0,0]))
        read = self.port.read(8)
        Left_wheel_encoder = struct.unpack('i', read[0:4])[0] * 0.5
        Right_wheel_encoder = struct.unpack('i', read[4:8])[0] * 0.5
        return Left_wheel_encoder,Right_wheel_encoder
    
    def open(self):
        try:
            self.port = serial.Serial(port=self.comport, baudrate=self.rate)
            #print(self.port)
        except:
              return 0
        return 1
    def close(self):
        self.port.close()
