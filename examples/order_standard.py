"""
In this example we will demonstrate how to order a standard job using information we
logged from the getdatasets_by_area.py example. A job on a Standard listing delivers all data 
and therefore do not allow for customization. The dataset used in this example is "GNS World Waterbodies",
which can be found here: http://market.weogeo.com/datasets/9dc42e34-cbd0-6952-ad6c-fb39eb23fd0a
"""

# Third Party Modules
import WeoGeoAPI

# Establish connection to WeoGeo Market
weos = WeoGeoAPI.weoSession('market.weogeo.com', 'username', 'password')
weos.connect()
print weos

# Create job object. Since there is no customization involved we only need to supply the token accept the license.
testJob = WeoGeoAPI.job(datasetToken = '9dc42e34-cbd0-6952-ad6c-fb39eb23fd0a',
                        acceptLicense = True)

# Create job object to be used for ordering.
job_response, job_output = weos.createJob(testJob)

# Pricing and size information
response, price = weos.getPrice(testJob)
print "\n-Order Summary-"
print "Price: " + price['price']
print "Size:  " + price['human_estimated_data_size']

# Complete the order
if job_response != 201:
    print job_output
    exit(0)
else:
    order_response, order_output = weos.orderJob(job_output['token'])
    print "\n***Order finished. Check your e-mail for order confirmation details.***"
