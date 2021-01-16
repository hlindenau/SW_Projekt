import smtplib

from email.MIMEMultipart import MIMEMultipart

from email.MIMEText import MIMEText

from email.MIMEBase import MIMEBase

from email import encoders

from subprocess import call 

import pyrebase

# database configuration
config = {
    "apiKey": "AIzaSyDc_M-tK_fnAg_sT5-MXkSLzQxkafSgJeE",
    "authDomain": "raspi-surveillance-camera.firebaseapp.com",
    "databaseURL": "https.//raspi-surveillance-camera.firebaseio.com",
    "projectId": "raspi-surveillance-camera",
    "storageBucket": "raspi-surveillance-camera.appspot.com",
    "messagingSenderId": "2557983580",
    "appId": "1:2557983580:web:7174e228ea0fecf28d1f99",
    "measurementId": "G-8NJX0T18V2"
}


fromaddr = "hubert.lindenau.dev@gmail.com"

toaddr = "hubert.lindenau@gmail.com"

msg = MIMEMultipart()

msg['From'] = fromaddr

msg['To'] = toaddr

msg['Subject'] = "Motion Cam Activated"

body = "Video of Motion Detected"

msg.attach(MIMEText(body, 'plain'))

import os


rootpath = '/var/lib/motion'

filelist = [os.path.join(rootpath, f) for f in os.listdir(rootpath)]

filelist = [f for f in filelist if os.path.isfile(f)]

newest = max(filelist, key=lambda x: os.stat(x).st_mtime)

command = "ffmpeg -i " + newest +" -codec copy "  + newest[:-3] + "mp4"
call([command],shell=True)

converted = newest[:-3] + "mp4"

filename = newest

attachment = open(newest, "rb")

part = MIMEBase('application', 'octet-stream')

part.set_payload((attachment).read())

encoders.encode_base64(part)

part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

msg.attach(part)

server = smtplib.SMTP('smtp.gmail.com', 587)

server.starttls()

server.login(fromaddr, "haslo")

text = msg.as_string()

server.sendmail(fromaddr, toaddr, text)

server.quit()

# connect to the database
firebase = pyrebase.initialize_app(config)
storage = firebase.storage()

print(filename[16:-3])
print(attachment)
print(converted)

# send video to the firebase db
path_on_cloud = "videos/" + converted[16:];
storage.child(path_on_cloud).put(converted)
