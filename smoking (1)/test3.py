from time import sleep
import RPi.GPIO as GPIO
import psycopg2
import threading
from tkinter import *
import tkinter as tk
import subprocess
from PIL import Image, ImageTk
import urllib.request as urllibreq
import serial
from decimal import Decimal,getcontext
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17,GPIO.OUT)
GPIO.output(17,GPIO.LOW)

getcontext().prec = 3
getdataIn = []
getdataOutput = []
card_no = ""
cardid = ""
badge = ""
name = ""
zone = ""
global data
data = True
root = Tk()
pic = ""
logo = PhotoImage(file=pic)
value = ""
value1= ""
value_in = ""
serIn = serial.Serial(
        port='/dev/ttyACM0',
        baudrate = 9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
)


serOut = serial.Serial(
        port='/dev/ttyACM1', 
        baudrate = 9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
)


class SensorThreadInDoor(threading.Thread):
  def run(self):
    try:
      while True:
        
        inDoor = serIn.readline()
        if inDoor != b'':
            inCode = inDoor.decode("utf-8")
            card_noIn = inCode.rstrip()
            valueIn = card_noIn.rstrip()
            
            global value
            if value == "":
              value = valueIn
            print(valueIn)
            IP = subprocess.check_output(["hostname", "-I"])
            if IP != b'\n' :
              dbIn = psycopg2.connect(user = "postgres", password = "postgres",
                                host= "snws01", port = "5432",
                                database = "ESDG")
            else:
              dbIn = psycopg2.connect(user = "postgres", password = "postgres",
                                host= "127.0.0.1", port = "5432",
                                database = "zonatest")

            curIn = dbIn.cursor()

            sqlIn = ("SELECT card_no, badge_no, name, time_left, time, atsr FROM public.employee where card_no = '%s'" %(valueIn))
            curIn.execute(sqlIn)
            valTimeIn = int(time.time())
            get_dataIn = curIn.fetchone()
            if get_dataIn :
                #print(get_dataIn[4])
                if get_dataIn[4] != "" and  get_dataIn[4] is not None:
                  tc.time_convert(int(get_dataIn[3]))
                  #TimeInCheck = int(time.time())
                  TimeInCheck = int(get_dataIn[4]) + 4000
                  
                  if((TimeInCheck - int(get_dataIn[4])) < 3600):
                    valTimeInCheck = (3600-(TimeInCheck - int(get_dataIn[4])))
                    tc.time_convert(valTimeInCheck)
                    getdataIn.append(str(get_dataIn[0])+","+str(get_dataIn[1])+","+str(get_dataIn[2])+","+"Belum Boleh Masuk"+"("+str(TimeLeft)+")"+","+str(get_dataIn[4])+","+"-")
                    sleep(1)
                    del getdataIn[:]

                  else:
                    sql2 = ("UPDATE public.employee SET time='%s',date = date_trunc('second', now()::timestamp),atsr='1' WHERE card_no = '%s'"%(str(valTimeIn),str(get_dataIn[0])))
                    curIn.execute(sql2)
                    dbIn.commit()
                    
                    getdataIn.append(str(get_dataIn[0])+","+str(get_dataIn[1])+","+str(get_dataIn[2])+","+str(TimeLeft)+","+str(get_dataIn[4])+","+"-")
                    #print("B%s"%getdataOutput)
                    '''sqlLogIn = ("INSERT INTO public.sr_logs(name, badge_no, date, atsr)VALUES ('%s', '%s', date_trunc('second', now()::timestamp), '1')"%(str(get_dataIn[2]),str(get_dataIn[1])))
                    curIn.execute(sqlLogIn)
                    dbIn.commit()'''
                    
                    
                    sleep(1)
                    if GPIO.input(17) != 1 :
                      GPIO.output(17,GPIO.HIGH)
                      timer = threading.Timer(4, self.gfg)
                      timer.start()
                    del getdataIn[:]
                    
                    
                else :
                  sql2 = ("UPDATE public.employee SET time='%s',date = date_trunc('second', now()::timestamp),atsr='1' WHERE card_no = '%s'"%(str(valTimeIn),str(get_dataIn[0])))
                  curIn.execute(sql2)
                  dbIn.commit()
                  tc.time_convert(int(get_dataIn[3]))
                  getdataIn.append(str(get_dataIn[0])+","+str(get_dataIn[1])+","+str(get_dataIn[2])+","+str(TimeLeft)+","+str(get_dataIn[4])+","+"-")
                  #print("B%s"%getdataOutput)
                  '''sqlLogIn = ("INSERT INTO public.sr_logs(name, badge_no, date, atsr)VALUES ('%s', '%s', date_trunc('second', now()::timestamp), '1')"%(str(get_dataIn[2]),str(get_dataIn[1])))
                  curIn.execute(sqlLogIn)
                  dbIn.commit()'''
                  sleep(1)
                  if GPIO.input(17) != 1 :
                      GPIO.output(17,GPIO.HIGH)
                      timer = threading.Timer(4, self.gfg)
                      timer.start()
                  del getdataIn[:]
                   
                value = ""
                curIn.close()
                dbIn.close()
                
    except KeyboardInterrupt:
        exit()

  def gfg(self):
    if GPIO.input(17) == 1 :
      GPIO.output(17,GPIO.LOW)


