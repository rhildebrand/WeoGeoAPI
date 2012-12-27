#!/usr/bin/env python

""" see previous example on how to an order for a dataset (https://gist.github.com/4355769)

For this example we take a job create and submit it to WeoGeo to generate an order.  Looking at the token
field in the JSON, I've picked this TOPO Raster token "a32957481fde138c22c38a680f2ec65".  The dataset
can be viewed here:  http://market.weogeo.com/datasets/a32957481fde138c22c38a680f2ec65  """

print "\nConnecting to WeoGeo...\n"
 
# Import Needed Libraries
 
import WeoGeoAPI
import getpass
import json
 
# To order from WeoGeo, you need a username/password.  You can generate these at https://market.weogeo.com/register
 
USERNAME = raw_input("User email: ")

PASSWORD = getpass.getpass()
 
weos = WeoGeoAPI.weoSession('http://market.weogeo.com', USERNAME, PASSWORD)

""" We need to order the job created previously.  We've put our jobs in the cart so all we have to do is 
execute all the jobs in the cart. """

# Connect
 
if weos.connectToMarket() is True:

  print "\nSubmitting your job...\n"
	
  weoJob = weos.orderJobsInCart('', 'JSON')
	
  print "Here is your order info:\n"
  
  # We pretty print the response
  
  print json.dumps(weoJob, indent=4)
 
# If connection fails, then exit and tell the user.
 
else:

  print "\nYou cannot connect to WeoGeo, check your Internet connection.\n"