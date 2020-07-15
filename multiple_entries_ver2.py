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
	print(my_entries[0].get())
	for entries in my_entries:
		entry_list = entry_list + str(entries.get()) + '\n'
	my_label.config(text=entry_list)


def show_districts(mwd):
	ward_no=''
	mwds =[]
	temp_values=[]
	for k, v in mwd.items():
		if ward_no == '': ward_no = v[2]

		temp_values.append((v[3], v[2], v[0]))
		if ward_no != v[2]:
			ward_no = v[2] 						
			temp_values.pop()			
			# add last value to mwds
			mwds.append( temp_values.pop() )
			temp_values=[]
		print(k, v)
	mwds.append( temp_values.pop() )

	my_header.config(text=f"MUNICIPALITY: {v[4]}", font=("helvetica", 14))
	print(mwds)

	offset_y = 0

	for i, item in enumerate(mwds):
		print( f"{1}  mwd: {item} offset_y: {offset_y}" )

'''
			# Display Ward 
			if y==1:
				my_label = Label(root, width=10, text= f"Ward {ward_no}   [{mwd}]", fg="white", bg="grey")
				my_label.grid(row=y1, column=0, pady=1, padx=40)
				my_label = Label(root, width=10, text= f"Total: {mwd_id}")
				my_label.grid(row=y1+1, column=0, pady=1, padx=40)

			if exit_loop == True: break
			for x in range(1,9):
				my_label = Label(root, width=10, text= f"District {xx}", fg="white", bg="grey")
				my_label.grid(row=y1, column=x, pady=1, padx=5)
				my_entry = Entry(root, width=10)	 
				my_entry.grid(row=y2, column=x, pady=5, padx=5)

				# form data entry
				my_labels.append(my_label)
				my_entries.append(my_entry)
				xx +=1
				if xx > mwd:
					exit_loop = True
					break
			# Add extra offset for more than 2 line of district boxes		
			if y > 1: offset_y += y
			# print(f"Position: y {y} {i}")
'''


my_header = Label(root, text='MUNICIPALITY:', font=("helvetica", 14) )
my_header.grid(row=0, column=0, columnspan=9, pady=20)

my_label = Label(root, text='')
my_label.grid(row=30, column=0, pady=20)

my_button = Button(root, text="Click Me!", command=something)
my_button.grid(row=90, column=0, pady=20)		

muni ='TRENTON'
muni = 'EAST WINDSOR'
muni = 'HAMILTON'

query = "SELECT id, form_no, ward, district, Municipality FROM form_master WHERE municipality ='"+muni+"' ORDER BY municipality, ward, district"
cursor.execute(query)
rows = cursor.fetchall()
# print(len(rows))

mwd={}
idx=''
for row in rows:
	idx = f"{row[2]}-{row[3]}"
	mwd[idx]= row
	# print(f"{row[2]}-{row[3]}")	

show_districts(mwd)

root.mainloop()
