#!/usr/bin/env python

""" see previous example on how to get a dataset (https://gist.github.com/4355190)

For this example we take a dataset found previously and order it from WeoGeo.  Looking at the token 
field in the JSON, I've picked this TOPO Raster token "a32957481fde138c22c38a680f2ec65".  The dataset 
can be viewed here:  http://market.weogeo.com/datasets/a32957481fde138c22c38a680f2ec65  """

import WeoGeoAPI

print "\nConnecting to WeoGeo...\n"
 
# Import Needed Libraries
 
import WeoGeoAPI
import getpass
import urllib
import json
 
# To order from WeoGeo, you need a username/password.  You can generate these at https://market.weogeo.com/register
 
USERNAME = raw_input("User email: ")

PASSWORD = getpass.getpass()
 
weos = WeoGeoAPI.weoSession('http://market.weogeo.com', USERNAME, PASSWORD)

	""" We need to create a JSON Job request.  More info can be found in our documentation: 
	http://www.weogeo.com/developer_doc/WeoGeo_API_Wrappers_Python.html#job_methods  
	In the returned JSON from the previous example, these options can be found in 
	the "job_parameters". """

weoOrder = {
    # may be either true or false 
    "cart" : "true",   
    "job" :
      {
        "dataset_token" : "a32957481fde138c22c38a680f2ec65",
 
        # must be 1 or it will not be accepted
        "content_license_acceptance" : "1", 
                 
        "parameters":   
        {
          "job_geocrop" : "Clip",             
          "job_north": "3995067.8436119 ",                 
          "job_south": "3980239.0603782 ",
          "job_east" : "-12386121.607448 ",
          "job_west" : "-12397931.128116 ",
          "job_layers": "layer_1",               
          "job_datum_projection" : "Native", 

          # FME name for file format
          "job_file_format": "Native",  

          # raster only         
          "job_spatial_resolution": "1"      
        }
      }
  }
 
# Connect
 
if weos.connectToMarket() is True:

	print "\nSubmitting your job...\n"
	
	weoJob = weos.createJob(weoOrder, 'JSON')
	
	print "Here is your order info:\n"
  
	# We pretty print the response
  
	print json.dumps(weoJob, indent=4)
 
# If connection fails, then exit and tell the user.
 
else:

  print "\nYou cannot connect to WeoGeo, check your Internet connection.\n"