"""
In this example we will demonstrate how to order a raster job with customization using
information we logged from the getdatasets_by_area.py example. The dataset used in this
example is "Natural Earth Shaded Relief", which can be found here:
http://market.weogeo.com/datasets/5dbdb7db-1acf-4f19-b629-04b54f907552
"""

# Third Party Modules
import WeoGeoAPI

# Establish connection to WeoGeo Market
weos = WeoGeoAPI.weoSession('market.weogeo.com', 'username', 'password')
weos.connect()
print weos

# Set initial job parameters. The 'note' variable is optional. Here we only want one layer, '10m High Res'.
# Spatial resolution is 1 (native). Use 2, 3 or 4 to deliver as 2x/3x/4x coarser.
# Reproject our order to NAD83-Geo(EPSG:4269).
newJob = WeoGeoAPI.weoJob(dataset_token = '5dbdb7db-1acf-4f19-b629-04b54f907552',
                          layers = ['10m High Res'],
                          job_file_format = 'GeoTIFF',
                          job_datum_projection = 'EPSG:4269',
                          job_spatial_resolution = '1',
                          note = 'Extract of area around Oregon.',
                          content_license_acceptance = True)

# Set crop box around Oregon. EPSG must be GEO(EPSG:4326) or Spherical Mercator(EPSG:3857).
newJob.setBoxCropArea('EPSG:4326', 46.17, 42.13, -116.28, -124.33)

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
