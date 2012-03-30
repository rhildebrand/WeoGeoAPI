import sys
from sqlalchemy import *
from sqlalchemy.orm import *

def call_box2boundaries(epsg,west,south,east,north):
    """
    """
    engine = create_engine('postgresql://postgres:postgres@localhost:5432/postgis', echo=True)
    engine.echo = True
    connection = engine.connect()
    rows = connection.execute(
        """
        SELECT weogeo_box2boundaries({0},{1},{2},{3},{4});
        """.format(epsg,west,east,south,north))
    for row in rows:
        return row.weogeo_box2boundaries
    

if __name__ == "__main__":
    #print call_box2boundaries(4326,-125.350914, 23.415519,-65.897631,49.813385)
    epsg = sys.argv[1]
    west = sys.argv[2]
    south = sys.argv[3]
    east = sys.argv[4]
    north = sys.argv[5]
    print call_box2boundaries(epsg,west,south,east,north)