class SensorThreadOutDoor(threading.Thread):
  def run(self):
    try:
      while True:
        OutDoor = serOut.readline()
        if OutDoor != b'':
            OutCode = OutDoor.decode("utf-8")
            card_noOut = OutCode.rstrip()
            valueOut = card_noOut.rstrip()
            global value1
            if value1 == "" :
              value1 = valueOut
              print(valueOut)
            
            IP = subprocess.check_output(["hostname", "-I"])
            if IP != b'\n' :
              dbOut = psycopg2.connect(user = "postgres", password = "postgres",
                                host= "snws01", port = "5432",           
                                database = "ESDG")
            else:
              dbOut = psycopg2.connect(user = "postgres", password = "postgres",
                                host= "127.0.0.1", port = "5432",
                                database = "zonatest")
            
            curOut = dbOut.cursor()
            sqlOut = ("SELECT card_no,time,time_left FROM public.employee where card_no = '%s'" %(valueOut))
            curOut.execute(sqlOut)
            valTimeOut = int(time.time())
            get_dataOut = curOut.fetchone()
            
            if get_dataOut:
              if get_dataOut[1] != "" and  get_dataOut[1] is not None:
                  valTimeTotal = valTimeOut - int(get_dataOut[1])
                  valTimeLeft = int(get_dataOut[2]) - valTimeTotal
                  print(valTimeLeft)
                
                  sql3 = ("UPDATE public.employee SET time_left='%s',atsr='0' WHERE card_no = '%s'"%(str(valTimeLeft),str(get_dataOut[0])))
                  curOut.execute(sql3)
                  dbOut.commit()
                  
                  sqlDisplayOut = ("SELECT card_no, badge_no, name, time_left, time FROM public.employee where card_no = '%s'" %(get_dataOut[0]))
                  curOut.execute(sqlDisplayOut)
                  get_dataOutDisplay = curOut.fetchone()
                  
                  if get_dataOutDisplay:
                    '''if int(get_dataOutDisplay[3]) > 0 : '''
                    tc.time_convert(int(get_dataOutDisplay[3]))
                    
                    if int(get_dataOutDisplay[3]) > 0:
                      getdataIn.append(str(get_dataOutDisplay[0])+","+str(get_dataOutDisplay[1])+","+str(get_dataOutDisplay[2])+","+str(TimeLeft)+","+str(get_dataOutDisplay[4])+","+"-")
                      sql4 = ("UPDATE public.employee SET time_left='900' WHERE card_no = '%s'"%(str(get_dataOut[0])))
                      curOut.execute(sql4)
                      dbOut.commit()
                      
                    '''else:
                      getdataIn.append(str(get_dataOutDisplay[0])+","+str(get_dataOutDisplay[1])+","+str(get_dataOutDisplay[2])+","+str(TimeLeft)+","+str(get_dataOutDisplay[4])+","+"-")
                      sql4 = ("UPDATE public.employee SET time_left='900' WHERE card_no = '%s'"%(str(get_dataOut[0])))
                      curOut.execute(sql4)
                      dbOut.commit()'''
                    
                    '''sqlLogOut = ("INSERT INTO public.sr_logs(name, badge_no, date, atsr)VALUES ('%s', '%s', date_trunc('second', now()::timestamp), '0')"%(str(get_dataOutDisplay[2]),str(get_dataOutDisplay[1])))
                    curOut.execute(sqlLogOut)
                    dbOut.commit()'''
                    sleep(1)
                    if GPIO.input(17) != 1 :
                      GPIO.output(17,GPIO.HIGH)
                      timer = threading.Timer(4, self.gfg)
                      timer.start()
                    del getdataIn[:]

                  value1 = ""
      
            curOut.close()
            dbOut.close()

    except KeyboardInterrupt:
        exit()
        
  def gfg(self):
      if GPIO.input(17) == 1 :
        GPIO.output(17,GPIO.LOW)

