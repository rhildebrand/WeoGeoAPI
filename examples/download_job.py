"""
In this example we will demonstrate how obtain the download link for a job order using
information that was logged from the order_multiple.py example. Important note: download
links are only valid for 7 days after the job has been ordered.
"""

# Third Party Modules
import WeoGeoAPI

# Establish connection to WeoGeo Market
weos = WeoGeoAPI.weoSession('market.weogeo.com', 'username', 'password')
weos.connect()
print weos

# List of job tokens pulled from previous example
jobtokens = ['c6c89bce-c633-4fe3-814f-61265d3324a6',
             '3ea0b1c7-0c09-44b5-a7fe-b183b4e8ab76',
             '8d0a9080-3bcc-426a-b367-585ee8d01161']

# Get download link for each job
for token in jobtokens:
    response = weos.getDownloadFile(token)
    for item in response.content:
        print item['url']

print "\nAll download links displayed."