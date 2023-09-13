import psycopg2
from configparser import ConfigParser
from time import time

conn = None
db = {}
mycursor = None

base_location = "/home/cpdl/Assignments/VSC_Projects/iitroparassignments_1013/Sem2/Topics_in_AI/Assignment1/"

# Delegating the sensitive info to a .info file which has all the information needed to connect to database
def config(filename=(base_location+'database.ini'), section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file.'.format(section, filename))

# Connect to the PostgreSQL database server
def connect():
    try:
        # read connection parameters
        config()
        params = db
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**db)
        # create a cursor
        mycursor = conn.cursor()
        print('Connected to the PostgreSQL database.')
        return mycursor, conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

# close the communication with the PostgreSQL
def close(conn, mycursor):
    mycursor.close()
    if conn is not None:
        conn.close()
        print('Database connection closed.')

