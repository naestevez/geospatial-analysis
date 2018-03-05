import mapnik
stylesheet = 'shapeToMap.xml'

BACKGROUND_COLOR = '#a0c0ff'

#variables for visible extent of map
BOUNDS_MIN_LAT = 35.26
BOUNDS_MAX_LAT = 71.39
BOUNDS_MIN_LONG = -10.90
BOUNDS_MAX_LONG = 41.13

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
