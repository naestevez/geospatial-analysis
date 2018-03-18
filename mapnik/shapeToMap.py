import mapnik
from osgeo import gdal, ogr
from shapely.wkt import dumps, loads

countryChosen = raw_input('Which country would you like to see? ')
countryChosen = countryChosen.lower()
print countryChosen

#find bounding box for a specific feature
shapefile = ogr.Open("TM_WORLD_BORDERS-0.3.shp")
layer = shapefile.GetLayer(0)

for i in range(layer.GetFeatureCount()):
    feature = layer.GetFeature(i)
    feature_name = feature.GetField("NAME")
    feature_name = feature_name.lower()
    if feature_name == countryChosen:
        geometry = feature.GetGeometryRef()
        wkt = geometry.ExportToWkt()
        outline = loads(wkt)
        print(outline.bounds) #(min_x, min_y, max_x, max_y)

#assign bounds of specific country to visible extent of map
(BOUNDS_MIN_LONG, BOUNDS_MIN_LAT, BOUNDS_MAX_LONG, BOUNDS_MAX_LAT) = outline.bounds

stylesheet = 'shapeToMap.xml'

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
