#!/bin/bash
# Network Connectivity Monitor
# By: Davis Whittaker
# Last updated: 9 Aug 2016
#
# This shell script tests network connectivity by pinging a few hosts and 
# testing web connectivity.  If it detects a failure, it calls a python script
# that triggers a relay that turns power off to the gateway for 15 seconds to
# initiate a new connection.
# This script is called by cron at an interval set by the user.  My setting is
# every 10 minutes.
#
# Add ip / hostname to HOSTS and WEBHOSTS separated by white space.
HOSTS="www.google.com 192.168.1.1 www.amex.com www.yahoo.com sasebo"
WEBHOSTS="https://www.yahoo.com https://www.google.com https://www.fedex.com"


# Number of pings to send
COUNT=1
# Count failed items.
fails=0
WEBCTR=0
TESTFAILS=0

for myHost in $HOSTS
do
  ping -c $COUNT $myHost >/dev/null
 if [ $? -ne 0 ]; then
    # Ping fails
    echo "*** $(date): Host $myHost is unreachable (ping failed)" >> /home/pi/bin/pinglog3.log
    # Increment the fail counter.
    let fails=fails+1
   else
	# Ping is good
	echo "" >/dev/null
  fi
done

# Proceed to URL testing using curl and HTTP
for myWebHost in $WEBHOSTS
do
  if  curl --output /dev/null --silent --head --fail $myWebHost;
  then
    printf '%s\n' "$myWebHost exists" >/dev/null
    # echo "*** $(date): $myWebHost is reachable." >> /home/pi/bin/pinglog3.log
   else
	let WEBCTR=WEBCTR+1
    # printf '%s\n' "$myWebHost failed"
    echo "*** $(date): FAIL! Cannot reach $myWebHost." >> /home/pi/bin/pinglog3.log	
  fi
done

let TESTFAILS=fails+WEBCTR

if [ $TESTFAILS -ge 3 ];
  then
   printf '%s\n' >> /home/pi/bin/pinglog3.log
   echo "*** $(date): $TESTFAILS failed web tests! $fails pings and $WEBCTR failed URLs!  Resetting router!"	>> /home/pi/bin/pinglog3.log
   echo "*** $(date): $TESTFAILS failed web tests! $fails pings and $WEBCTR failed URLs!  Resetting router!"	> /home/pi/bin/notification.txt
   printf '%s\n' >> /home/pi/bin/pinglog3.log
   python /home/pi/bin/bumprouter.py
  else
   echo "* $(date): $fails pings and $WEBCTR web hosts failed.  OK for now." >> /home/pi/bin/pinglog3.log
#    printf '%s\n' >> /home/pi/bin/pinglog3.log
fi
