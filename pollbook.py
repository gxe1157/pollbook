# main Pollbook application #
from tkinter import  *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from random import randint
from tkinter import filedialog
from tkinter import Widget
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
		error_mess, prj_name = new_file_validation() 
		if error_mess != '':
			messagebox.showerror("Validation Error:", error_mess)
			return

		f = f"Your Project Name is {prj_name}"	
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
		table_exists = db.check_table_exists(chk_name)
		project_name.insert(END, chk_name)

		if table_exists == 1:
			error_mess = f"Project name {table_name} is aready taken.\nPlease select another name."

		if 	error_mess != '' or table_exists == 1: 
			project_name.delete(0, END)
			
		project_name.config(state=DISABLED)		
		return (error_mess, chk_name)


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
	button1.bind("<Enter>", lambda event: btn_status(event, button1))
	button1.bind("<Leave>", lambda event: btn_status_out(event, button1))

	button2 = Button(buttonframe, text='Clear Fields', width=12, command=new_file)
	button2.pack( side = LEFT )
	button2.bind("<Enter>", lambda event: btn_status(event, button2))
	button2.bind("<Leave>", lambda event: btn_status_out(event, button2))

	button3 = Button(buttonframe, text='Create Job', width=12, command=dir_browse)
	button3.pack( side = LEFT )
	button3.bind("<Enter>", lambda event: btn_status(event, button3))
	button3.bind("<Leave>", lambda event: btn_status_out(event, button3))


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
	button1.bind("<Enter>", lambda event: btn_status(event, button1))
	button1.bind("<Leave>", lambda event: btn_status_out(event, button1))

	button2 = Button(buttonframe, text='Clear Fields', width=12, command=get_file)
	button2.pack( side = LEFT )
	button2.bind("<Enter>", lambda event: btn_status(event, button2))
	button2.bind("<Leave>", lambda event: btn_status_out(event, button2))

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
		return options

	def get_cust_selected(event):
		option = client_combo.get()
		try:
			if listbox_jobs.winfo_exists():
				listbox_jobs.delete(0, END)
				if option !='Please Select....':
					listbox_jobs.config(state=NORMAL, bg="#faf6e1")													
					results = db.fetch_tables_list()
					for result in results:
						chk_str = option.replace(' ', '_') # If 
						file_name = result[0]
						if option in file_name and '_fm' not in file_name:
							# print('found it! '+file_name)
							listbox_jobs.insert(END, file_name )

					if listbox_jobs.size() == 0:
						listbox_jobs.insert(END, 'Records not found..........' )				
						messagebox.showwarning("Databae Lookup", 'Records not found..........')
				else:
					listbox_jobs.config(state=DISABLED, bg="#e6e6e6")									
		except:
			pass

	def jobs_listbox(my_flash):
		frame = Frame(new_frame, relief="raised")
		scrollbar = Scrollbar(frame, orient=VERTICAL)
		global listbox_jobs
		listbox_jobs = Listbox(frame, width=40, font=("helvetica", 11), yscrollcommand=scrollbar.set)
		scrollbar.config(command=listbox_jobs.yview)
		scrollbar.pack(side=RIGHT, fill=Y)
		listbox_jobs.pack(side=LEFT, fill=NONE, expand=NO)		
		listbox_jobs.bind('<<ListboxSelect>>', lambda event: listbox_jobs_select(event, my_flash)) 	# Bind select
		frame.pack()


	def listbox_jobs_select(event, my_flash):
		# print('listbox_jobs_selected',my_flash.cget('text'))
		try:
			global selected_table
			selected_table = listbox_jobs.get(ANCHOR)

			if selected_table == 'Records not found..........':
				messagebox.showwarning("Database Look", selected_table)
				return

			if client_combo.get() !='Please Select....':
				response = messagebox.askokcancel("Open SQL File", f'Open File {selected_table} ? ')
				if response == 1:
					open_file()

		except IndexError:
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
		jobs_listbox(my_flash)
		listbox_jobs.config(state=DISABLED, bg="#e6e6e6")						
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


