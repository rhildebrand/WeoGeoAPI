#!/usr/bin/env python

""" This sample code will allow you to connect to the WeoGeo Market and get a list of datasets.  
You'll need the WeoGeo Python API that can be acquired by "pip install WeoGeoAPI". """

print "\nConnecting to WeoGeo...\n"
 
# Import Needed Libraries
 
import WeoGeoAPI
import json
 
# This example connects to the public market.  You don't need any user info.
 
weos = WeoGeoAPI.weoSession('http://market.weogeo.com', '', '')
 
# Connect
 
if weos.connectToMarket() is True:
  
  print "\nFetching your datasets...\n"
  
  """ We query for datasets over Phoenix, AZ.  Requesting the data in JSON format.  You can 
  find all the possible filters in the documentation 
  (http://www.weogeo.com/developer_doc/Datasets_API.html) """
  
  weoOutput = weos.getDatasets('JSON','&north=33.75&south=33.25&west=-111.75&east=-111.25')
  
  print "Here are your records:\n"
  
  # We pretty print the response
  
  print json.dumps(weoOutput, indent=4)
 
# If connection fails, then exit and tell the user.
 
else:

  print "\nYou cannot connect to WeoGeo, check your Internet connection.\n"