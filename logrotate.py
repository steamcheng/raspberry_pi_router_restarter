#!/usr/bin/python
##
## Router Restarter Log Manager
## By: Davis Whittaker
## Created: 17 Aug 2016
## Last updated: 8 Sep 2016 - Changed means of determining yesterday and day before dates.
## 
## Rolls logs for the day when called by cron job.
## saves a plain text copy of previous day and also a
## tar.gz archive of all.
## Deletes two day old plain text versions.

import tarfile
import datetime
import shutil
import os

# Daily logs being monitored and saved
logs = ['pinglog3.log', 'routerreset.log']
pipath = '/home/pi/bin/'
#Get the date for archive filename worked out
oldlogdate=(datetime.datetime.today()-datetime.timedelta(2)).strftime('%Y-%m-%d') +'-'
logdate=(datetime.datetime.today()-datetime.timedelta(1)).strftime('%Y-%m-%d') +'-'

# Name to give to tar gzipped archive every day
logfilename = logdate + 'pinglog.log.tar.gz'

# Function used to copy the logs to daily files.
def copylogs(loglist):
	for name in loglist:
		newname = pipath + logdate + name
		shutil.copy2(pipath + name, newname)

# Function used to zip up the logs.
def archivelogs(rawlogs):
	tar = tarfile.open(pipath + logfilename, 'w:gz')
	for name in rawlogs:
		name = pipath + logdate + name
		tar.add(name)
	tar.close()

# Function used to clear logs for the next day.
def clearlogs(archivelog, rawlogs):
	if os.path.exists(pipath + archivelog):
#		print 'Yes %s exists!' % (pipath + archivelog) # Used for testing and debugging.
		for log in rawlogs:
			fulllog = pipath + log
			open(fulllog,'w').close()
			oldlog = pipath + oldlogdate + log
			if os.path.exists(oldlog):
				os.remove(oldlog)
	else:
		print 'Bloody missing archive! %s' % archivelog
		
# Copy the pinglog to a simple daily archive with date in name.
# This facilitates short term log checking.
copylogs(logs)
# zip up the file for emailing and archiving.
archivelogs(logs)
#sleep(7) # Used for debugging
# Empty the log file for tomorrow and delete old raw backups.
clearlogs(logfilename, logs)
