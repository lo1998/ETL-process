#importing libraries
import mariadb
import sys
import pandas as pd
import numpy as np
#read the cleaning csv file
df = pd.read_csv('cleaned_data1.csv')
# Try to establish a connection to the MariaDB database
try:
 conn = mariadb.connect(
 user="cip_user",
 password="cip_pw",
 host="127.0.0.1",
 port=3306,
 database="CIP"
 )
except mariadb.Error as e:
 print(f"Error connecting to MariaDB Platform: {e}")
 sys.exit(1)
# Create a cursor object using the connection
cur = conn.cursor()

# SQL query to create a new table if it doesn't already exist
create_table_query = """
CREATE TABLE IF NOT EXISTS your_table_name (
    Rank INT,
    IMDB_Rating FLOAT,
    Director VARCHAR(255),
    Metascore INT,
    Release_Year INT,
    Duration FLOAT,
    Title VARCHAR(255),
    IMDB_Rating_Scaled_Up INT,
    Movie_Age INT
);
"""
# Prepare the data to be inserted into the table
data_to_insert = [tuple(row) for row in df.values]
# Execute the table creation query
cur.execute(create_table_query)
# SQL query to insert data into the table
insert_query = """
INSERT INTO your_table_name (Rank, IMDB_Rating, Director, Metascore, Release_Year, Duration, Title, IMDB_Rating_Scaled_Up, Movie_Age)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
"""
try:
    cur.executemany(insert_query, data_to_insert)
    conn.commit()
except mariadb.Error as e:
    print(f"Error: {e}")

# SQL query to retrieve data from the table
cur.execute("SELECT Rank, IMDB_Rating, Director, Metascore, Release_Year, Duration, Title, IMDB_Rating_Scaled_Up, Movie_Age FROM your_table_name")
# print each row of the table
for (Rank, IMDB_Rating, Director, Metascore, Release_Year, Duration, Title, IMDB_Rating_Scaled_Up, Movie_Age) in cur:
 print(Rank, IMDB_Rating, Director, Metascore, Release_Year, Duration, Title, IMDB_Rating_Scaled_Up, Movie_Age)
# close the database connection
conn.close()
