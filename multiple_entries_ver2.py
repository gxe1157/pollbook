from tkinter import  *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import math, sys


# Move this to database class
sqlite = True  # choose mysql or sqlite
if sqlite == True:
	# sqlite3
	import sqlite3	
	from db import Database
	db = 'pollbook.db'
	conn = sqlite3.connect(db)
	cursor = conn.cursor()


root = Tk()
root.title("My Application")
root.geometry("900x700")
root.resizable(False, False)

my_entries = []
my_labels = []

def something():
	entry_list = ''
	my_entries[0].insert(0,'text')
	print(my_entries[0].get())
	# print(dir(my_entries[0]))
	# print(dir(list))	

	for e, entries in enumerate(my_entries):
		entry_list += f"{e} {entries.get()} \n"

	print(entry_list)
   
	# my_label.config(text=entry_list)

def show_ward( r1, r2, ward_no):
	# v[id, form_no, ward, district, Municipalit]
	my_label = Label(root, width=10, text= f"Ward {ward_no}", fg="white", bg="grey")
	my_label.grid(row=r1, column=0, pady=1, padx=40)
	my_label = Label(root, width=10, text= f"Total: 0")
	my_label.grid(row=r2, column=0, pady=1, padx=40)


def show_districts(mwds):
	# y=True
	x = 1
	y1 = 1
	y2 = 2
	offset = 2
	ward_no = mwds[0][2]

	for i, item in enumerate(mwds):
		item = ['' if x is None else x for x in item]

		show_ward_no = True
		if i == 0:
			show_ward(y1, y2, item[2])			

		if ward_no != item[2]:
			ward_no = item[2]
			show_ward_no = False
			x=9

		if x == 9:
			x=1
			if 	show_ward_no == True and len(ward_no)>0:
				show_ward(y1, y2, item[2])						
			y1 += offset
			y2 += offset

		my_label = Label(root, width=10, text= f"District {item[3]}", fg="white", bg="grey")
		my_label.grid(row=y1, column=x, pady=1, padx=5)
		my_entry = Entry(root, width=10)	 
		my_entry.grid(row=y2, column=x, pady=5, padx=5)

		# form data entry
		my_labels.append(my_label)
		if item[1] == '':
			my_entry.config({"background": "#DEDCDC"})			

		my_entry.insert(0, f"{item[1]}")
		my_entries.append(my_entry)


		x += 1

	my_header.config(text=f"MUNICIPALITY: {item[4]}", font=("helvetica", 14))

my_header = Label(root, text='MUNICIPALITY:', font=("helvetica", 14) )
my_header.grid(row=0, column=0, columnspan=9, pady=20)

my_button = Button(root, text="Click Me!", command=something)
my_button.grid(row=90, column=0, pady=20)		

muni ='TRENTON'
# muni = 'EAST WINDSOR'
# muni = 'HAMILTON'

query = "SELECT id, form_no, ward, district, Municipality FROM form_master WHERE municipality ='"+muni+"' ORDER BY municipality, ward, district"
cursor.execute(query)
rows = cursor.fetchall()
show_districts(rows)

root.mainloop()
