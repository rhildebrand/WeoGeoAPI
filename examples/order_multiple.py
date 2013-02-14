"""
In this example we will demonstrate how to use the cart to order multiple datasets using
information that was logged from the getdatasets_by_area.py example. We will use the vector,
raster and standard datasets found in previous examples. We will log the job tokens for use
in another example to download the jobs.
"""

# Third Party Modules
import WeoGeoAPI

# Establish connection to WeoGeo Market
weos = WeoGeoAPI.weoSession('market.weogeo.com', 'username', 'password')
weos.connect()
print weos

# Create text file to log tokens
outfile = open('job_tokens.txt', 'w')

# Create lists for job instances and another list for their tokens
jobs = []
jobtokens = []

# Create standard job object and append to jobs list
standardJob = WeoGeoAPI.weoJob( datasetToken = '9dc42e34-cbd0-6952-ad6c-fb39eb23fd0a',
                                acceptLicense = True)
jobs.append(standardJob)

# Create vector job object and append to jobs list
vectorJob = WeoGeoAPI.weoJob( datasetToken = 'bfc2b36e-3d0d-4a6d-935d-e9ab090aaa3c',
                              layers = ['Area Hydrography', 'Linear Hydrography'],
                              outputFormat = 'SHAPE',
                              note = 'Extract of area around Portland, OR.',
                              acceptLicense = True )
vectorJob.setClipAreaCoordinateSystem( 'EPSG:4326' )                        
vectorJob.addClipAreaPoints((-122.55,45.43), (-122.46,45.43), (-122.14,45.32), (-122.14,45.27), (-122.55,45.27))
jobs.append(vectorJob)

# Create raster job object and append to jobs list
rasterJob = WeoGeoAPI.weoJob( datasetToken = '5dbdb7db-1acf-4f19-b629-04b54f907552',
                              layers = ['10m High Res'],
                              outputFormat = 'GeoTIFF',
                              coordinateSystem = 'EPSG:4269',
                              spatialResolution = '1',
                              note = 'Extract of area around Oregon.',
                              acceptLicense = True )
rasterJob.setBoxCropArea('EPSG:4326', 46.17, 42.13, -116.28, -124.33)
jobs.append(rasterJob)

# Create job objects and append the new job token to a list. Website response requires 201 to proceed.
for job in jobs:
    job_response, job_output = weos.createJob(job)
    if job_response == 201:
        jobtokens.append(job_output['parameters']['job_token'])
        response, price = weos.getPrice(job)
    else:
        print job_output
    print "\n-Job Summary-"
    print "Job Token: " + job_output['parameters']['job_token']
    print "Price: " + price['price']
    print "Size:  " + price['human_estimated_data_size']

# Move jobs to cart
print "\n-Adding jobs to cart-"
for token in jobtokens:
    weos.moveJobToCart(token)
    print token

# Order jobs in cart
order_response, order_results = weos.orderJobsInCart()

# Log job tokens to text file
for job in order_results['jobs']:
    outfile.writelines(job['token'] + '\n')

print "\n-Order completed: check e-mail for confirmation.-"

outfile.close()