#============================= Inner Funtions =========================================
def update(rows):
	trv.delete(*trv.get_children())
	for i in rows:
		trv.insert('', 'end', values=i)

def search():
	if mycombo.get() =='All...':
		clear()
	else:
		get_rows()

def get_rows():
	clear_inputs()
	muni = mycombo.get().upper()
	rows = db.fetch_mwd(selected_table, muni) # This is global
	update(rows)

def clear():
	clear_inputs()	
	rows = db.fetch_mwd(selected_table) # This is global	
	update(rows)

def clear_inputs():
	t1.set(' ')
	t2.set(' ')
	t3.set(' ')		
	t4.set(' ')		
	t5.set(' ')		
	t1a.set(' ')
	t1b.set(' ')
	t1c.set(' ')		

	customer_data_toggle(False)

def update_data():
	form_no = t2.get()
	municipality = t3.get()

	ward = t4.get() 
	if (ward != ''):
		ward = str(ward) if len(str(ward))==2 else '0'+str(ward)	

	dist_temp = t5.get()
	district = str(dist_temp) if len(str(dist_temp))==2 else '0'+str(dist_temp)	
	poll_name = t1a.get()
	poll_address = t1b.get()
	poll_location = t1c.get()		

	data = [(form_no, poll_name, poll_address,  poll_location, municipality, ward, district ),]
	table_name = selected_table     # global var
	set_columns = '''form_no = ?, poll_name = ?, poll_address = ?, poll_location = ?'''
	where_condition = '''municipality = ? and ward = ? and district = ?'''

	table_name = selected_table     # global var
	rows_updated = db.updateMultipleRecords(set_columns, where_condition, data, table_name)
	display_mess(rows_updated)

	table_name += "_fm"     # global var		
	rows_updated = db.updateMultipleRecords(set_columns, where_condition, data, table_name)
	display_mess(rows_updated, False)
	search()

def display_mess(rows_updated, show_mess=True):
	if rows_updated > 0 and show_mess:
		messagebox.showinfo("SQL Success!", f"{rows_updated} Record(s) updated successfully")			

	if rows_updated==0:
		messagebox.showerror("SQL Failed", f"Failed to update record(s)")
		sys.exit('Fatal Error..............')

def getrow(event):
	rowid = trv.identify_row(event.y)
	item = trv.item(trv.focus())

	# enable these inputs fields and buttons
	customer_data_toggle(True)
	t1.set(item['values'][0])
	t2.set(item['values'][1])
	t3.set(item['values'][2])		
	t4.set(item['values'][3])		
	t5.set(item['values'][4])		

	t1a.set(item['values'][6])
	t1b.set(item['values'][7])
	t1c.set(item['values'][8])		

def customer_data_toggle(isNormal):
	# print(f"customer_data_toggle -- {isNormal}")
	status = "normal" if isNormal else "disabled"
	up_btn1.config(state=status)
	up_btn2.config(state=status)
	up_btn3.config(state=status)	
	ent2.config(state=status)
	ent1a.config(state=status)			
	ent1b.config(state=status)			
	ent1c.config(state=status)

	# topwindow toggle button 
	muni = mycombo.get()
	status = "disabled" if muni=='All...' else 'normal'
	up_btn5.config(state=status)					


## Combobox - Select Dropdown
def fetch_municipalies():
	rows = db.fetch_clients(selected_table) #SELECTED_TABLE IS GLOBAL
	options = ['All...']
	for row in rows:
		options.append(f"{row[1]}")
	return options

def get_municipality(event):
	muni = mycombo.get()
	search()

## my_listbox functions
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

def delete_multiple():
	for item in reverse(my_listbox.curselection()):
		my_listbox.delete(item)

def btn_status(event, btn_state):
	if str(btn_state['state']) == 'disabled':
		btn_state['bg'] = "#d1c8b0"
	else:
		btn_state['bg'] = "#b0d1b9"
	# print('button status in ')

