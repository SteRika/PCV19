from time import sleep
#import RPi.GPIO as GPIO
import serial
import psycopg2
import threading
from tkinter import *
import tkinter as tk
from decimal import Decimal,getcontext
from PIL import Image, ImageTk, ImageEnhance, ImageFilter
import urllib.request as urllibreq
import requests
import json
import sys
from functools import partial

getcontext().prec = 3
getdata = []
card_no = ""
cardid = ""
badge = ""
name = ""
zone = ""
data = True
root = tk.Tk()
top = Toplevel(root)
pic = ""
logo = PhotoImage(file=pic)
url = 'http://192.168.88.19:1338/graphql'

ser = serial.Serial(
        port='COM3', #Replace ttyS0 with ttyAM0 for Pi1,Pi2,Pi0
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
        
        self.root = root
        #self.top = Toplevel(root)

        #canvas login
        width = 720
        height = 360
        self.canvas1 = tk.Canvas(top, width = width, height = height)
        self.canvas1.pack()
        self.aaimg1 = ImageTk.PhotoImage(Image.open(r'C:\Users\Sukmo Aji - MIS\Desktop\PCV19\imagelink\image\bg.png').resize((1220,880)))
        self.bg1 = self.canvas1.create_image(-150,0, image=self.aaimg1,anchor="nw")
        self.img1 = ImageTk.PhotoImage(Image.open(r'C:\Users\Sukmo Aji - MIS\Desktop\PCV19\imagelink\image\logo.png'))
        self.canvas1.create_image(width*0.5,height*0.13, image=self.img1)
        self.canvas1.image = self.img1
        self.username = tk.Entry(top,width=20,font = "AgencyFb 22 bold") 
        self.canvas1.create_window(0.5*width, 0.5*height, window=self.username)
        self.usernametext = "USERNAME :"
        self.usernamearea = self.canvas1.create_text(width*0.5, height*0.38, text= self.usernametext, justify=CENTER, font=("Agency Fb", 18, "bold"))
        self.password = tk.Entry(top,show='*',width=20,font = "AgencyFb 22 bold")
        self.passwordtext = "PASSWORD :"
        self.passwordarea = self.canvas1.create_text(width*0.5, height*0.62, text= self.passwordtext, justify=CENTER, font=("Agency Fb", 18, "bold"))
        self.canvas1.create_window(0.5*width, 0.75*height, window=self.password)
        self.rect1 = self.canvas1.create_rectangle (20, 78, 700, 85, fill="#000000", outline ='#f9f7f6')
        self.loginbtn = tk.Button(top,text='LOG IN',height = 3,width = 104,bg ='red', command=lambda:self.login(self.username.get(),self.password.get()))
        self.canvas1.create_window(0.5*width, 0.943*height, window=self.loginbtn)


        #canvas utama
        width = 1366
        height = 768
        
        self.canvas = Canvas(root, width = width ,height = height,bg="white")
        self.aaimg2 = ImageTk.PhotoImage(Image.open(r'C:\Users\Sukmo Aji - MIS\Desktop\PCV19\imagelink\image\bg.png').resize((1400,800)))
        self.bg = self.canvas.create_image(-35,-30, image=self.aaimg2,anchor="nw")
        root.title("PCV-19 Data Input")
        root.geometry("%sx%s"%(width,height))
        
        
        self.img = ImageTk.PhotoImage(Image.open(r'C:\Users\Sukmo Aji - MIS\Desktop\PCV19\imagelink\image\-.gif').resize((400,500)))
        self.img3 = ImageTk.PhotoImage(Image.open(r'C:\Users\Sukmo Aji - MIS\Desktop\PCV19\imagelink\image\logo.png'))
        self.imgBorder = ImageTk.PhotoImage(Image.open(r'C:\Users\Sukmo Aji - MIS\Desktop\PCV19\imagelink\image\border.png').resize((430,370)))
        self.textvalue = ""
        self.textlabel = "NoBadge \n\n\n Nama"
        self.textgejala = "Apa yang anda rasa kan saat ini ???"
        self.textsuhu = "Berapa suhu tubuh anda ???"
        self.textc = "°c"
                
        self.imgAreax = self.canvas.create_image(width*0.26,height*0.35,image = self.img)
        self.imgAreax3 = self.canvas.create_image(width*0.5,height*0.06, image=self.img3)
        self.textAreaxvalue = self.canvas.create_text(width*0.26, height*0.75, text= self.textvalue, justify=CENTER, font=("Agency Fb", 32, "bold"))
        self.textAreaxlabel = self.canvas.create_text(width*0.258, height*0.69, text= self.textlabel,justify=CENTER, font=("Times New Roman", 24))
        self.textAreaxGejala = self.canvas.create_text(0.6*width, 0.19*height,anchor="w", text= self.textgejala,justify=CENTER, font=("Times New Roman", 24))
        self.rect1 = self.canvas.create_rectangle (3, 78, 1360, 85, fill="#000000", outline ='#f9f7f6')             
        self.textAreaxSuhu = self.canvas.create_text(0.6*width, 0.65*height,anchor="w", text= self.textsuhu,justify=CENTER, font=("Times New Roman", 24))
        self.textAreaxc = self.canvas.create_text(0.7*width, 0.8*height,anchor="w", text= self.textc,justify=CENTER, font=("AgencyFb bold", 43))
        self.canvas.pack()

        self.gejala = tk.Entry(root,width=12, font = "AgencyFb 22 bold") 
        self.derajat = tk.Entry(root,width=4,font = "AgencyFb 30 bold")
        self.derajat.insert(0, (375/10))
        self.canvas.create_window(0.6*width, 0.80*height,anchor="w", window=self.derajat)

     
      
        self.kelelahan = tk.Button(text='KELELAHAN', height = 2, width = 10,font = "AgencyFb 10", background = "white", command=self.switch_kelelahan)
        self.canvas.create_window(0.65*width, 0.26*height, window=self.kelelahan)     
        self.batukKering = tk.Button(text='BATUK\nKERING', height = 2, width = 10,font = "AgencyFb 10", background = "white", command=self.switch_batukKering)
        self.canvas.create_window(0.65*width, 0.34*height, window=self.batukKering)       
        self.nafasPendek = tk.Button(text='SESAK\nNAFAS',height = 2,width = 10,font = "AgencyFb 10", background = "white",  command=self.switch_nafasPendek)
        self.canvas.create_window(0.65*width, 0.42*height, window=self.nafasPendek)
        self.demam = tk.Button(text='DEMAM',height = 2,width = 10, font = "AgencyFb 10", background = "white", command=self.switch_demam)
        self.canvas.create_window(0.65*width, 0.5*height, window=self.demam)

        self.mataMerah = tk.Button(text='MATA MERAH', height = 2, width = 10,font = "AgencyFb 10", background = "white",  command=self.switch_mataMerah)
        self.canvas.create_window(0.75*width, 0.26*height, window=self.mataMerah)
        self.menggigil = tk.Button(text='MENGGIGIL', height = 2, width = 10,font = "AgencyFb 10", background = "white",  command=self.switch_menggigil)
        self.canvas.create_window(0.75*width, 0.34*height, window=self.menggigil)
        self.nyeriPunggung = tk.Button(text='NYERI\nPUNGGUNG',height = 2,width = 10, font = "AgencyFb 10", background = "white",  command=self.switch_nyeriPunggung)
        self.canvas.create_window(0.75*width, 0.42*height, window=self.nyeriPunggung)
        self.diare = tk.Button(text='DIARE',height = 2,width = 10,font = "AgencyFb 10", background = "white",  command=self.switch_diare)
        self.canvas.create_window(0.75*width, 0.5*height, window=self.diare)

        self.hilangPenciuman = tk.Button(text='HILANG\nPenciuman', height = 2, width = 10,font = "AgencyFb 10", background = "white",  command=self.switch_hilangPenciuman)
        self.canvas.create_window(0.85*width, 0.26*height, window=self.hilangPenciuman)
        self.sakitKepala = tk.Button(text='SAKIT\nKEPALA', height = 2, width = 10,font = "AgencyFb 10", background = "white",  command=self.switch_sakitKepala)
        self.canvas.create_window(0.85*width, 0.34*height, window=self.sakitKepala)
        self.hidungTersumbat = tk.Button(text='HIDUNG\nTERSUMBAT',height = 2,width = 10 , font = "AgencyFb 10", background = "white",  command=self.switch_hidungTersumbat)
        self.canvas.create_window(0.85*width, 0.42*height, window=self.hidungTersumbat)
        self.sakitTenggorokan = tk.Button(text='SAKIT\nTENGGOROKAN',height = 2,width = 10, font = "AgencyFb 10", background = "white",   command=self.switch_sakitTenggorokan)
        self.canvas.create_window(0.85*width, 0.5*height, window=self.sakitTenggorokan)

        self.temp = StringVar()
        self.temp1 = Radiobutton(text = "37.5", height = 2,width = 5,bg = "white",font = "AgencyFb ", variable = self.temp, value = "37.5", command = self.tempChange)
        self.canvas.create_window(0.63*width, 0.72*height, window=self.temp1)
        self.temp2 = Radiobutton(text = "38.5", height = 2,width = 5,bg = "white",font = "AgencyFb ", variable = self.temp, value = "38.5", command = self.tempChange)
        self.canvas.create_window(0.70*width, 0.72*height, window=self.temp2)
        self.temp3 = Radiobutton(text = "39.5", height = 2,width = 5,bg = "white",font = "AgencyFb ", variable = self.temp, value = "39.5", command = self.tempChange)
        self.canvas.create_window(0.77*width, 0.72*height, window=self.temp3)
        self.temp4 = Radiobutton(text = "40", height = 2,width = 5,bg = "white",font = "AgencyFb ", variable = self.temp, value = "40", command = self.tempChange)
        self.canvas.create_window(0.84*width, 0.72*height, window=self.temp4)


        self.add = tk.Button(text='+',height = 1,width = 1,bg = "white",font = "AgencyFb 24 bold", command=lambda:self.AddValue())
        self.canvas.create_window(0.75*width, 0.8*height,anchor = "w", window=self.add)
        self.minus = tk.Button(text='-',height = 1,width = 1,background = "white",font = "AgencyFb 24 bold", command=lambda:self.MinValue())
        self.canvas.create_window(0.8*width, 0.8*height,anchor = "w", window=self.minus)
       

        self.insert = tk.Button(text='SAVE',height = 2,width = 4, background = "white", font = "AgencyFb 22 bold", command=lambda:self.sendData(self.gejala.get()))
        self.canvas.create_window(0.95*width, 0.73*height, window=self.insert)
        self.cleardata = tk.Button(text='CLEAR',height = 2,width = 4, background = "white", font = "AgencyFb 22 bold", command=self.cleardata)
        self.canvas.create_window(0.95*width, 0.84*height, window=self.cleardata)




        self.updateGUI()
        self.readSensor()
    

    def login(self,username,password):
      global token
      
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
      print(r.text)
      '''print(final)
      print(token)
      print(testid)
      print("name is %s" % name)
      print("Employee Number is %s" % badge)'''

      query2 = '''query test {
                    roles(where: {
                      users: {
                        have: {
                          objectId: {
                            equalTo: "%s"
                          } 
                        }
                      }
                    }){
                      edges {
                        node {
                          name
                        }
                      }
                    }
                  }''' % (testid)
      headers2 = {
          "X-Parse-Application-Id": "myAppId",
          "X-Parse-Session-Token": "%s"%token
      }
      r2 = requests.post(url, json={'query': query2},headers=headers2)
      '''print(query2)'''
      print(r2.text)
      b = r2.text
      b = b.strip('{')
      b = b.replace('{','')
      b = b.replace('}','')
      b = b.replace('"','')
      b = b.replace(',',':')
      final2 = b.split(':')
      role = final2[8].strip()
      role = role.replace(']','')
      print(final2)
      print(role)
      if role == 'Security': #Checks whether username and password are correct
          root.deiconify() #Unhides the root window
          top.destroy() #Removes the toplevel window

    def sendData(self,gejala):
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

        c = r3.text
        c = c.strip('{')
        c = c.replace('{','')
        c = c.replace('}','')
        c = c.replace('"','')
        c = c.replace(',',':')
        final3 = c.split(':')
        objectid = final3[5].strip()
        objectid = objectid.replace(']','')
        print(objectid)
        print (final3)
        #print(objectid)

        json = {
          "query": '''   
            mutation saveMonitoredUser($input: CreateMonitoredUserFieldsInput!) {
                        createMonitoredUser(input: { fields: $input }) {
                                monitoredUser {
                                        id
                                }
                        }
                }
          ''',
          "variables": {
            "input": {
            "ptsnUser": {
              "link": "%s"%objectid
            },
            "status": "OC", 
            "remarks": "%s%s"%(self.gejala.get(),self.derajat.get())
             }   
        }
          }

        headers4 = {
          "X-Parse-Application-Id": "myAppId",
          "X-Parse-Session-Token": "%s"%token
        }

        r4 = requests.post(url, json=json,headers=headers4)

        del getdata[:]
        x2 = Decimal(37.5)
        self.derajat.delete(0, "end")
        self.derajat.insert(0, x2)
        self.gejala.delete(0, "end")
        self.demam['state'] = tk.NORMAL
        self.menggigil['state'] = tk.NORMAL
        self.batukKering['state'] = tk.NORMAL
        self.nyeriPunggung['state'] = tk.NORMAL
        self.diare['state'] = tk.NORMAL
        self.nafasPendek['state'] = tk.NORMAL
        self.sakitKepala['state'] = tk.NORMAL
        self.hidungTersumbat['state'] = tk.NORMAL
        self.sakitTenggorokan['state'] = tk.NORMAL
        self.kelelahan['state'] = tk.NORMAL
        self.mataMerah['state'] = tk.NORMAL
        self.hilangPenciuman['state'] = tk.NORMAL
            
    def run(self):
        root.withdraw()
        self.root.mainloop()

    def tempChange(self):
        on = self.temp.get()
        if on == "37.5":
          self.derajat.delete(0,"end")
          self.derajat.insert(0,on)
        elif on == "38.5":
          self.derajat.delete(0,"end")
          self.derajat.insert(0,on)
        elif on == "39.5":
          self.derajat.delete(0,"end")
          self.derajat.insert(0,on)
        elif on == "40":
          self.derajat.delete(0,"end")
          self.derajat.insert(0,on)
    
    def switch_sakitKepala(self):
        self.SendToText("SAKIT KEPALA")
        self.sakitKepala['state'] = tk.DISABLED

    def switch_kelelahan(self):
        self.SendToText("KELELAHAN")
        self.kelelahan['state'] = tk.DISABLED

  
    def switch_hidungTersumbat(self):
        self.SendToText("HIDUNG TERSUMBAT")
        self.hidungTersumbat['state'] = tk.DISABLED

    def switch_hilangPenciuman(self):
        self.SendToText("HILANG PENCIUMAN")
        self.hilangPenciuman['state'] = tk.DISABLED

    def switch_sakitTenggorokan(self):
        self.SendToText("SAKIT TENGGOROKAN")
        self.sakitTenggorokan['state'] = tk.DISABLED

    def switch_menggigil(self):
        self.SendToText("MENGGIGIL")
        self.menggigil['state'] = tk.DISABLED
        
    def switch_nyeriPunggung(self):
        self.SendToText("NYERI PUNGGUNG")
        self.nyeriPunggung['state'] = tk.DISABLED

    def switch_demam(self):
        self.SendToText("DEMAM")
        self.demam['state'] = tk.DISABLED

    def switch_mataMerah(self):
        self.SendToText("MATA MERAH")
        self.mataMerah['state'] = tk.DISABLED

    def switch_batukKering(self):
        self.SendToText("BATUK KERING")
        self.batukKering['state'] = tk.DISABLED

    def switch_nafasPendek(self):
        self.SendToText("SESAK NAFAS")
        self.nafasPendek['state'] = tk.DISABLED

    def switch_diare(self):
        self.SendToText("DIARE")
        self.diare['state'] = tk.DISABLED


    def AddValue(self):  
        x1 = self.derajat.get()
        if float(x1) < 40 : 
          x2 = Decimal(x1) + Decimal(0.1)
          self.derajat.delete(0, "end")
          self.derajat.insert(0, x2)
        else:
          self.derajat.delete(0, "end")
          self.derajat.insert(0, "40")
          

    def MinValue(self):  
        x1 = self.derajat.get()
        if float(x1) > 37.5:
          x2 = Decimal(x1) - Decimal(0.1)
          self.derajat.delete(0, "end")
          self.derajat.insert(0, x2)
        else:
          self.derajat.delete(0, "end")
          self.derajat.insert(0, "37.5")
        
    def SendToText(self,text):
        self.gejala.insert(0, text + ',')

  
    def cleardata(self):
        del getdata[:]
        x2 = Decimal(37.5)
        self.derajat.delete(0, "end")
        self.derajat.insert(0, x2)
        self.gejala.delete(0, "end")
        self.demam['state'] = tk.NORMAL
        self.menggigil['state'] = tk.NORMAL
        self.batukKering['state'] = tk.NORMAL
        self.nyeriPunggung['state'] = tk.NORMAL
        self.diare['state'] = tk.NORMAL
        self.nafasPendek['state'] = tk.NORMAL
        self.sakitKepala['state'] = tk.NORMAL
        self.hidungTersumbat['state'] = tk.NORMAL
        self.sakitTenggorokan['state'] = tk.NORMAL
        self.kelelahan['state'] = tk.NORMAL
        self.mataMerah['state'] = tk.NORMAL
        self.hilangPenciuman['state'] = tk.NORMAL
        
    def updateGUI(self):
        self.root.update()

    def readSensor(self):
        global no_badge
        global nama
        
        data = (getdata[-1].split(",") if len(getdata) > 0 else ["-","-","-","-","-","-"])
        if len (getdata) > 1 :
              data[0:1]
        self.text =  " %s \n\n %s " % (data[1],data[2])
        no_badge = str(data[1])
        nama = str(data[2])
        path = str(data[5])
        
        if path != "-":
          imgsample = Image.open(urllibreq.urlopen(urllibreq.Request(path)))
          
        else:
          imgsample = Image.open(r'C:\Users\Sukmo Aji - MIS\Desktop\PCV19\imagelink\image\-.gif')
          
        width, height = imgsample.size
        newsize=(300,300)
        im1 = imgsample.resize(newsize)
        self.img = ImageTk.PhotoImage(im1)
        self.canvas.itemconfig(self.imgAreax, image = self.img)
        self.canvas.itemconfig(self.imgAreax3, image = self.img3)
        self.canvas.itemconfig(self.textAreaxvalue, text = self.text)
        self.root.update
        self.root.after(527, self.readSensor)

    
        
if __name__ == "__main__":
    SensorThread().start()
    Gui().run()
