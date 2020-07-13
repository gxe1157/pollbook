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
	cnt = 9 #len(mwds)
	# for i, mwd in enumerate(mwds):
	# 	pass

	rows_dn = math.ceil(((cnt/9)*2)+2)
	# if rows_dn == 1: rows_dn = 2

	# Display Ward 
	my_label = Label(root, width=10, text= f"Ward {cnt}", fg="white", bg="grey")
	my_label.grid(row=1, column=0, pady=1, padx=5)

	exit_loop = False
	xx = 1

	print( f"cnt 2 : {cnt}  rows_dn: {rows_dn}" )
	for y in range(1,rows_dn,2):
		print(y)
		y1 = y
		y2 = y+1

		if exit_loop == True: break
		for x in range(1,9):
			my_label = Label(root, width=10, text= f"District {xx}", fg="white", bg="grey")
			my_label.grid(row=y1, column=x, pady=1, padx=5)

			my_entry = Entry(root, width=10)	 
			my_entry.grid(row=y2, column=x, pady=5, padx=5)

			my_entries.append(my_entry)
			my_labels.append(my_label)
			xx +=1

			print(f"xx: {xx} -> cnt: {cnt}")
			if xx > cnt:
				print(f"xx: {xx} -> cnt: {cnt}")
				exit_loop = True
				break


my_header = Label(root, text='Municipality: East Windsor', font=("helvetica", 10) )
my_header.grid(row=0, column=0, pady=20)


my_button = Button(root, text="Click Me!", command=something)
my_button.grid(row=21, column=0, pady=20)

my_label = Label(root, text='')
my_label.grid(row=21, column=0, pady=20)

muni_ward_dist = [ 5,6,2,7,2,4 ]

show_districts(muni_ward_dist)

root.mainloop()
