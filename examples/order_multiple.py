"""
In this example we will demonstrate how to use the cart to order multiple datasets using
information that was logged from the getdatasets_by_area.py example. We will use the vector,
raster and standard datasets found in previous examples. We will log the job tokens for use
in another example to download the jobs.
"""

import WeoGeoAPI

# Establish connection to Trimble Data Marketplace
session = WeoGeoAPI.weoSession('market.trimbledata.com', 'username', 'password')
session.connect()
print session

# Create text file to log tokens
outfile = open('job_tokens.txt', 'w')

# Create lists for job instances and another list for their tokens
jobs = []
jobtokens = []

# Create standard job object and append to jobs list
standardJob = WeoGeoAPI.weoJob(dataset_token='5416193f-ba3d-f45e-bd9c-6dbf8193bfad',
                               content_license_acceptance=True)
jobs.append(standardJob)

# Create vector job object and append to jobs list
vectorJob = WeoGeoAPI.weoJob(dataset_token='3d52ffef-50cf-41e5-aadf-a5ec3dc5fc11',
                             layers=['All Roads', 'Census Tract'],
                             job_file_format='SHAPE',
                             note='Extract of area around Portland, OR.',
                             content_license_acceptance=True)
vectorJob.setClipAreaCoordinateSystem('EPSG:4326')
vectorJob.addClipAreaPoints(((-122.55, 45.43), (-122.46, 45.43), (-122.14, 45.32), (-122.14, 45.27), (-122.55, 45.27)))
jobs.append(vectorJob)

# Create raster job object and append to jobs list
rasterJob = WeoGeoAPI.weoJob(dataset_token='5dbdb7db-1acf-4f19-b629-04b54f907552',
                             layers=['10m High Res'],
                             job_file_format='GeoTIFF',
                             job_datum_projection='EPSG:4269',
                             job_spatial_resolution='1',
                             note='Extract of area around Oregon.',
                             content_license_acceptance=True)
rasterJob.setBoxCropArea('EPSG:4326', 46.17, 42.13, -116.28, -124.33)
jobs.append(rasterJob)

# Create job objects and append the new job token to a list. Website response requires 201 to proceed.
for job in jobs:
    response = session.createJob(job)
    if response.status == 201:
        jobtokens.append(response.content['job']['parameters']['job_token'])
        price = session.getPrice(job)
    else:
        print job, response.content
    print "\n-Job Summary-"
    print "Job Token: " + response.content['job']['parameters']['job_token']
    print "Price: " + price.content['job_price']['price']
    print "Size:  " + price.content['job_price']['human_estimated_data_size']

# Move jobs to cart
print "\n-Adding jobs to cart-"
for token in jobtokens:
    session.moveJobToCart(token)
    print token

# Order jobs in cart
response = session.orderJobsInCart()

# Log job tokens to text file
for job in response.content['order']['jobs']:
    outfile.writelines(job['token'] + '\n')

print "\n-Order completed: check e-mail for confirmation.-"

outfile.close()
