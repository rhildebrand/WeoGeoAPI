from fiona import collection
from osgeo import ogr

FEATURE = {'id': '1', 
           'geometry': 
             {'type': 'Polygon', 
              'coordinates': [[(-1.0, -1.0), 
                               (-1.0, 1.0), 
                               (1.0, 1.0), 
                               (1.0, -1.0), 
                               (-1.0, -1.0)]]
             },
           'properties': {'name': '',
                          'token':''}
          }
SCHEMA = {'geometry': 'Polygon', 'properties': {'name': 'str','token': 'str'}}

with collection("a_shp_by_fiona.shp", "w", "ESRI Shapefile", SCHEMA) as c:
    for i in range(1,6):
        f = FEATURE.copy()
        f['id'] = str(i)
        c.write(f)
