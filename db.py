import sqlite3, csv, time, sys

class Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()

        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS customers (id INTEGER PRIMARY KEY, customer text, contact text)")

        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)")

        self.conn.commit()

        # db = Database('pollbook.db')
        # self.insert_customer("Bergen County", "John Doe")
        # self.insert_customer("Hudson County", "Mike Henry")
        # self.insert_customer("Mercer County", "Karen Johnson")
        # self.insert_customer("Union County", "Karen Johnson")

        # self.insert_user("admin", "admin123")

    def insert_user(self, username, password):
        self.cur.execute("INSERT INTO users VALUES (NULL, ?, ?)",
                         (username, password))
        self.conn.commit()

    def insert_customer(self, customer, contact):
        self.cur.execute("INSERT INTO customers VALUES (NULL, ?, ?)",
                         (customer, contact))
        self.conn.commit()

    def fetch_by_id(self, id):
        query = "SELECT * FROM customers WHERE id='"+id+"'"
        self.cur.execute(query)
        rows = self.cur.fetchone()
        print(rows)
        return rows

    def fetch_customers(self):
        print('fetch_customers..............')
        self.cur.execute("SELECT * FROM customers")
        rows = self.cur.fetchall()

        return rows

    def confirm_login(self, username, password):
        print('fetch_customers..............')
        self.cur.execute("SELECT * FROM users where username='"+username+"' and password='"+password+"'")
        rows = self.cur.fetchone()
        print(rows)

        return rows

    def __del__(self):
        self.conn.close()

    def check_table_exists(self, table_name):
        #get the count of tables with the name
        query = "SELECT count(name) FROM sqlite_master WHERE type='table' AND name='" + table_name +"'"
        self.cur.execute(query)
        table_exists = self.cur.fetchone()[0]
        return table_exists    

    def insert_record(self, table_name, build_placeHolder, csv_row):
        query = "INSERT INTO "+table_name+" values ("+build_placeHolder+")"     
        self.cur.execute(query, csv_row)

    def create_pollbook_table(self, headers, table_name):
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

    def csv_to_sqlite(self, file_name, f, my_progress, percent, messagebox):

        # check id table is empty
        # SQLite> DELETE FROM COMPANY;
        # SQLite> VACUUM;        

        number_columns = 0
        last_line = False
        table_exists = self.check_table_exists('pollbook_june2020')
        if table_exists == 1:
            error_mess = f"Alert: Table Aready Exist."
            messagebox.showerror("Fatal Error", error_mess)
            sys.exit(error_mess)           
        else:
            do_commit = False
            table_name="test"
            build_placeHolder = ''
            x = 0
            tic = time.perf_counter()

            total_rows = self.count_csv_lines(file_name)
            with open(file_name, 'r') as file:
                no_records = 0
                for row in file:
                    # remove carraige return '\n'
                    row = row.strip('\n')
                    # create list - array
                    csv_row = row.split("|")
                    # remove last empty element which has no corresponding fieldname
                    if len(csv_row)==20:
                        csv_row.pop()

                    if no_records == 0:    
                        build_placeHolder = self.create_pollbook_table(csv_row, table_name)
                        number_columns = len( build_placeHolder.split(",") )
                        no_records +=1 # This is an adjustment so to counts matched record id                       
                    else:
                        # print(f"CSV Imported rows {no_records} = {total_rows} -> {csv_row[0]}")                        
                        if number_columns == len(csv_row):
                            self.insert_record(table_name, build_placeHolder, csv_row)
                        else:
                            if no_records == total_rows:
                                last_line = True
                            else:
                                error_mess = f"Error: There seems to be a problem with record {no_records}.\nAbort Data Import...."
                                messagebox.showerror("Fatal Error", error_mess)
                                # Execute the DROP Table SQL statement
                                dropTableStatement = "DROP TABLE "+table_name
                                self.cur.execute(dropTableStatement)                                
                                self.conn.commit()                                
                                #Close App
                                sys.exit(error_mess)                                    

                    if no_records > x or last_line == True:
                        self.update_frame(my_progress, percent, total_rows, no_records)
                        toc = time.perf_counter()
                        print(f"CSV Imported rows {str(no_records)} in {toc - tic:0.4f} seconds")
                        x +=2000
                        if last_line == True:    
                            success_mess = f"Total Numbr of Records : {no_records}."
                            messagebox.showinfo("Import File Successful", success_mess)
                            return True

                    no_records +=1

                percent['text'] = "{}%".format(int(100))
    
    def update_frame(self, my_progress, percent, total_rows, no_records):
        self.conn.commit()
        unit = no_records/total_rows*100
        my_progress['value'] = unit
        my_progress.update_idletasks()  
        percent['text'] = "{}%".format(int(unit))


    def count_csv_lines(self, file_name):
        file = open(file_name)
        reader = csv.reader(file)
        lines= len(list(reader))

        print( f"This is the number of lines in the file: {lines}") 
        # sys.exit(f"Last record: Done..............")
        return lines                


