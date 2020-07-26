# main Pollbook application #
from tkinter import  *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from random import randint
from tkinter import filedialog
import datetime
import os, sys


from db import Database
db = Database('pollbook.db')

#========== declare global here =============
muni_list = {}
months = ['---','Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'July', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']
selected_table = ''

#============================= Frame options start ==============================================
# Login
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

# Logged in
def logged_in():
	hide_menu_frames()
	start_frame.pack(fill="both", expand=1)
	start_label = Label(start_frame, text="Election Poll Books", font=("Helvetica", 18)).pack(pady=40)
	restore_menu()

# Create Poll Book
def new_file():
	remove_menu()
	reset_run_frame(new_frame)
	muni_list={}
	#======================= Inner functions ===================================================
	#Get file to import
	def dir_browse():
		resp, prj_name = new_file_validation() 
		if resp != '':
			messagebox.showerror("Validation Error:", resp)
			return

		f = f"{prj_name}. Continue or Cancel?"	
		if messagebox.askokcancel("Please Confirm:", f'{f} '):
			csv_file_name =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("all files","*.*"),("jpeg files","*.jpg")))
			if csv_file_name != "":
				import_file(csv_file_name)

		return

	#Form Validation
	def new_file_validation():
		project_name.config(state=NORMAL)			

		error_mess = ''
		if  client_combo.current() == 0:
			error_mess += f"\nAccount not selected. Please select one to continue.\n"

		if  event_combo.current() == 0:
			error_mess += f"\nEvent not selected. Please select one to continue.\n"

		if  event_dt_month_combo.current() == 0:
			error_mess += f"\nMonth not selected. Please select one to continue.\n"

		table_name = client_combo.get()+' '+event_combo.get()+' '+event_dt_month_combo.get()+' '+event_dt_year_combo.get()
		chk_name = table_name.replace(' ', '_')
		print('table_name:', chk_name);

		table_exists = db.check_table_exists(chk_name)

		if table_exists == 1:
			project_name.insert(END, table_name)
			error_mess = f"Project name {table_name} is aready taken.\nPlease select another name."
			project_name.delete(0, END) #deletes the current value
		else:
			project_name.insert(END, table_name)

		project_name.config(state=DISABLED)		
		return (error_mess, project_name.get())


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
				global selected_table
				selected_table = table_name
				open_file()
		else:
			new_file() # return	display results		

	header_text = "Create New Pollbook: Import New File."
	show_page(header_text)		

	# Buttons
	buttonframe = Frame(new_frame)
	buttonframe.pack(pady=20)

	button1 = Button(buttonframe, text='Return', width=12, command=logged_in)
	button1.pack( side = LEFT)

	button2 = Button(buttonframe, text='Clear Fields', width=12, command=new_file)
	button2.pack( side = LEFT )

	button3 = Button(buttonframe, text='Get File', width=12, command=dir_browse)
	button3.pack( side = LEFT )


def get_file():
	remove_menu()	
	reset_run_frame(new_frame)
	muni_list={}

	header_text = "Pollbook Lookup:"
	show_page(header_text)
	# Buttons
	buttonframe = Frame(new_frame)
	buttonframe.pack(pady=20)

	button1 = Button(buttonframe, text='Return', width=12, command=logged_in)
	button1.pack( side = LEFT)

	button2 = Button(buttonframe, text='Clear Fields', width=12, command=get_file)
	button2.pack( side = LEFT )

