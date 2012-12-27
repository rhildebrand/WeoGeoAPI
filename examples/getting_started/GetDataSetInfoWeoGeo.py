#!/usr/bin/env python

""" see previous example on how to get a dataset (https://gist.github.com/4355190)

For this example we take a dataset found previously and get more information about it.  Looking 
at the token field in the JSON, I've picked this TOPO Raster token "a32957481fde138c22c38a680f2ec65".  
The dataset can be viewed here:  http://market.weogeo.com/datasets/a32957481fde138c22c38a680f2ec65  """

print "\nConnecting to WeoGeo...\n"
 
# Import Needed Libraries
 
import WeoGeoAPI
import json
 
# This example connects to the public market.  You don't need any user info.
 
weos = WeoGeoAPI.weoSession('http://market.weogeo.com', '', '')
 
# Connect
 
if weos.connectToMarket() is True:

  print "\nFetching your dataset...\n"
	
  weoOutput = weos.getDataset('a32957481fde138c22c38a680f2ec65', 'JSON')
	
  print "Here is your dataset:\n"
  
  # We pretty print the response
  
  print json.dumps(weoOutput, indent=4)
 
# If connection fails, then exit and tell the user.
 
else:

  print "\nYou cannot connect to WeoGeo, check your Internet connection.\n"