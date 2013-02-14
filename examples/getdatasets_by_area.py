"""
For this example we will show you how to get a list of free datasets available inside of a bounding box 
with supplied north, south, east and west coordinates on the WeoGeo Market and log the results to 
a CSV file.
"""

# First Party Modules
import csv
import json
# Third Party Modules
import WeoGeoAPI

# Establish connection to WeoGeo Market
weos = WeoGeoAPI.weoSession('market.weogeo.com', 'username', 'password')
weos.connect()
print weos

# Create CSV file to log our results
outfile = open('tokenlist.csv', 'wb')
writer = csv.writer(outfile)
headers = ['token', 'name', 'max_price', 'data_type','data_files_size', 
           'file_format', 'north', 'south', 'east', 'west','layers']
writer.writerow(headers)

# List for datasets returned from parameters supplied
datasets = []
page = 1

# Parse through page of results (15 per page) and log any free datasets.
while True:
    response, results = weos.getDatasets('JSON',
                                         'page={}'.format(page),
                                         'north=45.39', 'south=45.21', 'east=-122.27', 'west=-122.46')
    if page > results['total_pages']:
        print '\n***Finished processing***'
        break
    else:
        print 'Processing page {} of {}'.format(page, results['total_pages'])
        for item in results['items']:
            if item['max_price'] == 0.0:
                datasets.append([item['token'],
                                 item['name'],
                                 item['max_price'],
                                 item['data_type'],
                                 item['data_files_size'],
                                 item['file_format'],
                                 item['north'],
                                 item['south'],
                                 item['east'],
                                 item['west'],
                                 json.dumps(item['layers']).lstrip('[').rstrip(']')])
        page += 1

for dataset in datasets:
    writer.writerow(dataset)

outfile.close()