def btn_status_out(event, btn_state):
	btn_state['bg'] = "SystemButtonFace"
	# print('button status out')


# Open Poll Book
def open_file(topLevel_update=None):
	reset_run_frame(open_frame)

	# Page Header 
	header_text = selected_table.replace('_', ' ')
	text_mess = f"{header_text}"	
	my_flash = Label(open_frame, text=f"{text_mess}", font=("helvetica", 12), relief= RIDGE, bd=5)
	my_flash.pack(ipadx=20, ipady=5, pady=2)

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
	mycombo = ttk.Combobox(wrapper1, textvariable=opts, width=30, font=("helvetica", 10))	
	mycombo['values'] = options
	mycombo.pack(pady=10)
	mycombo.current(0)
	mycombo.bind("<<ComboboxSelected>>", get_municipality )    

	# Display List Frame (Treeview)
	global trv
	trv = ttk.Treeview(wrapper1, column=(1,2,3,4,5,6), show="headings", height="12", selectmode='browse')
	# trv.place(x=30, y=45)
	global vsb
	vsb = ttk.Scrollbar(wrapper1, orient="vertical", command=trv.yview)
	vsb.place(x=730, y=45, height=260)
	trv.configure(yscrollcommand=vsb.set)
	trv.pack()

	trv.heading(1, text="Record No")
	trv.column(1, minwidth=0, width=100, anchor=E, stretch=YES)
	trv.heading(2, text="Form No.")
	trv.column(2, minwidth=0, anchor=CENTER, width=100, stretch=NO)
	trv.heading(3, text=  "Municipality")
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
	# wrapper3.pack()

	my_listbox.pack(pady=5)
	for i in range(8):
		my_listbox.insert(END, f"This is an item {i}" )

	# Data User Frame
	# Input Fields
	lbl1 = Label(wrapper2, text="Record No")
	lbl1.grid(row=0, column=0, padx=5, pady=3)
	ent1 = Entry(wrapper2, textvariable=t1, state="disabled")
	ent1.grid(row=0, column=1, padx=5, pady=3)

	global ent1a
	lbl1a = Label(wrapper2, text="Poll Name")
	lbl1a.grid(row=1, column=3, padx=5, pady=3)
	ent1a = Entry(wrapper2, textvariable=t1a,  width=60, state="disabled")
	ent1a.grid(row=1, column=4, padx=5, pady=3)
	global ent1b
	lbl1b = Label(wrapper2, text="Poll Address")
	lbl1b.grid(row=2, column=3, padx=5, pady=3)
	ent1b = Entry(wrapper2, textvariable=t1b,  width=60, state="disabled")
	ent1b.grid(row=2, column=4, padx=5, pady=3)
	global ent1c
	lbl1c = Label(wrapper2, text="Poll Location")
	lbl1c.grid(row=3, column=3, padx=5, pady=3)
	ent1c = Entry(wrapper2, textvariable=t1c,  width=60, state="disabled")
	ent1c.grid(row=3, column=4, padx=5, pady=3)

	global ent2
	lbl2 = Label(wrapper2, text="Form No")
	lbl2.grid(row=1, column=0, padx=5, pady=3)
	ent2 = Entry(wrapper2, textvariable=t2, state="disabled")
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
	global up_btn1
	up_btn1 = Button(wrapper2, text="Update",  width=7, command=update_data, state=DISABLED)
	up_btn1.grid(row=7, column=1, sticky=W, padx=5, pady=3)
	up_btn1.bind("<Enter>", lambda event: btn_status(event, up_btn1))
	up_btn1.bind("<Leave>", lambda event: btn_status_out(event, up_btn1))

	global up_btn2
	up_btn2 = Button(wrapper2, text="Clear", width=7, command=search, state=DISABLED)
	up_btn2.grid(row=7, column=1, sticky=E, padx=5, pady=3)
	up_btn2.bind("<Enter>", lambda event: btn_status(event, up_btn2))
	up_btn2.bind("<Leave>", lambda event: btn_status_out(event, up_btn2))

	global up_btn3
	up_btn3 = Button(wrapper2, text="Update Poll Info", width=14, command=update_data, state=DISABLED)
	up_btn3.grid(row=7, column=4, sticky=W, pady=1)
	up_btn3.bind("<Enter>", lambda event: btn_status(event, up_btn3))
	up_btn3.bind("<Leave>", lambda event: btn_status_out(event, up_btn3))

	global up_btn4
	up_btn4 = Button(wrapper2, text="Return", width=14, command=get_file)
	up_btn4.grid(row=7, column=4, sticky=E, pady=1)	
	up_btn4.bind("<Enter>", lambda event: btn_status(event, up_btn4))
	up_btn4.bind("<Leave>", lambda event: btn_status_out(event, up_btn4))

	global up_btn5
	up_btn5 = Button(wrapper2, text="Update Forms", width=14, command=win_assign_formno, state=DISABLED)
	up_btn5.grid(row=7, column=4, pady=1)	
	up_btn5.bind("<Enter>", lambda event: btn_status(event, up_btn5))
	up_btn5.bind("<Leave>", lambda event: btn_status_out(event, up_btn5))
	
	#========================== Select a job number and display default records =======================
	if topLevel_update != None:
		mycombo.current(mycombo['values'].index(topLevel_update))
		search()
	else:	
		clear()

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

	button1 = Button(buttonframe, text='Exit', width=12, command=root.destroy)
	button1.pack( side = LEFT )
	button1.bind("<Enter>", lambda event: btn_status(event, button1))
	button1.bind("<Leave>", lambda event: btn_status_out(event, button1))

	button2 = Button(buttonframe, text='Submit', width=12, command=logged_in)
	button2.pack( side = LEFT)
	button2.bind("<Enter>", lambda event: btn_status(event, button2))
	button2.bind("<Leave>", lambda event: btn_status_out(event, button2))

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

