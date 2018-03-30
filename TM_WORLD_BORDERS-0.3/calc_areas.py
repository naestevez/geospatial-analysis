from osgeo import ogr
import shapely.wkt
import shapely.ops
import pyproj

shapefile = ogr.Open("TM_WORLD_BORDERS-0.3.shp")
layer = shapefile.GetLayer(0)

src_proj = pyproj.Proj(proj="longlat", ellps="WGS84", datum="WGS84")
dst_proj = pyproj.Proj(proj="moll", lon_0=0, x_0=0, y_0=0, ellps="WGS84", datum="WGS84", units="m")

#transformation function
def latlong_to_mollweide(longitude, latitude):
    return pyproj.transform(src_proj, dst_proj, longitude, latitude)

#loops through each feature
for i in range(layer.GetFeatureCount()):
    feature = layer.GetFeature(i)
    wkt = feature.GetGeometryRef().ExportToWkt()
    geometry = shapely.wkt.loads(wkt)

    #use shapely to apply transformation to each coordinate in geometry (https://toblerity.org/shapely/shapely.html#module-shapely.ops)
    transformed = shapely.ops.transform(latlong_to_mollweide, geometry)

    #converts to square kilometers (uses .area shapely attribute)
    area = int(transformed.area/1000000)

    print feature.GetField("NAME"), area
