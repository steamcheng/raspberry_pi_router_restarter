# Network Connectivity Monitor
raspberry_pi_router_restarter

By: Davis Whittaker
Last updated: 9 Aug 2016

This shell script tests network connectivity by pinging a few hosts and testing a few websites.  If it detects failure (3 or more failed pings or web URLs), it calls a python script that triggers a relay that turns power off to the gateway (a Verizon branded D-Link DSL modem/router) for 15 seconds to initiate a full restart and new connection.

Although this is currently running on a Raspberry Pi that is used as an OpenHAB home automation center, it could be run on any Linux machine on the network.  This script is called by cron at an interval set by the user.  My setting is every 10 minutes.
