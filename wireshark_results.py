#!/bin/python
import os
import tkinter as tk
import subprocess
from tkinter import ttk
from tkinter import filedialog

#Defining scan_button action
def scan_button():
    print("scan button is clicked")
    subprocess.Popen(["python3", "scan.py"])
    window.destroy()

#Defining attack_button action
def attack_button():
    print("attack button is clicked")
    subprocess.Popen(["python3", "msfpygui.py"])
    window.destroy()

#Defining report_button action
def report_button():
    print("report button is clicked")
    subprocess.Popen(["python3", "reports_page.py"])
    window.destroy()

#Defining the home_button action
def home_button():
    print("home button is clicked")
    subprocess.Popen(["python3", "home.py"])
    window.destroy()

#Determine the script directory
script_directory = os.path.dirname(os.path.abspath(__file__))

#Define a relative path for data storage
data_directory = os.path.join(script_directory, "Wireshark Results")

#Get a list of all .csv files in the data directory
result_files = [f for f in os.listdir(data_directory) if f.endswith('.csv')]

#Create window
window = tk.Tk()
window.title('Canopy.io')
window.geometry("1239x664")
window.configure(bg="#FFFFFF")

#Menu bar pop-up definitions
canvas1 = tk.Canvas(window, width=1239, height=664, bg="#FFFFFF")
menubar = tk.Menu(window)
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label='Home', command=home_button)
filemenu.add_command(label='Scan', command=scan_button)
filemenu.add_command(label='Attack', command=attack_button)
filemenu.add_command(label='Reports', command=report_button)
menubar.add_cascade(label='Canopy.IO Menu', menu=filemenu)
window.config(menu=menubar)

canvas = tk.Canvas(
    window,
    bg="#FFFFFF",
    height=664,
    width=1239,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)

#Background image creation
canvas.place(x=0, y=0)
image_image_1 = tk.PhotoImage(file=r"wireshark_img.png")
image_1 = canvas.create_image(
    619.0,
    350.0,
    image=image_image_1
)

#Create the combobox with the sorted list of .csv files and set the default selection to the first item in the list
past_results_combobox = ttk.Combobox(window, width=27, values=result_files, state="readonly")
past_results_combobox.current(0)
past_results_combobox.place(x=100, y=255)

#Text box for displaying file contents
text_box = tk.Text(window, width=72, height=25)
text_box.place(x=500, y=220)

#Scrollbar for the text box
scrollbar = tk.Scrollbar(window, command=text_box.yview)
scrollbar.place(x=1015, y=220, height=333)
text_box.config(yscrollcommand=scrollbar.set)

def on_select(event=None):
    #Clear the text box
    text_box.delete('1.0', tk.END)

    #Get the selected file name
    selected_file = past_results_combobox.get()

    #Read the contents of the file
    file_path = os.path.join(data_directory, selected_file)
    with open(file_path, 'r') as f:
        file_contents = f.read()

    #Insert the file contents into the text box
    text_box.insert(tk.END, file_contents)

#Set the default selection to the first item in the list of .csv files
past_results_combobox.bind('<<ComboboxSelected>>', on_select)

#Call the on_select function with the default selection
on_select()

def save_file():
    #Get the selected file name
    selected_file = past_results_combobox.get()

    #Get the contents of the selected file
    file_path = os.path.join(data_directory, selected_file)
    with open(file_path, 'r') as f:
        file_contents = f.read()

    #Open a file dialog to select where to save the file
    file_path = filedialog.asksaveasfilename(defaultextension='.csv')

    #Save the file
    with open(file_path, 'w') as f:
        f.write(file_contents)

save_button = tk.Button(window, text="Save File to Device", command=save_file)
save_button.place(x=100, y=295)

#Runs the event in the window
window.mainloop()

