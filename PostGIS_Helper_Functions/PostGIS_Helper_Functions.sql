-- Function: weogeo_buffer_returnfloat(double precision, double precision, double precision, double precision)

-- DROP FUNCTION weogeo_buffer_returnfloat(double precision, double precision, double precision, double precision);

CREATE OR REPLACE FUNCTION weogeo_buffer_returnfloat(west double precision, south double precision, east double precision, north double precision)
  RETURNS text AS
$BODY$
    swath = max(east-west, north-south)
    buffered_west = (east-west)/2+west - swath/2
    buffered_east = (east-west)/2+west + swath/2
    buffered_south = (north-south)/2+south - swath/2
    buffered_north = (north-south)/2+south + swath/2
    return buffered_west,buffered_south,buffered_east,buffered_north
$BODY$
  LANGUAGE plpythonu VOLATILE
  COST 100;
ALTER FUNCTION weogeo_buffer_returnfloat(double precision, double precision, double precision, double precision) OWNER TO postgres;


-- Function: weogeo_box2boundaries(integer, double precision, double precision, double precision, double precision)

-- DROP FUNCTION weogeo_box2boundaries(integer, double precision, double precision, double precision, double precision);

CREATE OR REPLACE FUNCTION weogeo_box2boundaries(epsg integer, xmin double precision, ymin double precision, xmax double precision, ymax double precision)
  RETURNS text AS
$BODY$
DECLARE
 bounds text;
 kml_bounds text;
 smxmin float;
 smymin float;
 smxmax float;
 smymax float;
 bx1 float;
 bx2 float;
 by1 float;
 by2 float;
 buftext text;
 bounds_str text;
 buffered text;
 swath float;
 buf_bounds_4326 text;
 buf_bounds_sm text;
BEGIN

        -- The KML Boundary is the data extent converted to Lat/Lon WGS84
	kml_bounds = AseWKT(ST_Envelope(ST_Transform(SetSRID(AseWKT(MakeBox2D(
		PointFromText('POINT('|| xmin ||' '||ymin||')',epsg),
		PointFromText('POINT('|| xmax ||' '||ymax||')',epsg)
		)),epsg),4326)));

	-- Step 1: Convert native to Spherical Mercator
	bounds = AseWKT(ST_Envelope(ST_Transform(SetSRID(AseWKT(MakeBox2D(
		PointFromText('POINT('|| xmin ||' '||ymin||')',epsg),
		PointFromText('POINT('|| xmax ||' '||ymax||')',epsg)
		)),epsg),900913)));

	-- Recalculating...Shouldn't use the Envelope in this step
	-- Step 1: Convert native to Spherical Mercator
	bounds = AseWKT(ST_Transform(SetSRID(AseWKT(MakeBox2D(
		PointFromText('POINT('|| xmin ||' '||ymin||')',epsg),
		PointFromText('POINT('|| xmax ||' '||ymax||')',epsg)
		)),epsg),900913));
		

	smxmin = ST_XMin(ST_Transform(SetSRID(AseWKT(MakeBox2D(
			PointFromText('POINT('|| xmin ||' '||ymin||')',epsg),
			PointFromText('POINT('|| xmax ||' '||ymax||')',epsg)
			)),epsg),900913));

	smymin = ST_YMin(ST_Transform(SetSRID(AseWKT(MakeBox2D(
			PointFromText('POINT('|| xmin ||' '||ymin||')',epsg),
			PointFromText('POINT('|| xmax ||' '||ymax||')',epsg)
			)),epsg),900913));

	smxmax = ST_XMax(ST_Transform(SetSRID(AseWKT(MakeBox2D(
			PointFromText('POINT('|| xmin ||' '||ymin||')',epsg),
			PointFromText('POINT('|| xmax ||' '||ymax||')',epsg)
			)),epsg),900913));

	smymax = ST_YMax(ST_Transform(SetSRID(AseWKT(MakeBox2D(
			PointFromText('POINT('|| xmin ||' '||ymin||')',epsg),
			PointFromText('POINT('|| xmax ||' '||ymax||')',epsg)
			)),epsg),900913));
			
        -- Step 2: Buffer the Spherical Mercator bounding box
        buftext = weogeo_buffer_returnfloat(smxmin, smymin, smxmax, smymax);
        bx1 = get_from_list(0,buftext);
        by1 = get_from_list(1,buftext);
        bx2 = get_from_list(2,buftext);
        by2 = get_from_list(3,buftext);

        -- Step 3: Convert the buffered box to Lat/Lon WGS84
        -- FixMe: Is Envelope required?
	--buf_bounds_4326 = AseWKT(ST_Envelope(ST_Transform(SetSRID(AseWKT(MakeBox2D(
	--	PointFromText('POINT('||bx1||' '||by1||')',900913),
	--	PointFromText('POINT('||bx2||' '||by2||')',900913)
	--	)),900913),4326)));
	buf_bounds_sm = AseWKT(SetSRID(AseWKT(MakeBox2D(
		PointFromText('POINT('||bx1||' '||by1||')',900913),
		PointFromText('POINT('||bx2||' '||by2||')',900913)
		)),900913));

	buf_bounds_4326 = AseWKT(ST_Transform(SetSRID(AseWKT(MakeBox2D(
		PointFromText('POINT('||bx1||' '||by1||')',900913),
		PointFromText('POINT('||bx2||' '||by2||')',900913)
		)),900913),4326));

        bounds_str = 
          E'KML Values for Tilemill:\n'
        ||kml_bounds
        ||E'\n\nKML Values for WeoApp:\n'
        ||bounds
        ||E'\n\nThumbnanil and Baseimage Values for Tilemill:\n'
        ||buf_bounds_4326
	||E'\n\nThumbnanil and Baseimage Values for WeoApp:\n'
	||buf_bounds_sm;
        
   RETURN bounds_str;
END;
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION 
weogeo_box2boundaries(
	integer, 
	double precision, 
	double precision, 
	double precision, 
	double precision) 
OWNER TO postgres;
