# main Pollbook application #

from tkinter import *
import tkinter as tk
from random import randint
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
import os, sys


from db import Database
db = Database('pollbook.db')


#Browse dir
def dir_browse():
	resp = new_file_validation() 
	if resp != '':
		messagebox.showerror("Validation Error:", resp)
		return

	csv_file_name =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("all files","*.*"),("jpeg files","*.jpg")))
	if csv_file_name != "":
		import_file(csv_file_name)
	else:
		return

# Create Popup function
def import_file(csv_file_name):
	f = os.path.basename(csv_file_name)
	mess = f"Importing {f} ....."
	slqlite_flash = Label(new_frame, text=f"{mess}", font=("helvetica", 14))

	response = messagebox.askokcancel("Importing CSV File", f'Import File {f} ? ')
	if response == 1:
		slqlite_flash.pack(pady=10)
		# ProgressBar
		global progress_bar 
		progress_bar = ttk.Progressbar(new_frame, orient=HORIZONTAL, length=300, mode="determinate")
		progress_bar.pack(pady=10)
		global percent
		percent = Label(new_frame, text="", anchor=S, font=("helvetica", 12))
		percent.pack(pady=5)

		table_name = project_name.get()
		resp = db.csv_to_sqlite(csv_file_name, progress_bar, percent, messagebox, table_name)
		if resp == False:
			new_file() # return	display results
		else:											
			open_file();

	else:
		new_file() # return	display results		


def get_cust_list():
	results = db.fetch_all('customers')
	options = ['Please Select....']
	for row in results:
		options.append(str(row[0])+" - "+row[1])

	return options

def get_cust_data(event):
	pass
	
 	# print(mycombo.get())
 	# option = mycombo.get()
 	# id = option.split("-")[0]
 	# db.fetch_by_id(id, 'customers')
 	# for i in rows:
 	# 	customer.set(i[1])
 	# 	contact.set(i[2])

def login():
	# u = username.get()
	# p = password.get()

	# results = db.confirm_login(u, p )
	# username.set(' ')
	# password.set(' ')

	# if results == None:
	# 	resp = f"The Username {u} and or the Password {p} is incorrect!"
	# 	messagebox.showerror("Login Validation Error:", resp)
	# else:	
	# 	logged_in()	

	logged_in()	

#Create our new_file function
def new_file():
	reset_run_frame(new_frame)

	# Page Header 
	text_mess = "Create New Pollbook: Import New File."
	my_flash = Label(new_frame, text=f"{text_mess}", font=("helvetica", 14))
	my_flash.pack(pady=10)

	# Get Inputs
	options = get_cust_list();
	project_account_lbl = Label(new_frame, text='Account', font=("helvetica", 12)).pack(pady=10)

	global mycombo
	mycombo = ttk.Combobox(new_frame, textvariable=opts, width=30, font=("helvetica", 12))	
	mycombo['values'] = options
	mycombo.pack(padx=10, pady=6)
	mycombo.current(0)
	mycombo.bind("<<ComboboxSelected>>", get_cust_data )    

	global project_name 
	project_name_lbl = Label(new_frame, text="Project Name", font=("helvetica", 12)).pack(pady=10)	
	project_name = Entry(new_frame, font=("helvetica", 12))
	project_name.pack(ipadx=100, ipady=5)

	# Buttons
	add_btn = Button(new_frame, text='Get File', width=12, command=dir_browse).pack(pady=10)

#Create our open_file function
def open_file():
	reset_run_frame(open_frame)
	# Page Header 
	text_mess = "Project: "	
	my_flash = Label(open_frame, text=f"{text_mess}", font=("helvetica", 14))
	my_flash.pack(pady=5)

	# Create Section Frames
	wrapper1 = LabelFrame(open_frame, text="Dispaly List")
	wrapper2 = LabelFrame(open_frame, text="Search")
	wrapper3 = LabelFrame(open_frame, text="Customer Data")

	wrapper1.pack(fill="both", expand="yes", padx="20", pady="10")
	wrapper2.pack(fill="both", expand="yes", padx="20", pady="10")
	wrapper3.pack(fill="both", expand="yes", padx="20", pady="10")


	# Display List Frame (Treeview)
	global trv
	trv = ttk.Treeview(wrapper1, column=(1,2,3), show="headings", height="12")
	trv.pack()

	# trv.heading(1, text="Record No")
	# trv.column(1, minwidth=0, width=100, anchor=E, stretch=YES)
	trv.heading(1, text="Municipality")
	trv.column(1, minwidth=0, width=170, stretch=YES)
	trv.heading(2, text="Ward")
	trv.column(2, minwidth=0, anchor=E, width=100, stretch=NO)
	trv.heading(3, text="District")
	trv.column(3, minwidth=0, anchor=E, width=100, stretch=NO)

	# Get row data
	trv.bind('<Double 1>', getrow )

	# Buttons
	expbtn = Button(wrapper1, text="Export CSV", command=export_csv)
	expbtn.pack(side=tk.LEFT, padx=10, pady=10)


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



def reset_run_frame(frame_opt):
	hide_menu_frames()
	frame_opt.pack(fill="both", expand=1)


