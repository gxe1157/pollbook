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
def update(rows):
	trv.delete(*trv.get_children())
	for i in rows:
		trv.insert('', 'end', values=i)

def search():
	q2 = q.get()
	query = "SELECT voter_id,first_name, last_name FROM test WHERE first_name LIKE '%"+q2+"%' OR last_name LIKE '%"+q2+"%'"
	cursor.execute(query)
	rows = cursor.fetchall()
	update(rows)

def clear():
	clear_inputs()	
	query = "SELECT voter_id,first_name, last_name FROM test"
	cursor.execute(query)
	rows = cursor.fetchall()
	update(rows)

def clear_inputs():
	t1.set(' ')
	t2.set(' ')
	t3.set(' ')		

def getrow(event):
	rowid = trv.identify_row(event.y)
	item = trv.item(trv.focus())
	t1.set(item['values'][0])
	t2.set(item['values'][1])
	t3.set(item['values'][2])		


def update_data():
	rec_id = t1.get()
	fname  = t2.get()
	lname  = t3.get()

	if messagebox.askyesno("Confirm Please","Are You sure you want to update this record?"):
		query = "UPDATE users SET first_name = %s, last_name = %s WHERE id = %s"
		cursor.execute(query, (fname, lname, rec_id) )
		db.commit()
		clear()
	else:
		return True

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

root = Tk()
root.title("My Application")
root.geometry("800x700")
root.resizable(False, False)

# Init varaibles
q = StringVar()
t1 = StringVar()
t2 = StringVar()
t3 = StringVar()

# Create Section Frames
wrapper1 = LabelFrame(root, text="Dispaly List")
wrapper2 = LabelFrame(root, text="Search")
wrapper3 = LabelFrame(root, text="Customer Data")

wrapper1.pack(fill="both", expand="yes", padx="20", pady="10")
wrapper2.pack(fill="both", expand="yes", padx="20", pady="10")
wrapper3.pack(fill="both", expand="yes", padx="20", pady="10")


# Display List Frame (Treeview)
trv = ttk.Treeview(wrapper1, column=(1,2,3), show="headings", height="6")
trv.pack()

trv.heading(1, text="ID")
trv.heading(2, text="First Name")
trv.heading(3, text="Last Name")
# trv.heading(4, text="Age")

# Get row data
trv.bind('<Double 1>', getrow )

# Clear and display default records
clear()


# Search Frame
lbl = Label(wrapper2, text="Search")
lbl.pack(side=tk.LEFT, padx=10)
ent = Entry(wrapper2, textvariable=q)
ent.pack(side=tk.LEFT, padx=6)
btn = Button(wrapper2, text="Search", command=search)
btn.pack(side=tk.LEFT, padx=6)
cbtn = Button(wrapper2, text="Clear", command=clear)
cbtn.pack(side=tk.LEFT, padx=6)


# Data User Frame
# Input Fields
lbl1 = Label(wrapper3, text="ID")
lbl1.grid(row=0, column=0, padx=5, pady=3)
ent1 = Entry(wrapper3, textvariable=t1, state="disabled")
ent1.grid(row=0, column=1, padx=5, pady=3)

lbl2 = Label(wrapper3, text="First Name")
lbl2.grid(row=1, column=0, padx=5, pady=3)
ent2 = Entry(wrapper3, textvariable=t2)
ent2.grid(row=1, column=1, padx=5, pady=3)
# ent2.place(x=78, y=30, width=200) #width in pixels

lbl3 = Label(wrapper3, text="Last Name")
lbl3.grid(row=2, column=0, padx=5, pady=3)
ent3 = Entry(wrapper3, textvariable=t3)
ent3.grid(row=2, column=1, padx=5, pady=3)

# Buttons
add_btn = Button(wrapper3, text="Add New", command=add_new)
up_btn = Button(wrapper3, text="Update", command=update_data)
delete_btn = Button(wrapper3, text="Delete", command=delete_row)

add_btn.grid(row=3, column=0, padx=2, pady=1)
up_btn.grid(row=3, column=1, padx=2, pady=1)
delete_btn.grid(row=3, column=2, padx=2, pady=1)


root.mainloop()
