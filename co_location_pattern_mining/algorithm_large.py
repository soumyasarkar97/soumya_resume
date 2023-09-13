import connection as cn
from prettytable import PrettyTable
from prettytable import from_db_cursor
import sys
import os.path  

#all output is to be found at output_large.txt
sys.stdout = open((cn.base_location+"output_large.txt"), "wt")

table_dict = {}
all_table_dict = {} #keeps track of all tables, empty or not
query_dict = {}

################## CONNECTION FUNCTIONS ##################
#connect to database
def connect():
    mycursor, conn = cn.connect()
    return mycursor, conn

#disconenct from database
def disconnect(mycursor, conn):
    cn.close(conn, mycursor)






################## UTILITY FUNCTIONS ##################
#generate all combinations of 2 using some pattern
def generate_patterns2(pattern):
    combinations=[]
    length = len(pattern)
    # pattern format => patterns[t] = [a, b] where a<b, and a-b is the pattern
    for i in range(1, length+1):
        for j in range(i+1, length+1):
            pattern2 = []
            pattern2.append(i)
            pattern2.append(j)
            combinations.append(pattern2)
    return combinations

#for size k, find k-1 size patterns
def k_minus_one_finder(pattern):
    all_subs = []
    length = len(pattern)
    if(length==1):
        all_subs.append(pattern)
        return all_subs
    for i in range(len(pattern)):
        all_subs.append(pattern[0:i]+pattern[i+1:length])
    return all_subs

#for pattern find its total subset => RETURN set
def subset_finder(pattern):
    arr_pattern=k_minus_one_finder(pattern)
    arr_pattern = tuple(arr_pattern)
    arr=set()
    if(len(arr_pattern)==1):
        arr = set(arr_pattern)
        return arr
    for sub in arr_pattern:
        x= subset_finder(sub)
        arr = arr.union(x)

    pattern_list = []
    pattern_list.append(pattern)
    pattern_set = set(pattern_list)
    arr = arr.union(pattern_set)
    return arr

#for pattern find its total subset and return 2D list, each 1D list containing all  elements of size (index+1) => RETURNS list
def sublist_finder(pattern):
    subset=subset_finder(pattern)
    arr = []
    length = len(pattern)
    for i in range(length):
        arr.append([])
    for i in subset:
        arr[len(i)-1].append(i)
    return arr

################## QUERY FUNCTIONS ##################

##### UTILITY QUERIES #####
#create table with name as "pattern". Ex: Table AB is created for pattern "AB"
def create_table(pattern, mycursor, conn):
    query = '''CREATE TABLE IF NOT EXISTS "TiAI_Assignment1_InputData_Large"."'''+pattern+'''"
    ( '''
    for i in range(len(pattern)):
        query = query + pattern[i] + '''_id character varying,
         '''
    query = query + '''PRIMARY KEY('''
    for i in range(len(pattern)):
        if(i<len(pattern)-1):
            query = query + pattern[i] + '''_id, '''
        else:
            query = query + pattern[i] + '''_id'''
    query = query+''')
    );
    ALTER TABLE IF EXISTS "TiAI_Assignment1_InputData_large"."'''+pattern+'''"
    OWNER to postgres;'''
    mycursor.execute(query)
    conn.commit()

#create spatial index on all tables
def create_index_all(pattern, mycursor, conn):
    for i in range(len(pattern)):
        query = '''CREATE INDEX IF NOT EXISTS '''+pattern[i]+'''_index 
        ON "TiAI_Assignment1_InputData_Large"."large_'''+pattern[i]+'''"
        USING GIST(lat_long);'''
        mycursor.execute(query)
        conn.commit()

#drop spatial index on all tables
def drop_index_all(pattern, mycursor, conn):
    for i in range(len(pattern)):
        query = '''DROP INDEX IF EXISTS "TiAI_Assignment1_InputData_Large"."'''+pattern[i].lower()+'''_index";'''
        mycursor.execute(query)
        conn.commit()

#delete any tables except single tables -> TO BE USED AT START
def delete_init(pattern, mycursor, conn):
    sub_patterns = k_minus_one_finder(pattern)
    if(len(pattern)==1):
        return
    query = '''DROP TABLE IF EXISTS "TiAI_Assignment1_InputData_Large"."'''+pattern+'''";'''
    mycursor.execute(query)
    conn.commit()
    for p in sub_patterns:
        delete_init(p, mycursor, conn)

#delete all tables in all_table_dict (FINAL CLEAR OF TEMPORARY TABLES)
def delete_fin(mycursor, conn):
    for table in all_table_dict:
        query = '''DROP TABLE IF EXISTS "TiAI_Assignment1_InputData_Large"."'''+table+'''";'''
        mycursor.execute(query)
        conn.commit()