def show_page(header_text):
	#======================= Inner functions ===================================================
	def get_cust_list():
		results = db.fetch_all('customers')
		options = ['Please Select....']
		for row in results:
			options.append(row[1])
			muni_list[row[1]] = row[0]
		return options

	def get_event_data():
		results = db.fetch_all('election_events')
		options = ['Please Select....']
		for row in results:
			options.append(row[1])
		return options

	def get_event_dt(year):
		options= []

		for dy in range(year, year+5):
			options.append(dy)
		print(options)
		return options

	def get_cust_selected(event):
		option = client_combo.get()
		try:
			if listbox_jobs.winfo_exists():
				listbox_jobs_update(option)
		except:
			pass

	# Page Header 
	my_flash = Label(new_frame, text=f"{header_text}", font=("helvetica", 14))
	my_flash.pack(pady=10)
	project_account_lbl = Label(new_frame, text='Account', font=("helvetica", 12)).pack(pady=10)

	global client_combo
	client_combo = ttk.Combobox(new_frame, width=20, font=("helvetica", 12))	
	client_combo['values'] = get_cust_list()
	client_combo.pack(padx=10, pady=6)
	client_combo.current(0)
	client_combo.bind("<<ComboboxSelected>>", get_cust_selected )    

	global project_name 
	project_name_lbl = Label(new_frame, text="Project Name", font=("helvetica", 12))	
	project_event_lbl = Label(new_frame, text="Event Name", font=("helvetica", 12))	
	project_date_lbl = Label(new_frame, text="Event Date", font=("helvetica", 12))	

	if header_text == "Pollbook Lookup:":
		jobs_listbox()
	else:
		project_event_lbl.pack(pady=10)
		global event_combo
		event_combo = ttk.Combobox(new_frame, width=20, font=("helvetica", 12))	
		event_combo['values'] = get_event_data()
		event_combo.pack(padx=10, pady=6)
		event_combo.current(0)


		project_date_lbl.pack(pady=10)

		comboframe = Frame(new_frame)
		comboframe.pack()

		global event_dt_month_combo
		event_dt_month_combo = ttk.Combobox(comboframe, width=6, font=("helvetica", 12))	
		event_dt_month_combo['values'] = months
		event_dt_month_combo.pack( side=LEFT, padx=5)
		event_dt_month_combo.current(0)

		global event_dt_year_combo
		year = datetime.datetime.today().year		
		event_dt_year_combo = ttk.Combobox(comboframe, width=6, font=("helvetica", 12))	
		event_dt_year_combo['values'] = get_event_dt(year)
		event_dt_year_combo.pack( side=LEFT )
		event_dt_year_combo.current(0)

		project_name_lbl.pack(pady=10)	
		project_name = Entry(new_frame, font=("helvetica", 12))
		project_name.pack(ipadx=80, ipady=5)
		project_name.config(state=DISABLED)				



def jobs_listbox():
	wrapper_listbox_jobs = Frame(new_frame, relief="raised" )
	wrapper_listbox_jobs.pack(fill="none", expand="no", padx="10", pady="5")
	#Scrollbar
	scrollbar_jobs = Scrollbar(wrapper_listbox_jobs, orient=VERTICAL)
	#list Box - SINGLE, BROWSE, MULTIPLE, EXTENED
	global listbox_jobs
	listbox_jobs = Listbox(wrapper_listbox_jobs, width=65, yscrollcommand=scrollbar_jobs.set)
	scrollbar_jobs.config(command=listbox_jobs.yview) 		#scrollbar configure
	scrollbar_jobs.pack(side=RIGHT, fill=Y)
	wrapper_listbox_jobs.pack()
	listbox_jobs.pack()
	listbox_jobs.bind('<<ListboxSelect>>', listbox_jobs_select) 	# Bind select

def listbox_jobs_select(event):
	try:
		global selected_table
		selected_table = listbox_jobs.get(ANCHOR)
		response = messagebox.askokcancel("Open SQL File", f'Open File {selected_table} ? ')
		if response == 1:
			open_file()

	except IndexError:
		pass

def listbox_jobs_update(option):	
	listbox_jobs.delete(0, END)			
	if option !='Please Select....':
		results = db.fetch_tables_list()
		for result in results:
			chk_str = option.replace(' ', '_') # If 
			file_name = result[0]
			if option in file_name and '_fm' not in file_name:
				# print('found it! '+file_name)
				listbox_jobs.insert(END, file_name )

		if listbox_jobs.size() == 0:
			listbox_jobs.insert(END, 'Records not found..........' )


