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
	init= True
	dist_count=0
	recno=0
	track=''

	mwds =[]
	for k, v in mwd.items():
		if init == True:
			track = v[2]
			recno = v[0]			
			init= False

		if track != v[2]:
			track = v[2] 
			recno = v[0]
			mwds.append((dist_count,track,recno))
			dist_count = 1
			# print(f"{track} {dist_count}") 						
		else:
			dist_count +=1
			# print(f"{track} {dist_count}") 			
		# print(k, v)

	my_header.config(text=f"MUNICIPALITY: {v[4]}", font=("helvetica", 14))
	mwds.append((dist_count, track, recno ))
	print(mwds)
	# sys.exit("quit..........")		

	offset_y = 0
	for i, item in enumerate(mwds):
		mwd = item[0]
		ward_no = item[1]
		mdw_id= item[2]

		offset_y += 2		
		rows_dn = math.ceil(((mwd/9)*2)+2)
		exit_loop = False
		xx = 1

		print( f"mwd 2 : {mwd}  rows_dn: {rows_dn}   offset_y: {offset_y}" )
		for y in range(1,rows_dn,2):
			y1 = y+offset_y
			y2 = y+1+offset_y

			# Display Ward 
			if y==1:
				my_label = Label(root, width=10, text= f"Ward {ward_no}   [{mwd}]", fg="white", bg="grey")
				my_label.grid(row=y1, column=0, pady=1, padx=40)
				my_label = Label(root, width=10, text= f"Total: {mdw_id}")
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



my_header = Label(root, text='MUNICIPALITY:', font=("helvetica", 14) )
my_header.grid(row=0, column=0, columnspan=9, pady=20)

my_button = Button(root, text="Click Me!", command=something)
my_button.grid(row=90, column=0, pady=20)		

my_label = Label(root, text='')
my_label.grid(row=30, column=0, pady=20)

muni ='TRENTON'
muni = 'EAST WINDSOR'
muni = 'HAMILTON'

# query = "SELECT ID, form_no, municipality, ward, district FROM form_master WHERE municipality ='"+muni+"' ORDER BY municipality, ward, district"
query = "SELECT id, form_no, ward, district, Municipality FROM form_master WHERE municipality ='"+muni+"' ORDER BY municipality, ward, district"

cursor.execute(query)
rows = cursor.fetchall()
# print(len(rows))

mwd={}
idx=''
for i, row in enumerate(rows):
	# print(row)
	if i==0: key = row[2]

	if key != row[2]:
		idx = f"{row[2]}-{row[3]}"
		mwd[idx]= row
		key = row[2]
	else:
		idx = f"{row[2]}-{row[3]}"
		mwd[idx]= row

show_districts(mwd)

root.mainloop()
