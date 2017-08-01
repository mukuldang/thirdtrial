# echo_server.py
import socket
import xlwt
import subprocess
import os
import smtplib
from email import encoders
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
import pdfkit
from twilio.rest import Client
ACCOUNT="AC255041b230dc7f5003607fc7ae101972"
SECRET="67ec8fc56082fdec1d8ca6f2480e4f44"
client=Client(ACCOUNT,SECRET)
COMMASPACE = ', '
import sys
from random import randint
import xlrd
import urllib
from bs4 import BeautifulSoup
import twilio
import os
import time
import json
from openpyxl import Workbook
import csv
host = 'localhost'       # Symbolic name meaning all available interfaces
port = 8080              # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(1)
import smtplib, os, sys
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders
from HTMLParser import HTMLParser

username="nchitaliya"
password="1234"
def emailing(send,passwo,topeople,subject):
    attachments = ['Results.pdf','fig.png']
    username = 'lorddarkseid08@gmail.com
    '
    password = 'Mukul123'
    host = 'smtp.gmail.com:587' # specify port, if required, using this notations

    fromaddr = 'lorddarkseid08@gmail.com' # must be a vaild 'from' address in your GApps account
    toaddr  = 'mukul94dang@gmail.com'
    replyto = fromaddr # unless you want a different reply-to

    msgsubject = 'Results for your survey!'

    htmlmsgtext = """<h2>RESULTS !!!</h2>
                    <p>\
                    The survey you have conducted is now complete.\
                    The results for your survey have been attached below.\ 
                     </p>
                    <p><strong>Here are your attachments:</strong></p><br />"""



    class MLStripper(HTMLParser):
        def __init__(self):
            self.reset()
            self.fed = []
        def handle_data(self, d):
            self.fed.append(d)
        def get_data(self):
            return ''.join(self.fed)

    def strip_tags(html):
        s = MLStripper()
        s.feed(html)
        return s.get_data()

    ########################################################################

    try:
        # Make text version from HTML - First convert tags that produce a line break to carriage returns
        msgtext = htmlmsgtext.replace('</br>',"\r").replace('<br />',"\r").replace('</p>',"\r")
        # Then strip all the other tags out
        msgtext = strip_tags(msgtext)

        # necessary mimey stuff
        msg = MIMEMultipart()
        msg.preamble = 'This is a multi-part message in MIME format.\n'
        msg.epilogue = ''

        body = MIMEMultipart('alternative')
        body.attach(MIMEText(msgtext))
        body.attach(MIMEText(htmlmsgtext, 'html'))
        msg.attach(body)

        if 'attachments' in globals() and len('attachments') > 0: # are there attachments?
            for filename in attachments:
                f = filename
                part = MIMEBase('application', "octet-stream")
                part.set_payload( open(f,"rb").read() )
                Encoders.encode_base64(part)
                part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(f))
                msg.attach(part)

        msg.add_header('From', fromaddr)
        msg.add_header('To', toaddr)
        msg.add_header('Subject', msgsubject)
        msg.add_header('Reply-To', replyto)

        # The actual email sendy bits
        server = smtplib.SMTP(host)
        server.set_debuglevel(False) # set to True for verbose output
        try:
            # gmail expect tls
            server.starttls()
            server.login(username,password)
            server.sendmail(msg['From'], [msg['To']], msg.as_string())
            print 'Email sent'
            server.quit() # bye bye
        except:
            # if tls is set for non-tls servers you would have raised an exception, so....
            server.login(username,password)
            server.sendmail(msg['From'], [msg['To']], msg.as_string())
            print 'Email sent'
            server.quit() # sbye bye        
    except:
        print ('Email NOT sent to %s successfully. %s ERR: %s %s %s ', str(toaddr), 'tete', str(sys.exc_info()[0]), str(sys.exc_info()[1]), str(sys.exc_info()[2]) )
        #just in case