#generates queries to call tables in table_dict
def add_query(pattern, table_name):
    query_dict[pattern] = '''SELECT * FROM ''' + table_name

#truncate table with name as pattern
def truncate_table(mycursor, conn, pattern):
    query = '''TRUNCATE "TiAI_Assignment1_InputData_Large"."'''+pattern+'''";'''
    mycursor.execute(query)
    conn.commit()

# used for printing the data
def print_table(mycursor, conn, pattern):
    print("\nTable "+ pattern + " with participation index = "+str(participation_index(mycursor, pattern)))
    query = '''SELECT '''
    for i in range(len(pattern)):
        query = query + pattern[i]+"_id" #Ex: a_id
        if(i<len(pattern)-1):
            query = query + ", " #Adds a comma if more columns remaining, else ignores comma
    query = query + ''' FROM "TiAI_Assignment1_InputData_Large"."'''+pattern+'''";'''
    mycursor.execute(query)
    t = from_db_cursor(mycursor)
    print(t)

##### SIZE 2 QUERIES #####
#generates size 2 queries using ST_DWithin
def generate_size_2_queries(comb, mycursor, conn, threshold, h, X=0, Y=1):
    list_comb = []
    create_table(comb, mycursor, conn) #create table with name (e_type_name[X] + e_type_name[Y])
    table_name_x = '"large_' + comb[X] + '"'
    table_name_y = '"large_' + comb[Y] + '"'
    query = ''' INSERT INTO "TiAI_Assignment1_InputData_Large"."'''+(comb)+'''" ('''+comb[X]+'''_id, '''+comb[Y]+'''_id)
                SELECT
                '''+comb[X]+'''.id AS '''+comb[X]+'''_id,
                '''+comb[Y]+'''.id AS '''+comb[Y]+'''_id
                FROM "TiAI_Assignment1_InputData_Large".''' + table_name_x+ ''' AS '''+comb[X]+'''
                JOIN "TiAI_Assignment1_InputData_Large".''' + table_name_y + ''' AS '''+comb[Y]+'''
                ON ST_DWithin('''+comb[X]+'''.lat_long, '''+comb[Y]+'''.lat_long, '''+ str(h) +''', true);'''
    mycursor.execute(query)
    add_query(comb, '''"TiAI_Assignment1_InputData_Large"."'''+(comb)+'''"''')
    conn.commit()
    print_table(mycursor, conn, comb)
    all_table_dict[comb] = '''"TiAI_Assignment1_InputData_Large"."'''+(comb)+'''"'''
    pi_val = participation_index(mycursor, comb)
    if(pi_val<threshold):
        truncate_table(mycursor, conn, comb)
        return 0 #means this pattern has failed
    
    table_dict[comb] = '''"TiAI_Assignment1_InputData_Large"."'''+(comb)+'''"'''
    return 1

##### SIZE 3+ QUERIES #####
#creates and executes queries for patterns of size larger than 2
def generate_size_k_queries(pattern, mycursor, conn, threshold=0.5):
    all_subs = k_minus_one_finder(pattern)
    queries = []
    query_names=[]
    count = 1
    if(len(pattern)<3):
        return
    for i in all_subs:
        if(query_dict.get(i)==None):
            generate_size_k_queries(i, mycursor, conn, threshold)
            queries.append(query_dict[i]) #actual query referred
            query_names.append("Q"+str(count)) #stores the names = [Q1, Q2, Q3...]
            count=count+1
        else:
            queries.append(query_dict[i]) #actual query referred
            query_names.append("Q"+str(count)) #stores the names = [Q1, Q2, Q3...]
            count=count+1

    create_table(pattern, mycursor, conn) #create table with name pattern
    ########## INSERT clause ##########
    query = ''' INSERT INTO "TiAI_Assignment1_InputData_Large"."''' + pattern +'''" ('''
    for i in range(len(pattern)):
        j=(i+1)%(len(pattern))
        query = query +pattern[j]+"_id" #Ex: Q1.a_id as a_id
        if(i<len(pattern)-1):
            query = query + ", " #Adds a comma if more columns remaining, else ignores comma
        else:
            query = query + ") "
    ########### SELECT clause ##########
    query = query +"SELECT "
    for i in range(len(pattern)):
        j=(i+1)%(len(pattern))
        query = query + query_names[i] + "." +pattern[j]+"_id AS "+pattern[j]+"_id" #Ex: Q1.a_id as a_id
        if(i<len(pattern)-1):
            query = query + ", " #Adds a comma if more columns remaining, else ignores comma
    ########### FROM clause ##########
    query = query + "\nFROM ("
    for i in range(len(queries)):
        query = query + queries[i][0:len(queries[i])] + ") AS "+query_names[i]
        if(i<len(queries)-1):
            query = query + " NATURAL JOIN\n(" #Adds a comma if more queries remaining, else ignores comma
    ########### WHERE clause ##########
    query = query + "\nWHERE "
    for i in range(len(query_names)):
        j=(i+1)%(len(pattern))
        k=(i+2)%(len(pattern))
        query = query + query_names[i] + "." + pattern[j] + "_id = " + query_names[k] + "." + pattern[j] + "_id "
        if(i<len(queries)-1):
            query = query + "AND " #Adds a comma if more conditions remaining
        elif(i==len(queries)-1):
            query = query + ";" #End of query
    mycursor.execute(query)
    add_query(pattern, '''"TiAI_Assignment1_InputData_Large"."'''+pattern+'''"''')
    conn.commit()
    print_table(mycursor, conn, pattern)
    all_table_dict[pattern] = '''"TiAI_Assignment1_InputData_Large"."'''+(pattern)+'''"'''
    pi_val = participation_index(mycursor, pattern)
    if(pi_val<threshold):
        truncate_table(mycursor, conn, pattern)
        return 0 #means this pattern has failed
    table_dict[pattern] = '''"TiAI_Assignment1_InputData_Large"."'''+pattern+'''"'''
    return 1 #means this pattern has passed

