#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 25 09:21:38 2018

@author: Alex
"""

import osgeo.ogr
import psycopg2
import math

connection = psycopg2.connect(database="world_borders", user="postgres")
cursor = connection.cursor()

#add new field to hold buffered outline
try: 
    cursor.execute("ALTER TABLE borders ADD COLUMN buffered_outline GEOGRAPHY")
except psycopg2.ProgrammingError: #if column "outline" already exists
    connection.rollback() #allows program to continue despite raised exception
    
cursor.execute("UPDATE borders SET buffered_outline=ST_Buffer(outline, 1000)")

connection.commit()

cursor.execute("SELECT name, ST_Area(outline), ST_Area(buffered_outline) FROM borders ORDER BY name")

#checks for invalid outlines that is close to -180/180 degrees of longitude
for name, area1, area2 in cursor:
    if not math.isnan(area1):
        area1 = int(area1/1000000)
    else:
        area1 = "n/a"
    if not math.isnan(area2):
        area2 = int(area2/1000000)
    else:
        area2 = "n/a"
    print name, area1, area2 
    
cursor.execute("SELECT name, ST_AsText(outline) FROM borders")

#exports the spatial data into shapefile
for name, wkt in cursor:
    geometry = osgeo.ogr.CreateGeometryFromWkt(wkt)
    ...