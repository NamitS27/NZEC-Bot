import psycopg2
import datetime as dt
import os


class Database:
    def __init__(self):
        self.connected = False
        self.connection = None

    def connect(self):
        try:
            dbname = os.environ.get('DATABASE_NAME')
            user = os.environ.get('DATABASE_USER')
            password = os.environ.get('DATABASE_PASS')
            host = os.environ.get('DATABASE_HOST')
            conn = psycopg2.connect(f"dbname='{dbname}' user='{user}' host='{host}' password='{password}'")
            self.connection = conn
            self.connected = True
        except:
            raise

    def insert(self,query):
        try:
            with self.connection as con:
                with self.connection.cursor() as cursor:
                    cursor.execute(query)
                    con.commit()
        except:
            raise

    def insert_server_det(self,server_id,user_id,cf_username):
        NOW = dt.datetime.now()
        query = f"INSERT INTO server_det(server_id,user_id,cf_username,last_updated_time) VALUES('{server_id}','{user_id}','{cf_username}','{NOW}')"
        self.insert(query)

    def add_resource(self,server_id,user_id,tags,rlink):
        NOW = dt.datetime.now()
        query = f"INSERT INTO resources(rlink,tags,server_id,discord_user_id,submission_time) VALUES('{rlink}','{tags}','{server_id}','{user_id}','{NOW}')"
        self.insert(query)

    def fetch_all(self,table_name):
        query = f"SELECT * from {table_name}"
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query)
                return cursor.fetchall()
        except:
            raise

    def get_server_users(self,server_id):
        query = f"SELECT * from server_det WHERE server_id='{server_id}'"
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query)
                return cursor.fetchall()
        except:
            raise

    def get_user_det(self,server_id,user_id):
        query = f"SELECT * from server_det WHERE server_id='{server_id}' and user_id='{user_id}'"
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query)
                return cursor.fetchall()
        except:
            raise

    def update_username(self,server_id,user_id,username):
        NOW = dt.datetime.now()
        query = f"UPDATE server_det SET cf_username='{username}',last_updated_time='{NOW}' WHERE server_id='{server_id}' and user_id='{user_id}'"
        try:
            with self.connection as con:
                with self.connection.cursor() as cursor:
                    cursor.execute(query)
                    con.commit()
        except:
            raise
