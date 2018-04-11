import os
import os.path
import shutil
from osgeo import ogr, osr
from shapely import wkt

SRC_SHAPEFILE = "tl_2017_06_prisecroads.shp"

all_roads = []
shapefile = ogr.Open("SRC_SHAPEFILE")

#load lineString geometries into all_roads list
layer = shapefile.GetLayer(0)
for i in range(layer.GetFeatureCount()):
    feature = layer.GetFeature(i)
    wkt = feature.GetGeometryRef().ExportToWkt()
    geometry = shapely.wkt.loads(wkt)
    all_roads.append(geometry)

    #split roads at intersection points
    split_roads = []

    for i in range(len(all_roads)):
        cur_road = all_roads[i]
        crossroads = []
        for j in range(len(all_roads)):
            if i == j: continue
            other_road = all_roads[j]
            # shapely .crosses() identifies other_road if intersects with cur_road & appends to crossroads
            if cur_road.crosses(other_road):
                crossroads.append(other_road)
        if len(crossroads) > 0:
            #crossroad is removed from cur_road .difference() #https://toblerity.org/shapely/manual.html#object.difference
            for other_road in crossroads:
                cur_road = cur_road.difference(other_road)
            if cur_road.geom_type == "MultiLineString":
                #.geoms - sequence of shapely geomtery instances
                for split_road in cur_road.geoms:
                    split_roads.append(split_road)
            elif cur_road.geom_type == "LineString":
                split_roads.append(cur_road)
        else:
            split_roads.append(cur_road)

    driver = ogr.GetDriverByName("ESRI Shapefile")
    #removes split_roads directory if it exists
    if os.path.exists("split_roads"):
        shutil.rmtree("split_roads")
    #makes the split_roads directory & destination shapefile
    os.mkdir("split_roads")
    dstFile = driver.CreateDataSource("split_roads/split_roads.shp")

    spatialReference = osgeo.osr.SpatialReference()
    spatialReference.SetWellKnownGeogCS("WGS84")
    #sets a spatialReference to a created layer
    layer = dstFile.CreateLayer("Layer", spatialReference)

    for road in split_roads:
        #dumps a WKT representation of a geometry to a wkt string
        wkt = shapely.wkt.dumps(road)
        #creates a geometry from the wkt string
        linestring = osgeo.ogr.CreateGeometryFromWkt(wkt)
        #create an OGR feature object
        feature = osgeo.ogr.Feature(layer.GetLayerDefn())
        #sets the geometry to each feature
        feature.SetGeometry(linestring)
        #assigns the feature object as a feature for the layer
        layer.CreateFeature(feature)
        #removes feature
        feature.Destroy()
    #removes the new shapefile
    dstFile.Destroy()
