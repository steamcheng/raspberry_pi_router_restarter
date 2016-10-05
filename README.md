# raspberry_pi_router_restarter

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