##### ACTUAL ALGORITHM #####
def k_patterns(master_pattern, mycursor, conn, h, threshold=0.5):
    all_subs = sublist_finder(master_pattern)
    length = len(master_pattern)
    final_pattern = all_subs[0]
    btp = []
    for i in range(1, length):
        pattern_category = all_subs[i]
        below_threshold_patterns=[]
        for pattern in pattern_category:
            if(i==1):
                passed = generate_size_2_queries(pattern, mycursor, conn, threshold, h)
                if(passed==0):
                    below_threshold_patterns.append(pattern)
            else:
                passed = generate_size_k_queries(pattern, mycursor, conn, threshold)
                if(passed==0):
                    below_threshold_patterns.append(pattern)
        #check if all patterns in that size are empty i.e none of the patterns cross the threshold
        if(below_threshold_patterns!=pattern_category):
            btp = below_threshold_patterns
            final_pattern = list(set(pattern_category).difference(set(below_threshold_patterns)))
            
    return final_pattern, btp

################## PARAMETER CALCULATOR FUNCTIONS ##################
#find participation ratio of X in pattern
def participation_ratio(mycursor, X, pattern):
    if(len(pattern)==1):
        table_name_x = '"large_' + X + '"'
        table_name_y = '"large_' + X + '"'
    else:
        table_name_x = '"large_' + X + '"'
        table_name_y = '"' + pattern + '"'
    query = 'SELECT COUNT(*) FROM "TiAI_Assignment1_InputData_Large".' + table_name_x + ';'
    mycursor.execute(query)
    instances_tot_X = mycursor.fetchone()[0] # value of all instances of X
    query = ''' SELECT
                COUNT(DISTINCT '''+X+'''_id)
                FROM "TiAI_Assignment1_InputData_Large".''' + table_name_y+ ''';'''
    mycursor.execute(query)
    instances_neighbour_Y = mycursor.fetchone()[0] # value of all instances of X neighbouring Y
    return float(instances_neighbour_Y/instances_tot_X)

#find participation index of pattern
def participation_index(mycursor, pattern):
    val=[]
    for i in range(len(pattern)):
        val.append(participation_ratio(mycursor, pattern[i], pattern))
    return min(val)





################## MAIN FUNCTION ##################
#runs the whole game
def master_func(master_pattern, threshold, h):
    #connect to database
    mycursor, conn = connect()
    #clear tables and indices from previous query runs
    drop_index_all(master_pattern, mycursor, conn)
    delete_init(master_pattern, mycursor, conn)
    #create R-tree indexes on the base tables
    create_index_all(master_pattern, mycursor, conn)
    #output print
    print("\n****************************************RESULTS****************************************")
    print("Chosen parameters:")
    print("------------------")
    print("Parameters: ", end="")
    for i in [*master_pattern]:
        print(i, end=" ")
    print("")
    print("Threshold: " + str(threshold))
    if(h%1000==0):
        print("Distance Threshold: " + str(int(h/1000)) + " kilometres")
    else:
        print("Distance Threshold: " + str(round(float(h/1000),3)) + " kilometres")
    #final pattern that remains
    final_pattern, btp = k_patterns(master_pattern, mycursor, conn, h,threshold)
    print("\nEligible colocation patterns: ", final_pattern)
    print("\n\n****************************************END OF RESULTS****************************************\n")
    #delete all temporary tables created
    delete_fin(mycursor, conn)
    #disconnect from database
    disconnect(mycursor, conn)


master_pattern = "ABCDE"
threshold = 0.3
h = 120000
master_func(master_pattern, threshold, h)