"""
In this example we will demonstrate how to order a standard job using information we
logged from the getdatasets_by_area.py example. A job on a Standard listing delivers all data 
and therefore do not allow for customization. The dataset used in this example is "GNS World Waterbodies",
which can be found here: http://market.weogeo.com/datasets/5416193f-ba3d-f45e-bd9c-6dbf8193bfad
"""

# Third Party Modules
import WeoGeoAPI

# Establish connection to WeoGeo Market
weos = WeoGeoAPI.weoSession('market.weogeo.com', 'username', 'password')
weos.connect()
print weos

# Create job object. Since there is no customization involved we only need to supply the token accept the license.
testJob = WeoGeoAPI.weoJob(dataset_token = '5416193f-ba3d-f45e-bd9c-6dbf8193bfad',
                           content_license_acceptance = True)

# Create job object to be used for ordering.
response = weos.createJob(testJob)

# Pricing and size information
price = weos.getPrice(testJob)
print "\n-Order Summary-"
print "Price: " + price.content['job_price']['price']
print "Size:  " + price.content['job_price']['human_estimated_data_size']

# Complete the order
if response.status != 201:
    print response.content
    exit(0)
else:
    response = weos.orderJob(response.content['job']['token'])
    print "\n***Order finished. Check your e-mail for order confirmation details.***"
