#!/bin/python
import tkinter as tk
import pyshark
from tkinter import ttk
from datetime import datetime
import os
import subprocess

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
    
#Print packet summary for query
def print_packet_summary(pkt):
    packet_summary = "    " + str(pkt)[:120] + "\n"
    packet_summary_text.insert(tk.END, packet_summary)

#Capture Pyshark query
def capture_and_print_summary():
    packet_summary_text.delete("1.0", tk.END)
    interface = interface_combobox.get()
    capture = pyshark.LiveCapture(interface=interface, only_summaries=True)
    capture.sniff(packet_count=10)
    for packet in capture:
        print_packet_summary(packet)

#Defines save file contents and name
def generate_and_save_results():
    folder_name = "Wireshark Results"
    interface = interface_combobox.get()
    capture = pyshark.LiveCapture(interface=interface)
    current_time = datetime.now().strftime('%Y-%m-%d_%H-%M')
    filename = f"wireshark_results_{current_time}.csv"

    #Get the current working directory
    current_directory = os.getcwd()

    #Create the folder if it doesn't exist in current directory
    folder_path = os.path.join(current_directory, folder_name)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    #Construct the full file path
    filepath = os.path.join(folder_path, filename)

    try:
        #Create "Saving..." banner
        banner_label = tk.Label(window, text="Generating Results...", bg="blue", fg="white", font=("Arial", 16))
        banner_label.place(x=0, y=0, relwidth=1)
        window.update()

        with open(filepath, 'w') as f:
            for packet in capture.sniff_continuously(packet_count=50):
                f.write(str(packet))
        print(f"Full results saved to {filepath}")
        #Update banner to "Results Saved"
        banner_label.config(text="Results Saved", bg="green")
        #After 3 seconds, remove banner
        window.after(3000, banner_label.destroy)
    except Exception as e:
        print(f"Error saving results: {e}")
#Redirects to Wireshark Results page
def view_reports():
    print("wireshark_results button is clicked")
    subprocess.Popen(["python3","wireshark_results.py"])
    window.destroy()
   
   
#GUI setup
#Create window
window = tk.Tk()
window.title('Canopy.io')
window.geometry("1239x664")
window.configure(bg="#FFFFFF")

#Menu bar pop-up definitions
canvas1 = tk.Canvas(window, width=1239, height=664, bg = "#FFFFFF")
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
    bg = "#FFFFFF",
    height = 664,
    width = 1239,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

#Background image creation
canvas.place(x = 0, y = 0)
image_image_1 = tk.PhotoImage(file=r"wireshark_img.png")
image_1 = canvas.create_image(
    619.0,
    350.0,
    image=image_image_1
)

#Interface gui label
interface_label = tk.Label(window, text="Select Interface:")
interface_label.place(x=250, y=220)

#Interface drop-down menu
interface_combobox = ttk.Combobox(window, width=27, values=["eth0", "Wi-Fi", "en0", "en1", "en2"])
interface_combobox.place(x=250, y=255)

#Capture button - starts scan
capture_button = tk.Button(window, text="Start Capture", command=capture_and_print_summary)
capture_button.place(x=250, y=375)

#Save full results button
results_button = tk.Button(window, text="Save Full Results", command=generate_and_save_results)
results_button.place(x=365, y=375)

#Open new window button
new_window_button = tk.Button(window, text="View Past Results", command=view_reports)
new_window_button.place(x=500, y=375)

#Packet summary gui label
packet_summary_label = tk.Label(window, text="Packet Summaries:")
packet_summary_label.place(x=675, y=225)

#Results text window
packet_summary_text = tk.Text(window)
packet_summary_text.place(x=675, y=250, width=300, height=100)


#Runs the event in the window
window.mainloop()
