#!/usr/bin/python
##
## Router Restarter Log emailer
## By: Davis Whittaker
## Last updated: 18 Aug 2016
## 
## Emails me logs from the router and network
## connectivity checker for the previous day.
## 
## 

import smtplib
import datetime
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate

#Get the filename format worked out
yearmonth = datetime.datetime.now().strftime('%Y-%m-')
day = int(datetime.datetime.now().strftime('%d'))-1
logdate = yearmonth + str(day)

# Set up particulars for emailing here
send_to = ['xxxxx@gmail.com','yyyyy@gmail.com']
server = 'smtp.gmail.com'
port = 465
gmail_user = 'xxxxx'
gmail_pwd = 'xxxxx'
send_from = 'router@n1kx.net'
subject = 'Network monitor logs'
text = 'Daily network monitor logs attached.'
path = '/home/pi/bin/' + logdate
files = [path + '-pinglog3.log', path + '-routerreset.log', path + '-pinglog.log.tar.gz']

######### DEBUG Printing #########
#print files
#for file in files:
#	print basename(file)
##################################

msg = MIMEMultipart()
msg['From'] = send_from
msg['To'] = COMMASPACE.join(send_to)
msg['Date'] = formatdate(localtime=True)
msg['Subject'] = subject

try:	
	for f in files or []:
		with open(f, "rb") as fil:
			part = MIMEApplication(
				fil.read(),
				Name=basename(f)
			)
			part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
			msg.attach(part)
	print 'Files attached!'
except:
	text = text + '\n\nFailed to find files to attach!'
	print 'Failed to attach files!'

# Put in body of email test
msg.attach(MIMEText(text))

try:
	smtp = smtplib.SMTP_SSL(server, port)
	smtp.ehlo() # optional, called by login()
	smtp.login(gmail_user, gmail_pwd)
	smtp.sendmail(send_from, send_to, msg.as_string())
	smtp.close()
	print 'Email sent!'

except:
	print 'Failed to send email!'


