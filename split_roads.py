import os
import os.path
import shutil
import osgeo.ogr
import osgeo.osr
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
            if cur_road.crosses(other_road):
                crossroads.append(other_road)
        if len(crossroads) > 0:
            for other_road in crossroads:
                cur_road = cur_road.difference(other_road)
            if cur_road.geom_type == "MultiLineString":
                for split_road in cur_road.geoms:
                    split_roads.append(split_road)
            elif cur_road.geom_type == "LineString":
                split_roads.append(cur_road)
        else:
            split_roads.append(cur_road)

    driver = ogr.GetDriverByName("ESRI Shapefile")
    if os.path.exists("split_roads"):
        shutil.rmtree("split_roads")
    os.mkdir("split_roads")
    dstFile = driver.CreateDataSource("split_roads/split_roads.shp")

    spatialReference = osgeo.osr.SpatialReference()
    spatialReference.SetWellKnownGeogCS("WGS84")

    layer = dstFile.CreateLayer("Layer", spatialReference)

    for road in split_roads:
        wkt = shapely.wkt.dumps(road)
        linestring = osgeo.ogr.CreateGeometryFromWkt(wkt)

        feature = osgeo.ogr.Feature(layer.GetLayerDefn())
        feature.SetGeometry(linestring)

        layer.CreateFeature(feature)
        feature.Destroy()

    dstFile.Destroy()
