# Network Connectivity Monitor
raspberry_pi_router_restarter

By: Davis Whittaker
Last updated: 9 Aug 2016

Although this is currently running on a Raspberry Pi that is used as an OpenHAB home automation center, it could be run on any Linux machine on the network.  This script is called by cron at an interval set by the user.  My setting is every 10 minutes.

# netcheck3.sh
This shell script tests the network connection by pinging the gateway and a few hosts, and testing a few websites for connectivity.  If it detects failure (3 or more failed pings and/or web URLs), it calls a python script to restart the gateway (a Verizon branded D-Link DSL modem/router).  The script logs results from each network connectivity check.

# bumprouter.py
This is the router restarting script.  When called by netcheck3.sh, this python script logs the event to a log file and then triggers a relay to interrupt power to the DSL modem/router for 15 seconds.  This performs a hard restart of the gateway and resets the internet connection from scratch.  The script also assembles and sends an email after a 5 minute wait to alert me that a reset has occurred.

# logrotate.py
This script runs nightly to archive the previous days logs.

# email_logs.py
This script sweeps up the previous day's logs and emails them to me for review.

