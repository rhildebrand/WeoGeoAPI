"""
In this example we will demonstrate how to order a vector job with customization using
information we logged from the getdatasets_by_area.py example. The dataset used in this
example is "TIGER/Line Water Boundaries - Oregon", which can be found here:
http://market.weogeo.com/datasets/bfc2b36e-3d0d-4a6d-935d-e9ab090aaa3c
"""

# Third Party Modules
import WeoGeoAPI

# Establish connection to WeoGeo Market
weos = WeoGeoAPI.weoSession('market.weogeo.com', 'username', 'password')
weos.connect()
print weos

# Set initial job parameters. The 'note' variable is optional. Datasets with no layers do not need to be specified.
newJob = WeoGeoAPI.job(datasetToken = 'bfc2b36e-3d0d-4a6d-935d-e9ab090aaa3c',
                        layers = ['Area Hydrography', 'Linear Hydrography'],
                        outputFormat = 'SHAPE',
                        note = 'Extract of area around Portland, OR.',
                        acceptLicense = True)

# Create a polygon selection using pairs of X,Y points that are in sequence.
newJob.setClipAreaCoordinateSystem( 'EPSG:4326' )   
newJob.addClipAreaPoints( [(-122.55,45.43), (-122.46,45.43), (-122.14,45.32), (-122.14,45.27), (-122.55,45.27)] )

# Create job object to be used for ordering.
job_response, job_output = weos.createJob(newJob)

# Pricing and size information
response, price = weos.getPrice(newJob)
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
