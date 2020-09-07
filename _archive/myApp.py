from tkinter import  *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox



# Move this to database class
sqlite = True  # choose mysql or sqlite
if sqlite == True:
	# sqlite3
	import sqlite3	
	from db import Database
	db = 'pollbook.db'
	conn = sqlite3.connect(db)
	cursor = conn.cursor()
else:
	# mysql
	import mysql.connector
	db = mysql.connector.connect(host="localhost", user="root", password="", database="njpob", auth_plugin="")
	cursor = db.cursor()

# functions
def check_table_form_master(table_name):
	#get the count of tables with the name
	query = "SELECT count(name) FROM sqlite_master WHERE type='table' AND name='" + table_name +"'"
	cursor.execute(query)
	table_exists = cursor.fetchone()[0]

	if table_exists == False:
		cursor.execute("CREATE TABLE IF NOT EXISTS "+table_name+" (id INTEGER PRIMARY KEY, form_no integer, municipality text, ward text, district integer, dcount interger)")
		conn.commit()

		query = "SELECT municipality, ward, district, count(district) as dcount FROM test GROUP BY municipality, ward, district ORDER BY municipality, ward, district"
		cursor.execute(query)
		rows = cursor.fetchall()
		# print(rows)
		# sys.exit('quit.................')

		for row in rows:
			municipality = row[0]
			ward = row[1]
			district = row[2]
			dcount = row[3]
			cursor.execute("INSERT INTO "+table_name+" VALUES (?, ?, ?, ?, ?, ?)", (None, None, municipality, ward, district, dcount))

		conn.commit()

def update(rows):
	trv.delete(*trv.get_children())
	for i in rows:
		trv.insert('', 'end', values=i)

def search(muni=None):
	if muni == None or muni =='All...':
		clear()
		# q2 = q.get().upper()
	else:
		q2 = muni.upper()
		query = "SELECT ID, form_no, municipality, ward, district, dcount FROM form_master WHERE municipality ='"+q2+"' ORDER BY municipality, ward, district, dcount"
		cursor.execute(query)
		rows = cursor.fetchall()
		update(rows)

def clear():
	clear_inputs()	
	query = "SELECT ID, form_no, municipality, ward, district, dcount FROM form_master ORDER BY municipality, ward, district, dcount"
	cursor.execute(query)
	rows = cursor.fetchall()
	# print(rows[0])
	update(rows)


def clear_inputs():
	t1.set(' ')
	t2.set(' ')
	t3.set(' ')		
	t4.set(' ')		
	t5.set(' ')		

def getrow(event):
	rowid = trv.identify_row(event.y)
	item = trv.item(trv.focus())
	t1.set(item['values'][0])
	t2.set(item['values'][1])
	t3.set(item['values'][2])		
	t4.set(item['values'][3])		
	t5.set(item['values'][4])		

def update_data():
	rec_id = t1.get()
	form_no = t2.get()
	muni = t3.get()

	query = f"UPDATE form_master SET form_no = {form_no} WHERE id = {rec_id}"
	print(query)
	cursor.execute(query)
	conn.commit()
	search(muni)

def add_new():
	fname = t2.get()
	lname = t3.get()

	query = "INSERT INTO users(id, first_name, last_name) VALUES(NULL, %s, %s)"
	cursor.execute(query, (fname, lname))
	db.commit()	
	clear()

def delete_row():
	rec_id = t1.get()	
	if messagebox.askyesno("Confirm Delete","Are You sure you want to delete this record?"):
		query = "DELETE FROM test WHERE id="+rec_id
		cursor.execute(query)
		db.commit()
		clear()
	else:
		return True

## Combobox - Select Dropdown
def fetch_municipalies():
	''' Create lookup table by municipalities with counts by districts '''
	check_table_form_master('form_master')
	query = "SELECT id, municipality FROM form_master GROUP BY municipality ORDER BY municipality"
	cursor.execute(query)
	rows = cursor.fetchall()

	options = ['All...']
	for row in rows:
		options.append(f"{row[1]}")

	return options

def get_municipality(event):
	muni = mycombo.get()
	search(muni)


## List box functions
def delete_one():
	my_listbox.delete(ANCHOR)

def delete_all():
	my_listbox.delete(0, END)  # "end"

def select_show():
	my_label.config(text=my_listbox.get(ANCHOR))		

def select_all():
	result = ''
	for item in my_listbox.curselection():
		result = result + mylistbox(item) +'\n'

	print(result)		

def delete_multiple():
	for item in reverse(my_listbox.curselection()):
		my_listbox.delete(item)

root = Tk()
root.title("My Application")
root.geometry("800x700")
root.resizable(False, False)

# Init varaibles
q = StringVar()
t1 = StringVar()
t1a = StringVar()
t1b = StringVar()
t1c = StringVar()

t2 = StringVar()
t3 = StringVar()
t4 = StringVar()
t5 = StringVar()

opts = StringVar()
options = []

# Create Section Frames
wrapper1 = LabelFrame(root, text="Dispaly List")
wrapper2 = LabelFrame(root, text="Customer Data")
wrapper3 = LabelFrame(root, text="Select Items for Update")

