#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  2 11:41:31 2018

@author: Alex
"""

import osgeo.ogr
import shapely.wkt

def main():
    shapefile = osgeo.ogr.Open("TM_WORLD_BORDERS-0.3.shp")
    layer = shapefile.GetLayer(0)
    
    countries = {} #maps country name to shapely geometry
    
    for i in range(layer.GetFeatureCount()):
        feature = layer.GetFeature(i)
        country = feature.GetField("NAME")
        outline = shapely.wkt.loads(feature.GetGeometryRef().ExportToWkt())
        countries[country] = outline
        
    print "Loaded %d countries" %len(countries)
    
    for country in sorted(countries.keys()): #for each country
        outline = countries[country] #assign the shape object of country to outline
        
        for other_country in sorted(countries.keys()):
            if country == other_country: continue #if the country is the same as other_country, skip following code and return to beginning of outer for loop
            other_outline = countries[other_country] #assign the shape object of other_country to other_outline
            if outline.touches(other_outline): #uses touches method to compare outline of country and other_outline of other_country to find out if they are bordering eachother
                print "%s borders %s" % (country, other_country) #if they are, print it
    
if __name__ == "__main__":
    main()
    