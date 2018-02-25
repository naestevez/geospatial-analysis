#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 22:25:33 2018

@author: Alex
"""

import psycopg2

#connect to database and create cursor to run commands
connection = psycopg2.connect(database="world_borders", user="postgres")
cursor = connection.cursor()

#create database query
cursor.execute("SELECT id, name FROM borders ORDER BY name")
for row in cursor:
    print row

print "The following list are countries within 1000 kilometers of Paris:"
lat = 48.8567
longitude = 2.3508
radius = 1000000 #in meters

#ST_DWITHIN() function makes 3 parameters geometry 1(which is positive), geometry 2, distance
#ST_MakePoint() function take lat and long and makes a point
cursor.execute("SELECT name FROM borders WHERE ST_DWITHIN(" + "ST_MakePoint(%s, %s), outline, %s)", (longitude, lat, radius))

for row in cursor:
    print row[0]