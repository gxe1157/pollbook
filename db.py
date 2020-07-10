import sqlite3, csv

class Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()

        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS parts (id INTEGER PRIMARY KEY, part text, customer text, retailer text, price text)")

        self.conn.commit()

    def fetch(self):
        self.cur.execute("SELECT * FROM parts")
        rows = self.cur.fetchall()
        return rows

    def __del__(self):
        self.conn.close()

    def check_table_exists(self, table_name):
        #get the count of tables with the name
        query = "SELECT count(name) FROM sqlite_master WHERE type='table' AND name='" + table_name +"'"
        self.cur.execute(query)
        table_exists = self.cur.fetchone()[0]
        return table_exists    

    def insert_record(self, table_name, build_placeHolder, csv_row, complete=False):
        query = "INSERT INTO "+table_name+" values ("+build_placeHolder+")"     
        self.cur.execute(query, csv_row)

        if complete==True:
            self.conn.commit()

    def create_pollbook_table(self, headers, table_name):
        build_tableSchema = ''      
        build_placeHolder = ''

        for fld_name in headers:
            fieldType = 'TEXT'
            build_tableSchema +=  fld_name+' '+fieldType+','
            build_placeHolder += '?,'            

        build_tableSchema = build_tableSchema[:-1]
        query = "CREATE TABLE IF NOT EXISTS "+table_name+" ( "+build_tableSchema+")"     
        print(query)
        self.cur.execute(query)
        self.conn.commit()

        return build_placeHolder[:-1] 


'''
    def csv_to_array(self, file_name, table_name):
        # print('file: '+file_name)
        results = []
        with open(file_name) as csv_file:
            reader = csv.reader(csv_file, delimiter='|')
            for i, row in enumerate(reader): # each row is a record

                if i == 0:
                    header = row
                else:
                    # row.insert(0, None) # to add the word 'null' as a string                    
                    results.append(row)                        
                    if i >10:
                        break

        tableSchema, placeHolder = self.create_pollbook_table(header)
        tableSchema = tableSchema.replace(" TEXT", "||TEXT")                 
        tableSchema = tableSchema.replace(" ", "_")                         
        tableSchema = tableSchema.replace("-", "_")
        tableSchema = tableSchema.replace("||TEXT", " TEXT")                 
        fld_names = tableSchema.replace(" TEXT", "")

        query = f"CREATE TABLE IF NOT EXISTS {table_name}({tableSchema})"

        # print(query)
        self.cur.execute(query)
        # self.insert_many(fld_names, placeHolder, table_name, results)

    def insert_many(self, fld_names, placeHolder, table_name, results):
        print("\n ----------------------- \n")
        print(results[0]);
        print("\n ----------------------- \n")
        results =('152784825', 'AAMER', 'RAFI', 'D', '', '428', '', '', 'KELLINGTON DR', '', 'EAST WINDSOR', 'EAST WINDSOR', '08520', '', 'DEM', '', '11', 'A', '', '')

        query = """insert into test (ID,VOTER_ID,LAST_NAME,FIRST_NAME,MIDDLE_NAME,SUFFIX,STREET_NUMBER,SUF_A,SUF_B,STREET_NAME,UNIT,POSTAL_CITY,MUNICIPALITY,ZIP_CODE,DATE_OF_BIRTH,PARTY,WARD,DISTRICT,VOTER_STATUS,REGISTRATION_PROVISIONAL_BALLOT) values(NULL,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,? )"""
        print(query)

        # Fill the table
        self.cur.executemany(query, results)
        self.conn.commit()

'''