class tc():
    def time_convert(sec):
      global TimeLeft
      mins = sec // 60
      sec = sec % 60
      hours = mins // 60
      mins = mins % 60
      TimeLeft = "{0}:{1}".format(int(mins),sec)


class Gui(object):
    def __init__(self):
        
        self.root = root
        height = 650
        width = 525
        self.canvas = Canvas(root, width = width ,height = height,bg="white")
        self.aaimg2 = ImageTk.PhotoImage(Image.open(r'/home/pi/Desktop/smoking/image/bg.png').resize((700,600)))
        self.bg = self.canvas.create_image(-30,0, image=self.aaimg2,anchor="nw")
        root.title("MONITORING SMOKING ROOM")
        root.geometry("%sx%s"%(width,height))
        
        
        self.img = ImageTk.PhotoImage(Image.open(r'/home/pi/Desktop/smoking/image/-.gif').resize((150,200)))
        self.img2 = ImageTk.PhotoImage(Image.open(r'/home/pi/Desktop/smoking/image/mis.gif').resize((75,75)))
        self.img3 = ImageTk.PhotoImage(Image.open(r'/home/pi/Desktop/smoking/image/logo.png'))
        self.imgBorder = ImageTk.PhotoImage(Image.open(r'/home/pi/Desktop/smoking/image/border.png').resize((230,180)))
        self.rect1 = self.canvas.create_rectangle (20, 78, 505, 85, fill="#000000", outline ='#f9f7f6')
        self.rect2 = self.canvas.create_rectangle (20, 528, 505, 535, fill="#000000", outline ='#f9f7f6')
        self.text = ""
        self.text1 = "PLEASE SCAN YOUR BADGE!"
        self.text2 = "NoBadge\n\n\nNama\n\n\nSisa Waktu"
        self.text3 = "Powered by\n\n\n\nwith ❤"
        
        
        self.imgAreax = self.canvas.create_image(width*0.5,height*0.35,image = self.img)
        self.imgAreaxBorder = self.canvas.create_image(width*0.5,height*0.35,image = self.imgBorder)
        self.imgAreax2 = self.canvas.create_image(width*0.5,height*0.91, image=self.img2)
        self.imgAreax3 = self.canvas.create_image(width*0.5,height*0.06, image=self.img3)
        self.textAreax = self.canvas.create_text(width*0.5, height*0.677, text= self.text, justify=CENTER, font=("Agency Fb", 18, "bold"))
        self.textAreax1 = self.canvas.create_text(width*0.5, height*0.175,fill="white", text= self.text1,justify=CENTER, font=("Agency Fb", 20, "bold"))
        self.textAreax2 = self.canvas.create_text(width*0.498, height*0.635, text= self.text2,justify=CENTER, font=("Times New Roman", 12))
        self.textAreax3 = self.canvas.create_text(width*0.5, height*0.91, text= self.text3,justify=CENTER, font=("Times New Roman", 12))
        self.canvas.pack()
        self.updateGUI()
        self.readSensor()

    def run(self):
        self.root.mainloop()

    def updateGUI(self):

        self.root.update()

    def readSensor(self):
      
        dataIn = (getdataIn[-1].split(",") if len(getdataIn) > 0 else ["-","-","-","-","-","-"])
        
        '''if len (getdataIn) > 1 :
              data[0:1]'''
        self.text =  " %s \n\n %s \n\n %s " % (dataIn[1],dataIn[2],dataIn[3])
        path = str(dataIn[5])
        
        if path != "-":
          imgsample = Image.open(urllibreq.urlopen(urllibreq.Request(path)))
          
        else:
          imgsample = Image.open(r'/home/pi/Desktop/smoking/image/-.gif')
          
        width, height = imgsample.size
        newsize=(160,160)
        im1 = imgsample.resize(newsize)
        self.img = ImageTk.PhotoImage(im1)
        self.canvas.itemconfig(self.imgAreax, image = self.img)
        self.canvas.itemconfig(self.imgAreaxBorder, image = self.imgBorder)
        self.canvas.itemconfig(self.imgAreax2, image = self.img2)
        self.canvas.itemconfig(self.imgAreax3, image = self.img3)
        self.canvas.itemconfig(self.textAreax, text = self.text)
        self.canvas.itemconfig(self.textAreax1, text = self.text1)

        self.root.update
        self.root.after(527, self.readSensor)
        
if __name__ == "__main__":
    SensorThreadInDoor().start()
    SensorThreadOutDoor().start()

    
    Gui().run()
    

