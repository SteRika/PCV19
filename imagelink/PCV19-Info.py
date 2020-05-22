from time import sleep
#import RPi.GPIO as GPIO
#import mfrc522 as MFRC522
import serial
import psycopg2
import threading
from tkinter import *
from PIL import Image, ImageTk
import requests
import urllib.request as urllibreq

'''GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17,GPIO.OUT)
GPIO.setup(27,GPIO.OUT)
GPIO.setup(22,GPIO.OUT)'''

#MIFAREReader = MFRC522.MFRC522()
getdata = []
card_no = ""
cardid = ""
badge = ""
name = ""
zone = ""
data = True
root = Tk()
pic = ""
logo = PhotoImage(file=pic)
username = '038129'
password = 'asdasdqwe'
url = 'http://192.168.88.19:1338/graphql'
ser = serial.Serial(
        port='COM5', #Replace ttyS0 with ttyAM0 for Pi1,Pi2,Pi0
        baudrate = 9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
)


class SensorThread(threading.Thread):
  def run(self):
    try:
      while True:
        a = ser.readline()
        if a != b'':
            ab = a.decode("utf-8")
            card_no = ab.rstrip()
            value = card_no.rstrip()
            db = psycopg2.connect(user = "postgres", password = "postgres",
                                host= "192.168.8.133", port = "5432",
                                database = "zonetest")
            cur = db.cursor()
            sql = ("SELECT card_no, badge_no, employee_name, zone,color,path FROM zone A INNER JOIN zonedetail B on A.zone = B.id where card_no = '%s'" %(value))
            cur.execute(sql)
            get_data = cur.fetchone()
            getdata.append(str(get_data[0])+","+str(get_data[1])+","+str(get_data[2])+","+str(get_data[3])+","+str(get_data[4])+","+str(get_data[5]))
            sleep(1)

    except KeyboardInterrupt:
        exit()


class Gui(object):
    def __init__(self):
        
        self.root = Tk()
        height = 650
        width = 525
        self.canvas = Canvas(root, width = width ,height = height,bg="white")
        self.aaimg2 = ImageTk.PhotoImage(Image.open(r'C:\Users\Sukmo Aji - MIS\Desktop\PCV19\imagelink\image\bg.png').resize((700,600)))
        self.bg = self.canvas.create_image(-30,0, image=self.aaimg2,anchor="nw")
        root.title("DIECOVID-19")
        root.geometry("%sx%s"%(width,height))
        
        
        self.img = ImageTk.PhotoImage(Image.open(r'C:\Users\Sukmo Aji - MIS\Desktop\PCV19\imagelink\image\-.gif').resize((150,200)))
        self.img2 = ImageTk.PhotoImage(Image.open(r'C:\Users\Sukmo Aji - MIS\Desktop\PCV19\imagelink\image\mis.gif').resize((75,75)))
        self.img3 = ImageTk.PhotoImage(Image.open(r'C:\Users\Sukmo Aji - MIS\Desktop\PCV19\imagelink\image\logo.png'))
        self.imgBorder = ImageTk.PhotoImage(Image.open(r'C:\Users\Sukmo Aji - MIS\Desktop\PCV19\imagelink\image\border.png').resize((230,180)))
        self.rect1 = self.canvas.create_rectangle (20, 78, 505, 85, fill="#000000", outline ='#f9f7f6')
        self.rect2 = self.canvas.create_rectangle (20, 528, 505, 535, fill="#000000", outline ='#f9f7f6')
        self.text = ""
        self.text1 = "PLEASE SCAN YOUR BADGE!"
        self.text2 = "NoBadge\n\n\nNama\n\n\nZona"
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

    def GetStatus(self,no_badge):
        query = """mutation login {
                logIn(input: { username: "%s", password: "%s" }) {
                  viewer {
                    sessionToken
                    user {
                      objectId
                      username
                      ptsnUser {
                        fullname
                      }
                    }
                  }
                }
                }""" % (username,password)
        headers = {
          "X-Parse-Application-Id": "myAppId",
        }
        url = 'http://192.168.88.19:1338/graphql'
        r = requests.post(url, json={'query': query},headers=headers)
        a = r.text
        a = a.strip('{')
        a = a.replace('{','')
        a = a.replace('}','')
        a = a.replace('"','')
        a = a.replace(',',':')
        final = a.split(':')
        #print(final)
        testid = final[8]
        name = final[13].strip()
        badge = final[10]
        token = final[4]+':'+final[5]
        print(name)
        print(badge)
        print(token)
        print(final)
        query3 = '''query MyQuery {
                    ptsnUsers(where: {badgeNo: {equalTo: "%s"}}) {
                      edges {
                        node {
                          objectId
                        }
                      }
                    }
                }'''%no_badge
        headers3 = {
          "X-Parse-Application-Id": "myAppId",
          "X-Parse-Session-Token": "%s"%token
        }
        r3 = requests.post(url, json={'query': query3},headers=headers3)
        print(no_badge)
        c = r3.text
        c = c.strip('{')
        c = c.replace('{','')
        c = c.replace('}','')
        c = c.replace('"','')
        c = c.replace(',',':')
        
        final3 = c.split(':')
        print (final3)
        print(no_badge)
        objectid = final3[5].strip()
        objectid = objectid.replace(']','')
        print (final3)
                #print(objectid)

        json = {
          "query": '''   
            query aNestedQuery ($id:ID!) {
          monitoredUsers (where :{
            ptsnUser : {
              have :{
                id :{equalTo : $id}
              }
            }
          }){
            edges{
              node{
                status
                }
              }
            }
          }
          ''',
          "variables": {
            "id": "%s"%objectid
        }
          }

        headers4 = {
          "X-Parse-Application-Id": "myAppId",
          "X-Parse-Session-Token": "%s"%token
        }

        r4 = requests.post(url, json=json,headers=headers4)
        b = r4.text
        b = b.strip('{')
        b = b.replace('{','')
        b = b.replace('}','')
        b = b.replace('"','')
        b = b.replace(',',':')
        final2 = b.split(':')
        print(final2)
        print(len(final2))
        if len(final2) > 4:
            global status
            status = final2[5].replace(']','')
            status = status.strip()
            print(status)
        else:
            status = "EXCELLENT"
            print("EXCELLENT")
    

    def readSensor(self):
        data = (getdata[-1].split(",") if len(getdata) > 0 else ["-","-","-","-","-","-"])
        if len (getdata) > 1 :
              data[0:1]
              
        if(data[1] == "-"):
           print("No Check")
           statusa = "+++"
        else:
          self.GetStatus(data[1])
          statusa = status
          del getdata[:]
        self.text =  " %s \n\n %s \n\n %s " % (data[1],data[2],statusa)
        path = str(data[5])
          
        
        if path != "-":
          imgsample = Image.open(urllibreq.urlopen(urllibreq.Request(path)))
          
        else:
          imgsample = Image.open(r'C:\Users\Sukmo Aji - MIS\Desktop\PCV19\imagelink\image\-.gif')
          
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
        self.root.after(1000, self.readSensor)
        
if __name__ == "__main__":
    SensorThread().start()
    Gui().run()
