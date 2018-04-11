"""
Created on Tue Feb 13 10:31:28 2018

@author: Alex
"""

import osgeo.ogr
import osgeo.osr

driver = osgeo.ogr.GetDriverByName("ESRI Shapefile")
destFile = driver.CreateDataSource("test-shapefile")

spatialReference = osgeo.osr.SpatialReference()
spatialReference.SetWellKnownGeogCS("WGS84") #WGS84 - standard for lat and long

layer = destFile.CreateLayer("layer", spatialReference)

#create attribute and store in layer
field = osgeo.ogr.FieldDefn("NAME", osgeo.ogr.OFTString)
field.setWidth(100)
layer.CreateField(field)

#define simple polygon
wkt = "POLYGON((23.4 38.9, 23.5 38.9, 23.5 38.8, 23.4 38.9))"
polygon = osgeo.ogr.CreateGeometryFromWkt(wkt)

feature = osgeo.ogr.Feature(layer.GetLayerDefn())
feature.SetGeometry(polygon)
feature.SetField("NAME", "My Polygon")

layer.CreateFeature(feature)
feature.Destroy()

destFile.Destroy()