while True:
    conn, addr = s.accept()
    print('Connected by', addr)
    data = conn.recv(10000)
    if data:   
        msg=data.decode('utf8')
        print(msg)
        msf=str(msg)
        a=msg.split(":")
        if a[0]=="excel":
            
            wb = Workbook()
            ws = wb.active
            b=a[1].split(",")
            for i in range(0,len(b)):
                ws.append([str(b[i])])
            wb.save("C:\\Users\\mukul\\Desktop\\excel1.xlsx")
            conn.sendall(data)
        elif a[0]=="questions":
            b=a[2].split(",")
            with open('convertcsv.csv', 'w') as csvfile:
                fieldnames = ['body', 'body','type']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for i in range(0,len(b)):
                    writer.writerow({'body': str(b[i]), 'body': str(b[i]),'type':'numeric'})
            dic={}
            for j in range(0,len(b)):
                if b[j]=="":
                    break
                dic[str(b[j])]='numeric'
            lst=[{'body':k,'type':v} for k,v in dic.items()]
            print(lst)
            x={'questions':lst,'title':str(a[1])}
            print (json.dumps(x, indent=2))
            with open('D:\\automated-survey-spring\\survey.json', 'w') as outfile:
                    json.dump(x, outfile)
            conn.sendall(data)
        elif a[0]=="password":
            b=a[1].split(",")
            if b[0]=="nchitaliya" and b[1]=="1234":
                m="True"
                conn.sendall(m.encode('utf8'))
            else:
                m="False"
                conn.sendall(m.encode('utf8'))
        elif a[0]=="True":
            book=xlrd.open_workbook("C:\\Users\\mukul\\Desktop\\excel1.xlsx")
            sheet=book.sheet_by_index(0)
            nrowss=sheet.nrows
            for i in range(0,nrowss):
                call=client.api.account.calls.create(to=str(sheet.cell_value(i,0)),from_="+13214223232",url="https://newtialjava2.herokuapp.com/survey/call",method='get')
                with open("C:\\Users\\mukul\\Desktop\\callfile.txt", "a") as myfile:
                    myfile.write(str(sheet.cell_value(i,0))+"="+str(call.sid)+"\n")
                time.sleep(90)
            os.system("copy C:\\Users\\mukul\\Desktop\\callfile.txt C:\\Users\\mukul\\Desktop\\callagain.txt")
            #os.system("java -jar C:\\Users\\mukul\\Desktop\\runnable.jar")
            print("Letstry this")
            pdfkit.from_url('https://newtialjava2.herokuapp.com/', 'Results.pdf')
            response=urllib.urlopen('https://newtialjava2.herokuapp.com/')
            res=response.read()
            soup=BeautifulSoup(res)
            lis=[]
            lis1=[]
            ratings=[]
            count=1
            for i in soup.find_all('li'):
                lis.append(i.text)
            for i in range(4,len(lis)):
                if i%4==0:
                    a=lis[i].split(": ")
                    lis1.append(a[1])
                if i-count==4:
                    count=i
                    a=lis[i].split(": ")
                    u=a[1].rstrip("\n ")
                    if int(u)>5:
                        ratings.append(str(5))
                    ratings.append(str(u))
            dic={}
            key=[]
            print("This is the lis")
            print(lis[4:])
            print("This is the ratings we got")
            print(ratings)
            with open("C:\\Users\\mukul\\Desktop\\callfile.txt","r") as f:
                for line in f:
                    b=line.split("=")
                    dic[str(b[1]).strip("\n")]=str(b[0])
                    key.append(str(b[1]).strip("\n"))
            count=0
            msg=""
            for i in range(0,len(key)):
                if key[i] not in lis1:
                    msg=msg+dic[key[i]]+","
                    count=count+1
            #if(msg==""):
            #    msg="NONE"
            #    conn.send(msg.encode('utf8'))
            conn.send(msg.encode('utf8'))
            realrating=[ratings.count("1"),ratings.count("2"),ratings.count("3"),ratings.count("4"),ratings.count("5"),count]
            msg1=""
            for i in range(0,len(realrating)):
                msg1=msg1+str(realrating[i])+","
            print(msg)
            print(msg1)
            conn.send(msg1.encode('utf8'))
            w=open("C:\\Users\\mukul\\Desktop\\callfile.txt","w")
            w.close()        
            print("HELLLLOOOOOOOOOOOOOOOOOOOO")
        elif a[0]=="call":
            msg="done"
            conn.send(msg.encode('utf8'))
            time.sleep(3600)
            for i in range(0,nrowss):
                call=client.api.account.calls.create(to=str(sheet.cell_value(i,0)),from_="+13214223232",url="https://newtialjava2.herokuapp.com/survey/call/")
                with open("C:\\Users\\mukul\\Desktop\\callagain.txt", "a") as myfile:
                    myfile.write(str(sheet.cell_value(i,0))+"="+str(sheet.cell_value(i,0))+"\n")
                time.sleep(90)
            print("Letstry this")
            pdfkit.from_url('https://newtialjava2.herokuapp.com/', 'Results.pdf')
            response=urllib.urlopen('https://newtialjava2.herokuapp.com/')
            res=response.read()
            soup=BeautifulSoup(res)
            lis=[]
            lis1=[]
            ratings=[]
            count=1
            for i in soup.find_all('li'):
                lis.append(i.text)
            for i in range(4,len(lis)):
                if i%4==0:
                    a=lis[i].split(": ")
                    lis1.append(a[1])
                if i-count==4:
                    count=i
                    a=lis[i].split(": ")
                    u=a[1].rstrip("\n ")
                    if int(u)>5:
                        ratings.append(str(5))
                    ratings.append(str(u))
            dic={}
            key=[]
            print("This is the lis")
            print(lis[4:])
            print("This is the ratings we got")
            print(ratings)
            with open("C:\\Users\\mukul\\Desktop\\callagain.txt","r") as f:
                for line in f:
                    b=line.split("=")
                    dic[str(b[1]).strip("\n")]=str(b[0])
                    key.append(str(b[1]).strip("\n"))
            count=0
            msg=""
            for i in range(0,len(key)):
                if key[i] not in lis1:
                    msg=msg+dic[key[i]]+","
                    count=count+1
            #if(msg==""):
            #    msg="NONE"
            #    conn.send(msg.encode('utf8'))
            realrating=[ratings.count("1"),ratings.count("2"),ratings.count("3"),ratings.count("4"),ratings.count("5"),count]
            msg1=""
            for i in range(0,len(realrating)):
                msg1=msg1+str(realrating[i])+","
            print(msg)
            print(msg1)
            #w=open("C:\\Users\\mukul\\Desktop\\callfile.txt","w")
            #w.close()        
            print("HELLLLOOOOOOOOOOOOOOOOOOOO")
            
            objects = ('Rating 1', 'Rating 2', 'Rating 3', 'Rating 4', 'Rating 5 \nor more', 'No \nResponse')
            y_pos = np.arange(len(objects))
            rating=a[1].split(',')
            rating.pop(len(rating)-1)
            plt.bar(y_pos, rating, align='center', alpha=0.5)
            plt.xticks(y_pos,objects)
            print(rating)
            plt.ylabel('Number of Responses')
            plt.title('Results for your survey!')
            plt.savefig('fig.png')
            emailing("lorddarkseid08@gmail.com","Mukul123",a[1],"Your Survey Results")
            w=open("C:\\Users\\mukul\\Desktop\\callagain.txt","w")
            w.close()
        elif a[0]=="git":
            os.system("git init")
            os.system("git add .")
            os.system("git remote add origin https://github.com/mukuldang/thirdtrial.git")
            os.system("git commit -m ""try"" ")
            os.system("git push origin master")
            msg="True"
            conn.send(msg.encode('utf8'))
            
        elif a[0]=="rating":
            objects = ('Rating 1', 'Rating 2', 'Rating 3', 'Rating 4', 'Rating 5 \nor more', 'No \nResponse')
            y_pos = np.arange(len(objects))
            x=a[1].decode('utf-8')
            rating=x.split(',')
            rating.pop(len(rating)-1)
            plt.bar(y_pos, rating, align='center', alpha=0.5)
            plt.xticks(y_pos,objects)
            print(rating)
            plt.ylabel('Number of Responses')
            plt.title('Results for your survey!')
            plt.savefig('fig.png')
            emailing("lorddarkseid08@gmail.com","Mukul123",["mukul94dang@gmail.com"],"Your Survey Results")
       

    
            
            
 



