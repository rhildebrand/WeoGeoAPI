"""
In this example we will demonstrate how to order a vector job with customization using
information we logged from the getdatasets_by_area.py example. The dataset used in this
example is "TIGER/Line State Based Files: OREGON", which can be found here:
http://market.weogeo.com/datasets/af85e6ee-c2b8-e554-975f-dca938d40bc3
"""

# Third Party Modules
import WeoGeoAPI

# Establish connection to WeoGeo Market
weos = WeoGeoAPI.weoSession('market.weogeo.com', 'username', 'password')
weos.connect()
print weos

# Set initial job parameters. The 'note' variable is optional. Datasets with no layers do not need to be specified.
newJob = WeoGeoAPI.weoJob(dataset_token = 'af85e6ee-c2b8-e554-975f-dca938d40bc3',
                        layers = ['Block', 'Census Tract'],
                        job_file_format = 'SHAPE',
                        note = 'Extract of area around Portland, OR.',
                        content_license_acceptance = True)

# Create a polygon selection using pairs of X,Y points that are in sequence.
newJob.setClipAreaCoordinateSystem('EPSG:4326')
newJob.addClipAreaPoints(((-122.55,45.43), (-122.46,45.43), (-122.14,45.32), (-122.14,45.27), (-122.55,45.27)))

# Create job object to be used for ordering.
response = weos.createJob(newJob)

# Pricing and size information
price = weos.getPrice(newJob)
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
