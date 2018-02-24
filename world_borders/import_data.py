#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 20:29:46 2018

@author: Alex
"""

import osgeo.ogr
import psycopg2

#create connection to database and cursor to make commands with
connection = psycopg2.connect(database="world_borders", user="postgres")
cursor = connection.cursor()

#delete any instances of the table
cursor.execute("DELETE FROM borders")

#assign shapefile and layer variables
shapefile = osgeo.ogr.Open("data/TM_WORLD_BORDERS-0.3.shp")
layer = shapefile.GetLayer(0)


#for each feature, get name, iso_code, geometry and assign to variables
for i in range(layer.GetFeatureCount()):
    feature = layer.GetFeature(i)
    name = feature.GetField("NAME")
    iso_code = feature.GetField("ISO3")
    geometry = feature.GetGeometryRef()
    #convert the geometry into wkt   
    wkt = geometry.ExportToWkt()
    #insert the data with cursor.execute 
    #ST_GeogFromText() converts WKT-format string into geography value before inserting into outline field
    #OGR and Postgres use different internal representations for geometry data 
    cursor.execute("INSERT INTO borders (name, iso_code, outline) VALUES (%s, %s, ST_GeogFromText(%s))", (name, iso_code, wkt))

#save the insertion
connection.commit()

    
