# This script is for creating database and its tables automatically.

import mysql.connector

loladb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "root!QAZ2wsx"
)

mycursor = loladb.cursor()
 
# Create database
query_db = "CREATE DATABASE IF NOT EXISTS website;"
mycursor.execute(query_db)

# Create tables
query_table_attraction = '''
                CREATE TABLE IF NOT EXISTS website.attraction(
                    id BIGINT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    category VARCHAR(255) NOT NULL,
                    description VARCHAR(10000),
                    address VARCHAR(255) NOT NULL,
                    transport VARCHAR(1500),
                    mrt VARCHAR(255),
                    latitude DOUBLE NOT NULL,
                    longitude DOUBLE NOT NULL,
                    time DATETIME NOT NULL DEFAULT NOW()
                );
               '''
query_table_image = '''
                    CREATE TABLE IF NOT EXISTS website.image(
                    id BIGINT AUTO_INCREMENT PRIMARY KEY,
                    attraction_id BIGINT NOT NULL,
                    image VARCHAR(255) NOT NULL,
                    time DATETIME NOT NULL DEFAULT NOW(),
                    FOREIGN KEY(attraction_id) REFERENCES attraction(id)
                );
                    '''
mycursor.execute(query_table_attraction)
mycursor.execute(query_table_image)