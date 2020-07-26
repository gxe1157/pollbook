import sqlite3, csv, time, sys
#select municipality, ward, district, count(district) as ctn from test group by municipality, ward, district order by municipality, ward, district

class Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()

        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS customers (id INTEGER PRIMARY KEY, abbr_name text, county text, contact text)")

        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS election_events (id INTEGER PRIMARY KEY, event text)")

        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)")

        self.conn.commit()

        # db -> pollbook.db
        # self.insert_customer("Bergen", "Bergen County", "Supervisor")
        # self.insert_customer("Hudson", "Hudson County", "Supervisor")
        # self.insert_customer("Mercer", "Mercer County", "Supervisor")
        # self.insert_customer("Union", "Union County", "Supervisor")

        # self.insert_events("Primary")
        # self.insert_events("General")
        # self.insert_events("Board of Education")        
        # self.insert_events("Municipal")
        # self.insert_events("Municipal Run Off")

        # self.insert_user("admin", "admin123")

    #==========  Metadata Queries ======================================    
    def check_table_exists(self, table_name):
        #get the count of tables with the name
        query = "SELECT count(name) FROM sqlite_master WHERE type='table' AND name='" + table_name +"'"
        self.cur.execute(query)
        table_exists = self.cur.fetchone()[0]
        return table_exists    

    def fetch_tables_list(self):
        self.cur.execute('SELECT name from sqlite_master where type= "table"')
        rows = self.cur.fetchall()
        return rows

    def __del__(self):
        self.conn.close()
        
    #==========  Applications Queries ======================================    

    def insert_user(self, username, password):
        self.cur.execute("INSERT INTO users VALUES (NULL, ?, ?)",
                         (username, password))
        self.conn.commit()

    def insert_customer(self, abbr_name, county, contact):
        self.cur.execute("INSERT INTO customers VALUES (NULL, ?, ?, ?)",
                         (abbr_name, county, contact))
        self.conn.commit()

    def insert_events(self, events):
        self.cur.execute("INSERT INTO election_events VALUES (NULL, ?)", (events,))
        self.conn.commit()

    def fetch_by_id(self, id, table_name):
        query = f"SELECT * FROM {table_name} WHERE id='{id}'"
        self.cur.execute(query)
        rows = self.cur.fetchone()
        return rows

    def fetch_all(self, table_name):
        query = f"SELECT * FROM {table_name}"
        self.cur.execute(query)
        rows = self.cur.fetchall()
        return rows

    # def fetch_voters(self, table_name):
    #     query = "SELECT municipality, ward, district FROM "+table_name+" ORDER BY municipality, ward, district"        
    #     self.cur.execute(query)
    #     rows = self.cur.fetchall()
    #     return rows

    def confirm_login(self, username, password):
        self.cur.execute("SELECT * FROM users where username='"+username+"' and password='"+password+"'")
        rows = self.cur.fetchone()
        return rows

    def csv_to_sqlite(self, csv_file_name, progress_bar, percent, messagebox, table_name):
        number_columns = 0
        last_line = False

        table_exists = self.check_table_exists(table_name)
        if table_exists == 1:
            error_mess = f"Alert: Table Aready Exist."
            messagebox.showerror("Fatal Error", error_mess)
            sys.exit(error_mess)           
        else:
            build_placeHolder = ''
            x = 0
            tic = time.perf_counter()

            total_rows = self._count_csv_lines(csv_file_name)
            with open(csv_file_name, 'r') as file:
                record_number = 0
                for row in file:
                    # remove carraige return '\n'
                    row = row.strip('\n')
                    # create list - array
                    csv_row = row.split("|")
                    # remove last empty element which has no corresponding fieldname
                    if len(csv_row)==20:
                        csv_row.pop()

                    if record_number == 0:    
                        build_placeHolder = self._create_table(csv_row, table_name)
                        number_columns = len( build_placeHolder.split(",") )
                        record_number +=1 # This is an adjustment so to counts matched record id                       
                    else:
                        # print(f"CSV Imported rows {record_number} = {total_rows} -> {csv_row[0]}")                        
                        if number_columns == len(csv_row):
                            self._insert_record(build_placeHolder, csv_row, table_name)
                        else:
                            if record_number == total_rows:
                                last_line = True
                                self.conn.commit()
                            else:
                                error_mess = f"Error: There seems to be a problem with record {record_number}.\nAbort Data Import...."
                                messagebox.showerror("Fatal Error", error_mess)
                                # Execute the DROP Table SQL statement
                                dropTableStatement = "DROP TABLE "+table_name
                                self.cur.execute(dropTableStatement)                                
                                self.conn.commit()                                
                                #Close App
                                sys.exit(error_mess)                                    

                    if record_number > x or last_line == True:
                        self._update_frame(progress_bar, percent, total_rows, record_number)
                        toc = time.perf_counter()
                        print(f"CSV Imported rows {str(record_number)} in {toc - tic:0.4f} seconds")
                        x +=2000
                        if last_line == True:  
                            # Create lookup table by municipality, ward, district with counts by districts
                            self.check_table_form_master(table_name)        

                            success_mess = f"Total Numbr of Records : {record_number}."
                            messagebox.showinfo("Import File Successful", success_mess)
                            return True

                    record_number +=1

                percent['text'] = "{}%".format(int(100))
    
    #=============================================#
    #  
    #=============================================#
    def check_table_form_master(self, table_name):
        ''' Create lookup table by municipality, ward, district with counts by districts '''
        form_table_name = table_name+'_fm'        
        table_exists=self.check_table_exists(form_table_name)        

        if table_exists == False:
            self.cur.execute("CREATE TABLE IF NOT EXISTS "+form_table_name+" (id INTEGER PRIMARY KEY, form_no integer, municipality text, ward text, district integer, dcount interger)")
            self.conn.commit()

            query = f"SELECT municipality, ward, district, count(district) as dcount FROM {table_name} GROUP BY municipality, ward, district ORDER BY municipality, ward, district"
            self.cur.execute(query)
            rows = self.cur.fetchall()
            for row in rows:
                municipality = row[0]
                ward = row[1]
                district = row[2]
                dcount = row[3]
                self.cur.execute("INSERT INTO "+form_table_name+" VALUES (?, ?, ?, ?, ?, ?)", (None, None, municipality, ward, district, dcount))
            self.conn.commit()
        return form_table_name    

    def fetch_clients(self, table_name):
        form_table_name = self.check_table_form_master(table_name)        
        query = f"SELECT id, municipality FROM {form_table_name} GROUP BY municipality ORDER BY municipality"
        rows = self.cur.execute(query)
        return rows

    def fetch_mwd(self, table_name, muni=None ):
        form_table_name = table_name+'_fm'
        muni = f"municipality != ''" if muni == None else f"municipality = '{muni}'"
        query = f"SELECT id, form_no, municipality, ward, district, dcount FROM \
                    {form_table_name} WHERE "+muni+" ORDER BY municipality, ward, district, dcount"

        rows = self.cur.execute(query)
        return rows

    def update_mwd(self, data, table_name ):
        print(data);
        set_flds = ' SET '
        for key, value in data.items():
            set_flds += f"{key} = {value},  "

        print(set_flds)        

        sys.exit('quit...................')
        # query = UPDATE products SET Qty=100,product_name='CAD' WHERE product_id = 102

    def run_query(self, query):
        # print(query)
        self.cur.execute(query)
        self.conn.commit()        


    #=============================================#
    # Private class methods used only by db.py
    #=============================================#    
    def _update_frame(self, progress_bar, percent, total_rows, record_number):
        self.conn.commit()
        unit = record_number/total_rows*100
        progress_bar['value'] = unit
        progress_bar.update_idletasks()  
        percent['text'] = "{}%".format(int(unit))


    def _count_csv_lines(self, csv_file_name):
        file = open(csv_file_name)
        reader = csv.reader(file)
        lines= len(list(reader))
        return lines                

    def _create_table(self, headers, table_name):
        build_tableSchema = ''      
        build_placeHolder = ''

        for fld_name in headers:
            fieldType = 'TEXT'
            build_tableSchema +=  fld_name+' '+fieldType+','
            build_placeHolder += '?,'            

        build_tableSchema = build_tableSchema[:-1]
        query = "CREATE TABLE IF NOT EXISTS "+table_name+" ( "+build_tableSchema+")"     
        # print(query)
        self.cur.execute(query)
        self.conn.commit()

        return build_placeHolder[:-1] 

    def _insert_record(self, build_placeHolder, csv_row, table_name):
        query = "INSERT INTO "+table_name+" values ("+build_placeHolder+")"     
        self.cur.execute(query, csv_row)