wrapper1.pack(fill="both", expand="yes", padx="20", pady="10")
wrapper2.pack(fill="both", expand="yes", padx="20", pady="10")
wrapper3.pack(fill="both", expand="yes", padx="20", pady="10")

# Combobox for select municipality
options = fetch_municipalies();

# global mycombo
mycombo = ttk.Combobox(wrapper1, textvariable=opts, width=30, font=("helvetica", 12))	
mycombo['values'] = options
mycombo.pack(padx=5, pady=10)
mycombo.current(0)
mycombo.bind("<<ComboboxSelected>>", get_municipality )    

# Display List Frame (Treeview)
trv = ttk.Treeview(wrapper1, column=(1,2,3,4,5,6), show="headings", height="12", selectmode='browse')
# trv.place(x=30, y=45)

vsb = ttk.Scrollbar(wrapper1, orient="vertical", command=trv.yview)
vsb.place(x=730, y=45, height=265)
trv.configure(yscrollcommand=vsb.set)
trv.pack()

trv.heading(1, text="Record No")
trv.column(1, minwidth=0, width=100, anchor=E, stretch=YES)
trv.heading(2, text="Form No.")
trv.column(2, minwidth=0, anchor=CENTER, width=100, stretch=NO)
trv.heading(3, text="Municipality")
trv.column(4, minwidth=0, width=170, stretch=YES)
trv.heading(4, text="Ward")
trv.column(4, minwidth=0, anchor=E, width=100, stretch=NO)
trv.heading(5, text="District")
trv.column(5, minwidth=0, anchor=E, width=100, stretch=NO)
trv.heading(6, text="Totals")
trv.column(6, minwidth=0, anchor=E, width=90, stretch=NO)

# Get row data
trv.bind('<Double 1>', getrow )

#Scrollbar wrapper3
my_scrollbar = Scrollbar(wrapper3, orient=VERTICAL)
#list Box
# SINGLE, BROWSE, MULTIPLE, EXTENED
my_listbox = Listbox(wrapper3, width=100, yscrollcommand=my_scrollbar.set)
#scrollbar configure
my_scrollbar.config(command=my_listbox.yview)
my_scrollbar.pack(side=RIGHT, fill=Y)
wrapper3.pack()

my_listbox.pack(pady=5)

my_listbox.insert(END, "This is an item1")
my_listbox.insert(END, "This is an item2")
my_listbox.insert(END, "This is an item3")
my_listbox.insert(END, "This is an item4")
my_listbox.insert(END, "This is an item5")
my_listbox.insert(END, "This is an item6")
my_listbox.insert(END, "This is an item7")
my_listbox.insert(END, "This is an item8")
my_listbox.insert(END, "This is an item9")
my_listbox.insert(END, "This is an item10")

# Clear and display default records
clear()

# Data User Frame
# Input Fields
lbl1 = Label(wrapper2, text="Record No")
lbl1.grid(row=0, column=0, padx=5, pady=3)
ent1 = Entry(wrapper2, textvariable=t1, state="disabled")
ent1.grid(row=0, column=1, padx=5, pady=3)

lbl1a = Label(wrapper2, text="Poll Name")
lbl1a.grid(row=1, column=3, padx=5, pady=3)
ent1a = Entry(wrapper2, textvariable=t1a,  width=60)
ent1a.grid(row=1, column=4, padx=5, pady=3)

lbl1b = Label(wrapper2, text="Poll Location")
lbl1b.grid(row=2, column=3, padx=5, pady=3)
ent1b = Entry(wrapper2, textvariable=t1b,  width=60)
ent1b.grid(row=2, column=4, padx=5, pady=3)

lbl2 = Label(wrapper2, text="Form No")
lbl2.grid(row=1, column=0, padx=5, pady=3)
ent2 = Entry(wrapper2, textvariable=t2)
ent2.grid(row=1, column=1, padx=5, pady=3)

lbl3 = Label(wrapper2, text="Municipality")
lbl3.grid(row=2, column=0, padx=5, pady=3)
ent3 = Entry(wrapper2, textvariable=t3, state="disabled")
ent3.grid(row=2, column=1, padx=5, pady=3)
# ent2.place(x=78, y=30, width=200) #width in pixels

lbl4 = Label(wrapper2, text="Ward")
lbl4.grid(row=3, column=0, padx=5, pady=3)
ent4 = Entry(wrapper2, textvariable=t4, state="disabled")
ent4.grid(row=3, column=1, padx=5, pady=3)

lbl5 = Label(wrapper2, text="District")
lbl5.grid(row=4, column=0, padx=5, pady=3)
ent5 = Entry(wrapper2, textvariable=t5, state="disabled")
ent5.grid(row=4, column=1, padx=5, pady=3)


# Buttons
add_btn = Button(wrapper2, text="Add New", command=add_new)
up_btn = Button(wrapper2, text="Update", command=update_data)
delete_btn = Button(wrapper2, text="Delete", command=delete_row)

add_btn.grid(row=7, column=0, padx=2, pady=1)
up_btn.grid(row=7, column=1, padx=2, pady=1)
delete_btn.grid(row=7, column=2, padx=2, pady=1)


root.mainloop()
