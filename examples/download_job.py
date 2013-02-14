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
jobtokens = ['69add159-01fa-4d84-8b83-f34692f582ec',
             '4b278ed3-3674-425a-8106-eba5a2875de8',
             '073dd749-2f04-41fa-911d-c90e8a3c098f']

# Get download link for each job
for token in jobtokens:
    response, result = weos.getDownloadFile(token)
    for item in result:
        print item['url']

print "\nAll download links displayed."