# Open Poll Book
def open_file():
	reset_run_frame(open_frame)

	# Page Header 
	text_mess = "Project: "	
	my_flash = Label(open_frame, text=f"{text_mess}", font=("helvetica", 14))
	my_flash.pack(pady=5)

	# Create Section Frames
	wrapper1 = LabelFrame(open_frame, text="Dispaly List")
	wrapper2 = LabelFrame(open_frame, text="Customer Data")
	wrapper3 = LabelFrame(open_frame, text="Update Activity")

	wrapper1.pack(fill="both", expand="yes", padx="20", pady="10")
	wrapper2.pack(fill="both", expand="yes", padx="20", pady="10")
	wrapper3.pack(fill="both", expand="yes", padx="20", pady="10")

	# Combobox for select municipality
	options = fetch_municipalies();

	global mycombo
	mycombo = ttk.Combobox(wrapper1, textvariable=opts, width=30, font=("helvetica", 12))	
	mycombo['values'] = options
	mycombo.pack(padx=5, pady=10)
	mycombo.current(0)
	mycombo.bind("<<ComboboxSelected>>", get_municipality )    

	# Display List Frame (Treeview)
	global trv
	trv = ttk.Treeview(wrapper1, column=(1,2,3,4,5,6), show="headings", height="12", selectmode='browse')
	# trv.place(x=30, y=45)
	global vsb
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

	
	#========================== Select a job number and display default records =======================
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
	buttonframe = Frame(start_frame)
	buttonframe.pack(pady=20)

	button1 = Button(buttonframe, text='Exit', width=12, command=root.quit)
	button1.pack( side = LEFT )

	button2 = Button(buttonframe, text='Submit', width=12, command=logged_in)
	button2.pack( side = LEFT)

	remove_menu()

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
	for widget in mwdForm_frame.winfo_children():
		widget.destroy()

	# Hide all frames
	new_frame.pack_forget()
	open_frame.pack_forget()
	start_frame.pack_forget()
	mwdForm_frame.pack_forget()

def remove_menu():
    emptyMenu = Menu(root)
    root.config(menu=emptyMenu)

def restore_menu():    
	root.config(menu=my_menu)

#============================= Funtions  ======================================================
def update(rows):
	trv.delete(*trv.get_children())
	for i in rows:
		trv.insert('', 'end', values=i)

def search(muni=None):
	if muni == None or muni =='All...':
		clear()
	else:
		sql_file = selected_table # This is global
		q2 = muni.upper()
		rows = db.fetch_mwd(sql_file, q2)
		update(rows)

def clear():
	sql_file = selected_table # This is global	

	clear_inputs()	
	rows = db.fetch_mwd(sql_file)
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
	sql_file = selected_table+"_fm" # This is global		
	rec_id = t1.get()
	form_no = t2.get()
	muni = t3.get()

	query = f"UPDATE {sql_file} SET form_no = {form_no} WHERE id = {rec_id}"
	db.run_query(query)


	search(muni)

def add_new():
	pass

	# fname = t2.get()
	# lname = t3.get()

	# query = "INSERT INTO users(id, first_name, last_name) VALUES(NULL, %s, %s)"
	# cursor.execute(query, (fname, lname))
	# db.commit()	
	# clear()

def delete_row():
	pass

	# rec_id = t1.get()	
	# if messagebox.askyesno("Confirm Delete","Are You sure you want to delete this record?"):
	# 	query = "DELETE FROM test WHERE id="+rec_id
	# 	cursor.execute(query)
	# 	db.commit()
	# 	clear()
	# else:
	# 	return True

## Combobox - Select Dropdown
def fetch_municipalies():
	sql_file = selected_table # this is global
	rows = db.fetch_clients(sql_file)

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

# sys.exit(f"Quit App.............")


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

def open_directory():
	top = Toplevel()
	top.title('window 2')
	top.geometry("400x300")
	top.geometry("+{}+{}".format(positionRight, positionDown))
	top.grab_set()  #.grab_release() # to return to normal
	bnt2 = Button(top, text="close", command=top.destroy).pack(pady=10)


project_name = StringVar()
password = StringVar()
username = StringVar()
opts = StringVar()
options = []

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

#Define Main Menu
my_menu = Menu(root)
root.config(menu=my_menu)

# Create menu items
poll_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="File", menu=poll_menu)
poll_menu.add_command(label="Create Poll Book", command=new_file)
poll_menu.add_command(label="Open Poll Book", command=get_file)
poll_menu.add_separator()
poll_menu.add_command(label="Exit", command=root.quit)

# Create menu items
# print_menu = Menu(my_menu, tearoff=0)
# my_menu.add_cascade(label="Print Files", menu=print_menu)
# print_menu.add_command(label="New Poll Book", command=lambda: new_file())
# print_menu.add_command(label="Open Poll Book", command=lambda: get_file())
# print_menu.add_separator()
# print_menu.add_command(label="Exit", command=root.quit)


# Create Math Frames
new_frame = Frame(root) #, highlightbackground="black", highlightthickness=1
open_frame = Frame(root)
start_frame = Frame(root)
mwdForm_frame = Frame(root)

# Show the start screen
home()

root.mainloop()