# sys.exit(f"Quit App............. test")


#####################################################
# Create Tk Window
#####################################################
root = Tk()
root.title("Poll Books App!")
# root.iconbitmap('c:/guis/exe/codemy.ico')
root.resizable(False, False)
root.geometry("800x700")

# Gets the requested values of the height and widht.
windowWidth = root.winfo_reqwidth()
windowHeight = root.winfo_reqheight()
# Gets both half the screen width/height and window width/height
positionRight = int(root.winfo_screenwidth()/3 - windowWidth/2)
positionDown = int(root.winfo_screenheight()/3 - windowHeight/2)
# Positions the window in the center of the page.
root.geometry("+{}+{}".format(positionRight, positionDown))

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to log out?"):
        home()

root.protocol("WM_DELETE_WINDOW", on_closing)


def win_assign_formno():
	root.withdraw()	

	top = Toplevel()
	top.title('Top - window 2')
	top.geometry("900x700")
	top.resizable(False, False)
	top.geometry("+{}+{}".format(positionRight, positionDown))

	def on_closing():
	    if messagebox.askokcancel("Quit", "Do you want to quit?"):
	        top_close()

	top.protocol("WM_DELETE_WINDOW", on_closing)

    #=============================================#
	# Global Obj and Vas
    #=============================================#
	my_entries = []
	chkbox_state = {}

    #=============================================#
    # Toplevel Windowmethods
    #=============================================#    
	def top_close():
		root.deiconify()
		top.destroy()

	def save_sql(mwds, my_entries):
		data = _format_data(mwds, my_entries)   # return (form_value, municipality, ward, dist)
		set_columns = '''form_no = ? '''
		where_condition = '''municipality = ? and ward = ? and district = ?'''

		table_name = selected_table     # global var
		rows_updated=db.updateMultipleRecords(set_columns, where_condition, data, table_name)

		table_name += "_fm"
		rows_updated=db.updateMultipleRecords(set_columns, where_condition, data, table_name)
		display_mess(rows_updated, False)

		open_file(municipality)
		top.destroy()

	def _format_data(mwds, my_entries):
		data = []			
		for mwd, entry in zip(mwds, my_entries):
			fld1, fld2, municipality, ward, district, count, poll_name, poll_address, poll_location = mwd 
			form_value = entry.get()
			dist = str(district) if len(str(district))==2 else '0'+str(district)
			data.append((form_value, municipality, ward, dist))

		return data		

	def clear_fields(my_entries):
		for i, item in enumerate(my_entries):
			# print(item.get())
			item.config({"background": "white"}) 			
			item.delete(0, END)
			item.insert(END,'0')

	def show_ward(r1, r2, ward_no):
		# v[id, form_no, municipality, ward, district, dcount ]
		my_label = Label(top, width=10, text= f"Ward {ward_no}", fg="white", bg="grey")
		my_label.grid(row=r1, column=0, pady=1, padx=40)
		my_label = Label(top, width=10, text= f"Total: 0")
		my_label.grid(row=r2, column=0, pady=1, padx=40)

	def show_dist(r1, r2, x, item, eof=False):
		my_label = Label(top, width=10, text= f"District {item[4]}", fg="white", bg="grey")
		my_label.grid(row=r1, column=x, pady=1, padx=5)

		if eof:
			my_label.config(text="")
			return

		my_entry = Entry(top, width=10)     
		my_entry.grid(row=r2, column=x, pady=5, padx=5)
		# my_labels.append(my_label)		

		if item[1] >0:
			my_entry.config({"background": "#f5efd0"})          #DEDCDC

		my_entry.insert(0, f"{item[1]}")
		my_entries.append(my_entry)

	def show_districts(muni):
		header_text = selected_table.replace('_', ' ')
		text_mess = f"{header_text}\n\n{muni}"	

		header = Label(top, text=f"{text_mess}", font=("helvetica", 12), relief= RIDGE, bd=5)
		header.grid(row=1, column=3, columnspan=3, ipadx=20, ipady=5, pady=2)

		header1 = Label(top, text=f"", font=("helvetica", 12))
		header1.grid(row=2, column=0, columnspan=9)

		mwds = db.fetch_mwd(selected_table, muni) # This is global
		x = 1
		y1 = 5
		y2 = 6
		offset = 2
		# for row in mwds: print(row)
		
		ward_no = mwds[0][3] 				# id, form_no, municipality, ward, district, dcount            
		muni_name = mwds[0][2]				# (109, 20, 'HIGHTSTOWN', '', 1, 179)
		for i, item in enumerate(mwds):
			item = ['' if x is None else x for x in item]

			show_ward_no = True
			if i == 0:
				show_ward(y1, y2, item[3])          

			if ward_no != item[3]:
				ward_no = item[3]
				show_ward_no = False
				x=9

			if x == 9:
				x=1
				if show_ward_no == True and len(ward_no)>0:
					show_ward(y1, y2, item[3])
				y1 += offset
				y2 += offset

			show_dist(y1, y2, x, item)          	
			x += 1

		for col_pos in range( x, 9):
			show_dist(y1, y2, col_pos, item, True)

		# Buttons
		y2 += offset
		buttonframe = Frame(top)
		buttonframe.grid(row=y2, column=0, columnspan=9, pady=15)

		button1 = Button(buttonframe, text='Close', width=12, command=top_close)
		button1.pack( side = LEFT)
		button1.bind("<Enter>", lambda event: btn_status(event, button1))
		button1.bind("<Leave>", lambda event: btn_status_out(event, button1))

		button2 = Button(buttonframe, text='Clear Fields', width=12, command=lambda: clear_fields(my_entries))
		button2.pack( side = LEFT )
		button2.bind("<Enter>", lambda event: btn_status(event, button2))
		button2.bind("<Leave>", lambda event: btn_status_out(event, button2))

		button3 = Button(buttonframe, text='Save', width=12, command=lambda: save_sql(mwds, my_entries))
		button3.pack( side = LEFT )
		button3.bind("<Enter>", lambda event: btn_status(event, button3))
		button3.bind("<Leave>", lambda event: btn_status_out(event, button3))

		button4 = Button(buttonframe, text='Print-Export', width=12, command=lambda: _print_export(mwds, my_entries))
		button4.pack( side = LEFT )
		button4.bind("<Enter>", lambda event: btn_status(event, button4))
		button4.bind("<Leave>", lambda event: btn_status_out(event, button4))


    #=============================================#
    # Second Toplevel
    #=============================================#    
	def _print_export(mwds, my_entries):
		# root.withdraw()
		top.withdraw()
		top.attributes('-topmost', 'false')

		top2 = Toplevel()
		top2.title('window 3')
		top2.geometry("600x500")
		top2.resizable(False, False)
		top2.geometry("+{}+{}".format(positionRight, positionDown))
		# top2.update_idletasks()
		# top2.overrideredirect(True)

		def on_closing():
		    if messagebox.askokcancel("Quit", "Do you want to quit?"):
		        top2_close()

		top2.protocol("WM_DELETE_WINDOW", on_closing)


		muni_name = '' 
		data = _format_data(mwds, my_entries)   # return (form_value, municipality, ward, dist)
		data.sort(key = lambda x: x[0])  
		for f,m,w,d in data:
			muni_name = m
			key = f"Form-{f}"
			chkbox_state[key] = f

		# print(chkbox_state)
		# print('=================')		

		def top2_close():
			print('Close top2')
			top.deiconify()			
			top2.destroy()
			top.attributes('-topmost', 'true')

		def checkboxes():
			hdr_width = 15
			font_name = "Bahnschrift"
			header1 = Label(top2, text="", font=(font_name, 16), width=hdr_width)
			header1.grid(row=0, column=0)
			header2 = Label(top2, text="", font=(font_name, 16), width=hdr_width)
			header2.grid(row=0, column=1)
			header3 = Label(top2, text="", font=(font_name, 16), width=hdr_width)
			header3.grid(row=0, column=2)

			for i, machine in enumerate(chkbox_state):
				if i==0:
					header = Label(top2, text=f"{muni_name}", font=(font_name, 14),  relief= RIDGE, bd=5)
					header.grid(row=0, columnspan=3, ipadx=20, ipady=5)

				chkbox_state[machine] = Variable()
				chkbox = tk.Checkbutton(top2, text=machine, variable=chkbox_state[machine], font=("BahnschriftLight", 12), height=1, width=16, anchor="w")
				chkbox.grid(row=i+1, columnspan=3)
				chkbox.deselect()

			return int(i+2)

		# Show checkbox set:
		btn_row = checkboxes()
		spacer = Label(top2, text="").grid(row=btn_row, columnspan=3)
		btn_row +=1		
		buttonframe = Frame(top2) # highlightbackground="black", highlightthickness=1, bd=2
		buttonframe.grid(row=btn_row, columnspan=3)

		chk_btn1 = Button(buttonframe, text='Close', width=12, command=top2_close)
		chk_btn1.pack( side = LEFT)
		chk_btn1.bind("<Enter>", lambda event: btn_status(event, chk_btn1))
		chk_btn1.bind("<Leave>", lambda event: btn_status_out(event, chk_btn1))

		chk_btn2 = Button(buttonframe, text='Export CSV', width=12, command=lambda: _export(chkbox_state))
		chk_btn2.pack( side = LEFT )
		chk_btn2.bind("<Enter>", lambda event: btn_status(event, chk_btn2))
		chk_btn2.bind("<Leave>", lambda event: btn_status_out(event, chk_btn2))

		def _export(chkbox_state):
			for item in chkbox_state:
				print(f'{item}', chkbox_state[item].get())

	# Page Header 
	muni = mycombo.get()
	print(muni)
	show_districts(muni)
	top.mainloop()	

project_name = StringVar()
password = StringVar()
username = StringVar()
opts = StringVar()
chkStatus = IntVar()
chkbox_state = {}
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
poll_menu.add_command(label="Exit", command=root.destroy)
# poll_menu.add_command(label="Exit", command=root.destroy)

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