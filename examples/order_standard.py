"""
In this example we will demonstrate how to order a standard job using information we
logged from the getdatasets_by_area.py example. A job on a Standard listing delivers all data
and therefore do not allow for customization. The dataset used in this example is "NASA: Earth at Night - 2000",
which can be found here: http://market.trimbledata.com/#/datasets/5416193f-ba3d-f45e-bd9c-6dbf8193bfad
"""

import WeoGeoAPI

# Establish connection to Trimble Data Marketplace
session = WeoGeoAPI.weoSession('market.trimbledata.com', 'username', 'password')
session.connect()
print session

# Create job object. Since there is no customization involved we only need to supply the token accept the license.
testJob = WeoGeoAPI.weoJob(dataset_token='5416193f-ba3d-f45e-bd9c-6dbf8193bfad',
                           content_license_acceptance=True)

# Create job object to be used for ordering.
response = session.createJob(testJob)

# Pricing and size information
price = session.getPrice(testJob)
print "\n-Order Summary-"
print "Price: " + price.content['job_price']['price']
print "Size:  " + price.content['job_price']['human_estimated_data_size']

# Complete the order
if response.status != 201:
    print response.content
    exit(0)
else:
    response = session.orderJob(response.content['job']['token'])
    print "\n***Order finished. Check your e-mail for order confirmation details.***"
