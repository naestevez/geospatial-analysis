import mapnik
from osgeo import gdal, ogr, osr
from shapely.wkt import dumps, loads
import os
from xml.etree import ElementTree as ET

def main():
    stylesheet = 'shapeToMap.xml'

    #asks what country does user want to see
    countryChosen = raw_input('Which country would you like to see? ')
    countryChosen = countryChosen.lower()

    #retrieves shapefile, assigns layer to variable, fetches srs for this layer
    shapefile = ogr.Open("TM_WORLD_BORDERS-0.3.shp")
    layer = shapefile.GetLayer()
    projection = layer.GetSpatialRef()

    #converts wkt to proj4, assigns srs to variable to be placed in xml stylesheet
    srs = osr.SpatialReference()
    srs.ImportFromWkt(projection.ExportToWkt())
    proj4_format = srs.ExportToProj4()

    #assigns srs attribute(in proj4 format) for map and layers in xml
    dom = ET.parse(stylesheet)
    root = dom.getroot()
    root.attrib['srs'] = proj4_format
    for child in root.findall('Layer'):
        child.attrib['srs'] = proj4_format

    #finds bounding box for a specific feature
    for i in range(layer.GetFeatureCount()):
        feature = layer.GetFeature(i)
        feature_name = feature.GetField("NAME")
        feature_name = feature_name.lower()
        if feature_name == countryChosen:
            geometry = feature.GetGeometryRef()
            wkt = geometry.ExportToWkt()
            outline = loads(wkt)


    #assign bounds of specific country to visible extent of map
    (BOUNDS_MIN_LONG, BOUNDS_MIN_LAT, BOUNDS_MAX_LONG, BOUNDS_MAX_LAT) = outline.bounds

    BACKGROUND_COLOR = '#a0c0ff'

    #variables for visible extent of map
    # BOUNDS_MIN_LAT = 35.26
    # BOUNDS_MAX_LAT = 71.39
    # BOUNDS_MIN_LONG = -10.90
    # BOUNDS_MAX_LONG = 41.13

    #max size of image - might be smaller than bounding rectangle
    MAX_WIDTH = 1600
    MAX_HEIGHT = 800

    #calculates max width/height of map so width is equal to max width of image(1600) and image height matches map height
    extent = mapnik.Envelope(BOUNDS_MIN_LONG, BOUNDS_MIN_LAT, BOUNDS_MAX_LONG, BOUNDS_MAX_LAT)
    aspectRatio = extent.width() / extent.height()

    mapWidth = MAX_WIDTH
    mapHeight = int(mapWidth / aspectRatio)

    #if map height is larger than image height, scale down both map width and height
    if mapHeight > MAX_HEIGHT:
        scaleFactor = float(MAX_HEIGHT) / float(mapHeight)
        mapWidth = int(mapWidth * scaleFactor)
        mapHeight = int(mapHeight * scaleFactor)

    #initialize map object
    map = mapnik.Map(mapWidth, mapHeight)
    map.background = mapnik.Color(BACKGROUND_COLOR)
    mapnik.load_map(map, stylesheet)

    #renders the map image
    map.zoom_to_box(extent)
    mapnik.render_to_file(map, "map.png", "png")

    #opens map
    os.system('open map.png')

if __name__ == "__main__":
    main()
