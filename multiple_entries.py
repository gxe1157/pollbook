from tkinter import *
import math

root = Tk()
root.title("My Application")
root.geometry("900x700")
# root.resizable(False, False)

my_entries = []
my_labels = []

def something():
	entry_list = ''
	for entries in my_entries:
		entry_list = entry_list + str(entries.get()) + '\n'
		my_label.config(text=entry_list)


def show_districts(mwds):
	offset_y = 0
	for i, mwd in enumerate(mwds):
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
				my_label = Label(root, width=10, text= f"Ward {i}   [{mwd}]", fg="white", bg="grey")
				my_label.grid(row=y1, column=0, pady=1, padx=5)

			if exit_loop == True: break
			for x in range(1,9):
				my_label = Label(root, width=10, text= f"District {xx}", fg="white", bg="grey")
				my_label.grid(row=y1, column=x, pady=1, padx=5)

				my_entry = Entry(root, width=10)	 
				my_entry.grid(row=y2, column=x, pady=5, padx=5)

				my_entries.append(my_entry)
				my_labels.append(my_label)
				xx +=1
				if xx > mwd:
					exit_loop = True
					break
			# Add extra offset for more than 2 line of district boxes		
			if y > 1: offset_y += y
		


my_header = Label(root, text='Municipality: East Windsor', font=("helvetica", 10) )
my_header.grid(row=0, column=0, pady=20)


my_button = Button(root, text="Click Me!", command=something)
my_button.grid(row=29, column=0, pady=20)

my_label = Label(root, text='')
my_label.grid(row=30, column=0, pady=20)

muni_ward_dist = [ 40 ]

show_districts(muni_ward_dist)

root.mainloop()
