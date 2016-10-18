#!/usr/bin/python
##
## Router Restarter
## By: Davis Whittaker
## Last updated: 15 Aug 2016
## 
## 15 Aug 2016 - Added ability to email me when a reset occurs.
##
## This script is called by the netcheck3 shell script
## to restart the router when a failed connection is detected.

## Set things up here
import time ## Import time library
import RPi.GPIO as GPIO ## Import GPIO Library
# Import smtplib for the actual sending function
import smtplib
# Import the email modules we'll need
from email.mime.text import MIMEText
GPIO.setmode(GPIO.BOARD) ## Use BOARD pin numbering
GPIO.setup(7, GPIO.OUT) ## Setup GPIO pin 7 to OUT

with open("/home/pi/bin/routerreset.log", "a") as text_file:
 text_file.write("* %s -====== Network failure detected by RasPi. ======-\n" % time.strftime("%Y-%m-%d %X"))
 text_file.write("* %s Resetting router power. \n" % time.strftime("%Y-%m-%d %X"))
 text_file.close()
 
with open("/home/pi/bin/notification.txt", "a") as text_file:
 text_file.write("* %s -====== Network failure detected by RasPi. ======-\n" % time.strftime("%Y-%m-%d %X"))
 text_file.write("* %s Resetting router power. \n" % time.strftime("%Y-%m-%d %X"))
 text_file.close()

GPIO.output(7, True) ## Turn on GPIO pin 7 - opens relay
time.sleep(15) ## Wait 15 seconds before restarting router
GPIO.output(7, False) ## Turn off GPIO pin 7 - let relay close again
GPIO.cleanup()

with open("/home/pi/bin/routerreset.log", "a") as text_file:
 text_file.write("* %s Finished router power reset. \n\n" % time.strftime("%Y-%m-%d %X"))
 text_file.close()

with open("/home/pi/bin/notification.txt", "a") as text_file:
 text_file.write("* %s Finished router power reset. \n\n" % time.strftime("%Y-%m-%d %X"))
 text_file.close()

""" Email me with the failure information """
time.sleep(300) ## Wait 5 minutes for router to restart before trying to send email

# Open a plain text file for reading.  This file is the information 
# on the reset logged above.
fp = open('/home/pi/bin/notification.txt', 'rb')
# Create a text/plain message
msg = MIMEText(fp.read())
fp.close()

# Login information for the mail server.
gmail_user = 'xxxxx'
gmail_pwd = 'xxxxxxx'

me = 'xxxx@xxxxxx.net'
you = 'xxxxx@gmail.com'
msg['Subject'] = 'Network Failure - Router was reset!'
msg['From'] = me
msg['To'] = you

# Send the message via our own SMTP server, but don't include the
# envelope header.
server_ssl = smtplib.SMTP_SSL("smtp.gmail.com", 465)
server_ssl.ehlo() # optional, called by login()
server_ssl.login(gmail_user, gmail_pwd)  
# ssl server doesn't support or need tls, so don't call server_ssl.starttls() 
server_ssl.sendmail(me, you, msg.as_string())
#server_ssl.quit()
server_ssl.close()
