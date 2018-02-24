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
