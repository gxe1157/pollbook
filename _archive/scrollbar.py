from tkinter import *

root = Tk()
root.title('Scrollbar')
root.geometry("400x600")

print('I am in scrollbar app1!')
#Scrollbar
my_frame = Frame(root)
my_scrollbar = Scrollbar(my_frame, orient=VERTICAL)

#list Box
# SINGLE, BROWSE, MULTIPLE, EXTENED
my_listbox = Listbox(my_frame, width=50, yscrollcommand=my_scrollbar.set)

#scrollbar configure
my_scrollbar.config(command=my_listbox.yview)
my_scrollbar.pack(side=RIGHT, fill=Y)
print('I am in scrollbar app2!')
my_frame.pack()
print('I am in scrollbar app3!')

my_listbox.pack(pady=5)
my_listbox.insert(END, "This is an item")
my_listbox.insert(END, "This is an item")
my_listbox.insert(END, "This is an item")
my_listbox.insert(END, "This is an item")
my_listbox.insert(END, "This is an item")
my_listbox.insert(END, "This is an item")
my_listbox.insert(END, "This is an item")
my_listbox.insert(END, "This is an item")
my_listbox.insert(END, "This is an item")
my_listbox.insert(END, "This is an item")

print('I am in scrollbar app4!')