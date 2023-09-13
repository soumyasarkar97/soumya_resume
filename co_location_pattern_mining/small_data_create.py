import csv
import connection as cn

e_type_name = ['A', 'B', 'C']

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
    mycursor.execute(open((base_location+"small_tables.sql"), "r").read())
    conn.commit()

#inserts particular (x,y) data into base tables
def insert_data(mycursor, id, x, y, e_type):
    try:
        point = 'SRID=4326;POINT(' + x + ' ' + y +')'
        table_name = '"small_' + e_type_name[e_type] + '"'
        query = 'INSERT INTO "TiAI_Assignment1_InputData_Small".' + table_name + ' VALUES(%s, %s);'
        mycursor.execute(query, (id, point))
    except Exception as err:
        print('Could not insert value ({0},{1},{2},{3}) into database.'.format(id,x,y,e_type))
        print(err)

#reads file and inserts all  data into base tables
def read_file(mycursor, filename=(cn.base_location+"small_data_points.csv")):
    # opening the CSV file
    csvFile = csv.reader(open(filename, mode ='r'))
    
    # displaying the contents of the CSV file
    for line in csvFile:
        #input is in the form: id, longtitude, latitude
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
        insert_data(mycursor, id, x, y, e_type)

#main function for this file
def main_method():
    #connect to database
    mycursor, conn = connect()
    #create tables
    # create_table(mycursor, conn)
    #read data and save in database
    read_file(mycursor)
    #commit
    conn.commit()
    #close the connection
    cn.close(conn, mycursor)
    print("Values inserted for small dataset.")

main_method()