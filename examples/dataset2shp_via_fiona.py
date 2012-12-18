import os,sys
from optparse import OptionParser
from osgeo import ogr
from fiona import collection
import WeoGeoAPI


FEATURE = {'id': '1','geometry': {'type': "Polygon", 'coordinates': [[(0.0, 0.0), (0.0, 1.0), (1.0, 1.0), (1.0, 0.0), (0.0, 0.0)]]}, 'properties': {'name': '','token':''}}

SCHEMA = {'geometry': 'Polygon', 'properties': {'name': 'str','token': 'str'}}

def get_options():
    parser = OptionParser()
    parser.add_option("-l", "--library", dest="library", 
                      help="Your library subdomain (example.weogeo.com)")
    #parser.add_option("-k", "--key", dest="key", 
    #                  help="API Key for your library.")
    parser.add_option("-u", "--username", dest="username", 
                      help="Library Admin username.")
    parser.add_option("-p", "--password", dest="password", 
                      help="Library Admin password.")
    return parser,parser.parse_args()

def get_connex(options):
    print "Trying to connect to library %s using username %s and password %s" % (options.library,options.username,options.password)
    weos = WeoGeoAPI.weoSession(options.library,options.username,options.password)
        
    result = weos.connect()        
    if not result:
        print "\nCould not connect to your library with the credentils that you supplied.\nPlease check #your credentials and the CLI syntax.\n"
        parser.print_help()
        sys.exit()

    return weos
    
    
if __name__ == "__main__":    
    
    parser,(options, args) = get_options()
    with collection("%s.shp" % options.library, "w", "ESRI Shapefile", SCHEMA) as c:    
        weos = get_connex(options)
        n_pages = weos.getDatasets("JSON")
        feature_cnt = 0
        for page in range(1,n_pages[1]["total_pages"]+1): # for each page in the results
            print "Getting API page #%s of %s" % (page,n_pages[1]["total_pages"]+1)
            items = weos.getDatasets("JSON","&page=%s" % page)[1]["items"]
            
            for item in items: # for each item in a page
                feature_cnt += 1
                
                f = {'id': '1','geometry': {'type': "Polygon", 'coordinates': [[(0.0, 0.0), (0.0, 1.0), (1.0, 1.0), (1.0, 0.0), (0.0, 0.0)]]}, 'properties': {'name': '','token':''}}
                
                f['id'] = str(feature_cnt) #Fiona record ids are usually string representations of integer record indexes.
                # if additional attributes are added here, be sure to add them to the schema too.
                f['properties']['name'] = item['name']
                f['properties']['token'] = item["token"]

                west = float(item['boundaries']['geo']['west'])
                south = float(item['boundaries']['geo']['south'])
                east = float(item['boundaries']['geo']['east'])
                north = float(item['boundaries']['geo']['north'])

                f['geometry']['coordinates'][0][0] = (west, south) 
                f['geometry']['coordinates'][0][1] = (west, north)
                f['geometry']['coordinates'][0][2] = (east, north)
                f['geometry']['coordinates'][0][3] = (east, south)
                f['geometry']['coordinates'][0][4] = (west, south)
                
                c.write(f)

        


        
