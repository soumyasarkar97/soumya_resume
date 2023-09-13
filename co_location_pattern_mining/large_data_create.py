import csv
import connection as cn
import random
import os

e_type_name = ['A', 'B', 'C', 'D', 'E']
mycursor = None
conn = None

#connect to database
def connect():
    mycursor, conn = cn.connect()
    return mycursor, conn

#disconnect from database
def disconnect(mycursor, conn):
    cn.close(conn, mycursor)

#creates base tables for each attribute using script
def create_table(mycursor, conn):
    base_location = cn.base_location
    mycursor.execute(open((base_location+"large_tables.sql"), "r").read())
    conn.commit()

#inserts particular (x,y) data into base tables
def insert_data(mycursor, id, x, y, e_type):
    try:
        point = 'SRID=4326;POINT(' + x + ' ' + y +')'
        table_name = '"large_' + e_type_name[e_type] + '"'
        query = 'INSERT INTO "TiAI_Assignment1_InputData_Large".' + table_name + ' VALUES(%s, %s);'
        mycursor.execute(query, (id, point))
    except Exception as err:
        print('Could not insert value ({0},{1},{2},{3}) into database.'.format(id,x,y,e_type))
        print(err)

#generates the input file
def create_file(size):
    rows=[]
    minx = 28.457523
    maxx = 28.984644
    miny = 77.026344
    maxy = 77.705956
    for i in e_type_name:
        for j in range(size):
            rows.append([i+str(j+1), random.uniform(miny, maxy), random.uniform(minx, maxx)])
    base_location = cn.base_location
    filename = base_location+"large_data_points.csv"
    # writing to csv file
    if os.path.exists(filename):
        os.remove(filename)
    with open(filename, 'w') as csvfile: 
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)           
        # writing the data rows
        csvwriter.writerows(rows)

#reads file and inserts all  data into base tables
def read_file(mycursor, filename=(cn.base_location+"large_data_points.csv")):
    # opening the CSV file
    csvFile = csv.reader(open(filename, mode ='r'))
    
    # displaying the contents of the CSV file
    for line in csvFile:
        #format is id, longtitude, latitude
        x = str(line[1])
        y = str(line[2])
        id = line[0]
        e_type = 0 #default is event A
        if(id[0]=='A'):
            e_type = 0
        elif(id[0]=='B'):
            e_type = 1
        elif(id[0]=='C'):
            e_type = 2
        elif(id[0]=='D'):
            e_type = 3
        elif(id[0]=='E'):
            e_type = 4
        insert_data(mycursor, id, x, y, e_type)

#main function for this file
def main_method():
    #connect to database
    mycursor, conn = connect()
    #create tables
    create_table(mycursor, conn)
    #create data
    # create_file(100)
    #read data and save in database
    read_file(mycursor)
    #commit
    conn.commit()
    #close the connection
    disconnect(mycursor, conn)

main_method()