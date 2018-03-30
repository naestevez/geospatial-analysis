from osgeo import ogr
import shapely.wkt
import pyproj

geod = pyproj.Geod(ellps="WGS84")

shapefile = ogr.Open("tl_2017_06_prisecroads.shp")
layer = shapefile.GetLayer(0)

for i in range(layer.GetFeatureCount()):
    feature = layer.GetFeature(i)
    geometry = shapely.wkt.loads(feature.GetGeometryRef().ExportToWkt())

    #calculates length(meters) of all primary and secondary roads in California
    total_length = 0
    prev_long, prev_lat = geometry.coords[0] #takes first coodinates
    for cur_long, cur_lat in geometry.coords[1:]: #loops through all coordinates
        #calculates heading, inverse heading, and distance of each line
        heading1, heading2, distance = geod.inv(prev_long, prev_lat, cur_long, cur_lat)
        total_length = total_length + distance #stores distance of each line in total_length
        prev_long, prev_lat = cur_long, cur_lat #assigns current coordinates to previous coordinates

    print feature.GetField("FULLNAME"), int(total_length), geometry.geom_type

#the length of the perimeter of a polygon can be calculated by looping through: polygon.exterior
