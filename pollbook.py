from tkinter import *
from random import randint
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
import os, time


from db import Database
db = Database('store.db')

root = Tk()
root.title("Flashcard App!")
# root.resizable(False, False)
root.geometry("900x400")

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


# global options


# Browse dir
def dir_browse():
	file_name =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("all files","*.*"),("jpeg files","*.jpg")))

	if file_name != "":
		new_frame.pack_forget()
		import_file(file_name)
	else:
		return

	print (file_name)

# Create Popup function
def import_file(file_name):
	f = os.path.basename(file_name)
	response = messagebox.askokcancel("Importing CSV File", f'Import File {f} ? ')
	if response == 1:
		csv_to_sqlite(file_name, f)
	else:
		new_file() # return	display results		

def csv_to_sqlite(file_name, f):
	hide_menu_frames()
	sqlite_import.pack(fill="both", expand=1)

	mess = f"Importing {f} ....."
	slqlite_flash = Label(sqlite_import, text=f"{mess}", font=("helvetica", 14))
	slqlite_flash.pack(pady=10)

	# ProgressBar
	global my_progress 
	my_progress = ttk.Progressbar(sqlite_import, orient=HORIZONTAL, length=300, mode="determinate")
	my_progress.pack(pady=20)

	table_exists = db.check_table_exists('pollbook_june2020')
	if table_exists == 1:
		print('table_exists')
	else:
		print('build schema and create table')
		table_name="test"
		gen = db.csv_to_array(file_name, table_name)
		next(gen)
		my_progress['value'] += 10
		time.sleep(1)

		next(gen)		
		my_progress['value'] += 10
		time.sleep(1)

		next(gen)
		my_progress['value'] += 10		
		time.sleep(1)

		next(gen)
		my_progress['value'] += 10				
	
		next(gen)		


# Create function 
def display_results(frame_obj, mess):
	# Put our random number onto the screen
	my_flash = Label(frame_obj, text=f"{mess}", font=("helvetica", 14))
	my_flash.pack(pady=10)

	# Get Project Name
	project_name_lbl = Label(frame_obj, text="Enter Project Nane", font=("helvetica", 12)).pack(pady=10)	
	# global project_name
	project_name = Entry(frame_obj, font=("helvetica", 12))
	project_name.pack(ipadx=100, ipady=6)

	# Buttons
	add_btn = Button(frame_obj, text='Get File', width=12, command=dir_browse).pack(pady=10)

	# Popup Boxes
	# showinfo, showwarning, showerror, askquestion, askokcancel, askyesno
	# pop_button = Button(root, text="Click To Pop Up!", command=import_file)
	# pop_button.pack(pady=20)


#Create our new_file function
def new_file():
	text_mess = "Create New Pollbook: Import New File."
	reset_run_frame(new_frame, text_mess)

#Create our open_file function
def open_file():
	text_mess = "Open Project: Select Job Folder"	
	reset_run_frame(open_frame, text_mess)

def reset_run_frame(frame_opt, text_mess):
	hide_menu_frames()
	frame_opt.pack(fill="both", expand=1)
	display_results(frame_opt, text_mess)


# Hide Frame Function
def hide_menu_frames():
	# Destroy the children widgets in each frame
	for widget in new_frame.winfo_children():
		widget.destroy()
	for widget in open_frame.winfo_children():
		widget.destroy()
	for widget in start_frame.winfo_children():
		widget.destroy()
	for widget in sqlite_import.winfo_children():
		widget.destroy()

	# Hide all frames
	new_frame.pack_forget()
	open_frame.pack_forget()
	start_frame.pack_forget()
	sqlite_import.pack_forget()

# Start Screen
def home():
	hide_menu_frames()
	start_frame.pack(fill="both", expand=1)
	start_label = Label(start_frame, text="Election Poll Books", font=("Helvetica", 18)).pack(pady=40)


#Define Main Menu
my_menu = Menu(root)
root.config(menu=my_menu)

# Create menu items
poll_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="File", menu=poll_menu)
poll_menu.add_command(label="Create Poll Book", command=lambda: new_file())
poll_menu.add_command(label="Open Poll Book", command=lambda: open_file())
poll_menu.add_separator()
poll_menu.add_command(label="Close Files", command=lambda: home())
poll_menu.add_separator()
poll_menu.add_command(label="Exit", command=root.quit)

# Create menu items
print_menu = Menu(my_menu)
my_menu.add_cascade(label="Print Files", menu=print_menu)
print_menu.add_command(label="New Poll Book", command=lambda: new_file())
print_menu.add_command(label="Open Poll Book", command=lambda: open_file())
print_menu.add_separator()
print_menu.add_command(label="Close Files", command=lambda: home())
print_menu.add_separator()
print_menu.add_command(label="Exit", command=root.quit)


# Create Math Frames
new_frame = Frame(root) #, highlightbackground="black", highlightthickness=1
open_frame = Frame(root)
start_frame = Frame(root)
sqlite_import =Frame(root)

# Show the start screen
home()

root.mainloop()