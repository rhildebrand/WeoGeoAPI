#!/usr/bin/env python

""" see previous example on how to submit jobs to be ordered (https://gist.github.com/4356165)

For this example we take a job create and submit it to WeoGeo to generate an order.  Looking at the 
token field in the JSON, I've picked this TOPO Raster token "a32957481fde138c22c38a680f2ec65".  
The dataset can be viewed here:  http://market.weogeo.com/datasets/a32957481fde138c22c38a680f2ec65  """

print "\nConnecting to WeoGeo...\n"
 
# Import Needed Libraries
 
import WeoGeoAPI
import getpass
import json
 
# To order from WeoGeo, you need a username/password.  You can generate these at https://market.weogeo.com/register
 
USERNAME = raw_input("User email: ")

PASSWORD = getpass.getpass()
 
weos = WeoGeoAPI.weoSession('http://market.weogeo.com', USERNAME, PASSWORD)

""" We take the job token returned to us in the create job example (https://gist.github.com/4355769).  
The "job_token": parameter is what we need.  Change "TOKEN" below to your unique job_token. """

# Connect
 
if weos.connectToMarket() is True:

  print "\nFinding download URL...\n"
	
	weoDownload = weos.getDownloadFile("TOKEN")
	
	print "Here is your download info:\n"
  
	# We pretty print the response
  
	print json.dumps(weoDownload, indent=4)
 
# If connection fails, then exit and tell the user.
 
else:

  print "\nYou cannot connect to WeoGeo, check your Internet connection.\n"