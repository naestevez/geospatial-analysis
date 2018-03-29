import pyproj

geod = pyproj.Geod(ellps="WGS84")

#prompt user to enter desired coordinates
def get_coord(prompt):
    while True:
        s = raw_input(prompt + " (lat,long): ")
        if "," not in s: continue
        s1, s2 = s.split(",", 1)
        try:
            latitude = float(s1.strip())
        except ValueError:
            continue
        try: longitude = float(s2.strip())
        except ValueError:
            continue
        return latitude, longitude

lat1,long1 = get_coord("Starting coordinate")
lat2,long2 = get_coord("Ending coordinate")

#calculate distance between these two coordinates
heading1,heading2,distance = geod.inv(long1, lat1, long2, lat2)

print "Heading = %0.2f degrees" % heading1
print "Inverse heading = %0.2f degrees" % heading2
print "Distance = %0.2f kilometers" % (distance/1000)
