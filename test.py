import psycopg2
import os

global conn

try:
    dbname = os.environ.get('DATABASE_NAME')
    user = os.environ.get('DATABASE_USER')
    password = os.environ.get('DATABASE_PASS')
    host = os.environ.get('DATABASE_HOST')
    conn = psycopg2.connect(f"dbname='{dbname}' user='{user}' host='{host}' password='{password}'")
except:
    print("ERROR :(")

cur = conn.cursor()


query = """
CREATE TABLE resources(
    rid serial PRIMARY KEY,
    rlink VARCHAR ( 2000 ) UNIQUE NOT NULL,
    tags VARCHAR ( 1000 ) NOT NULL,
    server_id VARCHAR(1000) UNIQUE NOT NULL,
    discord_user_id VARCHAR( 1000 ) NOT NULL,
    submission_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    accepted BOOLEAN DEFAULT FALSE,
    checked BOOLEAN DEFAULT FALSE
);

CREATE TABLE server_det(
    sd_id serial PRIMARY KEY,
    server_id VARCHAR(1000) NOT NULL,
    user_id VARCHAR(1000) NOT NULL,
    cf_username VARCHAR(500) NOT NULL,
    last_updated_time TIMESTAMP NOT NULL,
    UNIQUE (server_id,user_id)
);
"""

del_query = """DROP TABLE resources;
DROP TABLE server_det;"""
# cur.execute(del_query)
cur.execute(query)
conn.commit()