# Hide Frame Function
def hide_menu_frames():
	# Destroy the children widgets in each frame
	for widget in new_frame.winfo_children():
		widget.destroy()
	for widget in open_frame.winfo_children():
		widget.destroy()
	for widget in start_frame.winfo_children():
		widget.destroy()

	# Hide all frames
	new_frame.pack_forget()
	open_frame.pack_forget()
	start_frame.pack_forget()

# Logged in
def logged_in():
	hide_menu_frames()
	start_frame.pack(fill="both", expand=1)
	start_label = Label(start_frame, text="Election Poll Books", font=("Helvetica", 18)).pack(pady=40)
	restore_menu()


# Start Screen
def home():
	hide_menu_frames()
	start_frame.pack(fill="both", expand=1)
	start_label = Label(start_frame, text="Election Poll Books", font=("Helvetica", 18)).pack(pady=40)

	global username
	username_lbl = Label(start_frame, text="Username", font=("helvetica", 12)).pack(pady=10)	
	username1 = Entry(start_frame, textvariable=username, font=("helvetica", 12))
	username1.pack(ipadx=100, ipady=5)

	global password
	password_lbl = Label(start_frame, text="Password", font=("helvetica", 12)).pack(pady=10)	
	password1 = Entry(start_frame, textvariable=password, font=("helvetica", 12))
	password1.pack(ipadx=100, ipady=5)

	# Buttons
	submit_btn = Button(start_frame, text='Submit', width=12, command=login).pack(pady=10)
	remove_menu()

def remove_menu():
    emptyMenu = Menu(root)
    root.config(menu=emptyMenu)

def restore_menu():    
	root.config(menu=my_menu)

#Form Validation
def new_file_validation():
	print(mycombo.current())
	error_mess = ''
	if  mycombo.current() == 0:
		error_mess += f"\nAccount not selected. Please select one to continue.\n"

	if project_name.get() =='':
		error_mess += f"\nProject Name empty and is required\n"

	if project_name.get() !='':
		table_name = project_name.get()
		chk_name = table_name.replace(' ', '_')
		table_exists = db.check_table_exists(chk_name)
		if table_exists == 1:
			error_mess = f"Project name is aready taken. Please select another name."
			project_name.delete(0, END) #deletes the current value

	return error_mess

#################
# 
#################
# functions
def update(rows):
	trv.delete(*trv.get_children())
	for i in rows:
		trv.insert("","end", values=i)

def search():
	pass

def clear():
	# clear_inputs()	
	table_name ='test'
	rows = db.fetch_voters(table_name)
	update(rows)

def clear_inputs():
	pass

def getrow(event):
	pass

	# rowid = trv.identify_row(event.y)
	# item = trv.item(trv.focus())
	# t1.set(item['values'][0])
	# t2.set(item['values'][1])
	# t3.set(item['values'][2])		
	# t4.set(item['values'][3])		
	# t5.set(item['values'][4])

def update_data():
	pass

def add_new():
	pass

def delete_row():
	pass

def export_csv():
	pass

def import_data():
	pass

# sys.exit(f"Quit App.............")
def get_attributes(widget):
	widg = widget
	keys = widg.keys()
	for key in keys:
		print("Attribute: {:<20}".format(key), end=' ')
		value = widg[key]
		vtype = type(value)
		print('Type: {:<30} Value: {}'.format(str(vtype), value))



#####################################################
# Create Tk Window
#####################################################
root = Tk()
root.title("Poll Books App!")
root.resizable(False, False)
root.geometry("800x700")

# Gets the requested values of the height and widht.
windowWidth = root.winfo_reqwidth()
windowHeight = root.winfo_reqheight()
print("Width",windowWidth,"Height",windowHeight)
 
# Gets both half the screen width/height and window width/height
positionRight = int(root.winfo_screenwidth()/3 - windowWidth/2)
positionDown = int(root.winfo_screenheight()/3 - windowHeight/2)
 
# Positions the window in the center of the page.
root.geometry("+{}+{}".format(positionRight, positionDown))
# root.iconbitmap('c:/guis/exe/codemy.ico')

##################
# global options #
##################
project_name = StringVar()
password = StringVar()
username = StringVar()
opts = StringVar()
options = []

q = StringVar()
t1 = StringVar()
t2 = StringVar()
t3 = StringVar()

#Define Main Menu
my_menu = Menu(root)
root.config(menu=my_menu)

# Create menu items
poll_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="File", menu=poll_menu)
poll_menu.add_command(label="Create Poll Book", command=lambda: new_file())
poll_menu.add_command(label="Open Poll Book", command=lambda: open_file())
poll_menu.add_separator()
poll_menu.add_command(label="Close Files", command=lambda: logged_in())
poll_menu.add_separator()
poll_menu.add_command(label="Exit", command=root.quit)

# Create menu items
print_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="Print Files", menu=print_menu)
print_menu.add_command(label="New Poll Book", command=lambda: new_file())
print_menu.add_command(label="Open Poll Book", command=lambda: open_file())
print_menu.add_separator()
print_menu.add_command(label="Close Files", command=lambda: logged_in())
print_menu.add_separator()
print_menu.add_command(label="Exit", command=root.quit)


# Create Math Frames
new_frame = Frame(root) #, highlightbackground="black", highlightthickness=1
open_frame = Frame(root)
start_frame = Frame(root)

# Show the start screen
home()

root.mainloop()