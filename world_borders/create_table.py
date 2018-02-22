import psycopg2

#set up connection to database
connection = psycopg2.connect(database="world_borders", user="postgres")

#allows commands to the database
cursor = connection.cursor()

#deletes table if it exists - lets the program to be run multiple times w/o errors
#.execute() runs SQL demand
cursor.execute("DROP TABLE IF EXISTS borders")

#create table borders and 4 fields
cursor.execute("CREATE TABLE borders (" +
                "id SERIAL PRIMARY KEY," +
                "name VARCHAR NOT NULL," +
                "iso_code VARCHAR NOT NULL," +
                "outline GEOGRAPHY)")

#creates spatial index for outline field
cursor.execute("CREATE INDEX border_index ON borders USING GIST(outline)")

#save the changes permanently
connection.commit()

