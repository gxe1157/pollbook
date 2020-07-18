import sqlite3, csv, time, sys
#select municipality, ward, district, count(district) as ctn from test group by municipality, ward, district order by municipality, ward, district

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

    def check_table_exists(self, table_name):
        #get the count of tables with the name
        query = "SELECT count(name) FROM sqlite_master WHERE type='table' AND name='" + table_name +"'"
        self.cur.execute(query)
        table_exists = self.cur.fetchone()[0]
        return table_exists    


    def __del__(self):
        self.conn.close()
        

    def insert_user(self, username, password):
        self.cur.execute("INSERT INTO users VALUES (NULL, ?, ?)",
                         (username, password))
        self.conn.commit()

    def insert_customer(self, customer, contact):
        self.cur.execute("INSERT INTO customers VALUES (NULL, ?, ?)",
                         (customer, contact))
        self.conn.commit()

    def fetch_by_id(self, id, table_name):
        query = "SELECT * FROM "+table_name+"WHERE id='"+id+"'"
        self.cur.execute(query)
        rows = self.cur.fetchone()
        print(rows)
        return rows

    def fetch_all(self, table_name):
        self.cur.execute("SELECT * FROM "+table_name)
        rows = self.cur.fetchall()
        return rows

    def fetch_voters(self, table_name):
        query = "SELECT municipality, ward, district FROM "+table_name+" ORDER BY municipality, ward, district"        
        self.cur.execute(query)
        rows = self.cur.fetchall()
        return rows

    def confirm_login(self, username, password):
        print('fetch_customers..............')
        self.cur.execute("SELECT * FROM users where username='"+username+"' and password='"+password+"'")
        rows = self.cur.fetchone()
        print(rows)
        return rows


    def csv_to_sqlite(self, csv_file_name, progress_bar, percent, messagebox, table_name):
        number_columns = 0
        last_line = False
        table_name = table_name.replace(' ', '_')
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
                            success_mess = f"Total Numbr of Records : {record_number}."
                            messagebox.showinfo("Import File Successful", success_mess)
                            return True

                    record_number +=1

                percent['text'] = "{}%".format(int(100))
    

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

        print( f"This is the number of lines in the file: {lines}") 
        # sys.exit(f"Last record: Done..............")
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
