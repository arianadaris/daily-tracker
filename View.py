import tkinter as tk
from tkinter import ttk, font, messagebox
from tkcalendar import Calendar
from datetime import datetime
import urllib3

from Controller import *

# Disable urllib3 warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Get database attributes
attrs = get_attrs()

"""
open_calendar()
Open Tkinter Calendar widget
"""
def open_calendar():
    def on_date_selected():
        selected_date = cal.get_date()
        datetime_obj = datetime.strptime(selected_date, '%Y-%m-%d')
        
        # Update date label in interface
        date = datetime_obj.strftime('%B %d, %Y')
        dayLabel.config(text=date)

        top.destroy() # close window after date updates

    # Create calendar
    top = tk.Toplevel()
    cal = Calendar(top, selectmode="day", date_pattern="yyyy-mm-dd")
    cal.grid(row=0, column=0, padx=10, pady=10)

    # Create select date button
    select_button = tk.Button(top, text="Select Date", command=on_date_selected)
    select_button.grid(row=1, column=0, pady=10)

"""
Main Application Setup
"""
# Root dimensions and customization
root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_width = 800
window_height = 575
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2
root.geometry(f'{window_width}x{window_height}+{x}+{y}')
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)

# Initialize fonts
normal = font.Font(family="Arial", size=14)
bold = font.Font(family="Arial", size=20, weight="bold")

datetime_obj = datetime.now()
date = datetime_obj.strftime('%B %d, %Y')
if(date[date.index('0') + 1].isdigit() and date[date.index('0') - 1] != '2'):
    date = date.replace('0', '', 1)
root.title(f'Daily Tracker')

# Add day label
dayLabel = tk.Label(root, text=date, font=bold)
dayLabel.grid(row=0, column=0, padx=15, pady=10, sticky=tk.W, columnspan=2)

# Create open calendar button
open_button = tk.Button(root, text="Open Calendar", command=open_calendar)
open_button.grid(row=0, column=1, sticky=tk.W, pady=10)

# Create variables for each attribute's element
widgets = []

# Create widgets for each attribute
for i, attr in enumerate(attrs):
    # Create label element
    label = tk.Label(root, text=attr["name"], font=normal)
    label.grid(row=i+1, column=0, padx=15, pady=5, sticky=tk.W)

    if attr["type"] == "select":
        # Define option variables
        selected_option = tk.StringVar()
        options = attr["select"]

        # Add None value to options for Gym Day field
        if attr["name"] == "Gym Day": options.append('None')
        if "None" in options: selected_option.set("None")
        else: selected_option.set(options[0])

        # Create OptionMenu widget
        option_menu = ttk.OptionMenu(root, selected_option, selected_option.get(), *options)
        option_menu.grid(row=i+1, column=1, padx=15, pady=5, sticky=tk.W)
        widgets.append(selected_option)

    elif attr["type"] == "checkbox":
        # Create variable to store checkbox state
        checkbox_state = tk.BooleanVar()

        # Create Checkbutton widget
        checkbox = tk.Checkbutton(root, variable=checkbox_state)
        checkbox.grid(row=i+1, column=1, padx=15, pady=5, sticky=tk.W)
        widgets.append(checkbox_state)

    else:
        entry = tk.Entry()
        entry.grid(row=i+1, column=1, padx=15, pady=5, sticky=tk.W)
        widgets.append(entry)


# Create the Update Day button
def on_button_click():
    vals = []

    date = dayLabel.cget('text')
    datetime_obj = datetime.strptime(date, '%B %d, %Y')

    for widget in widgets:
        vals.append(widget.get())

    # Create dictionaries for each attribute
    inputs = []
    for i, attr in enumerate(attrs):
        val = vals[i]
        if attr["type"] == "number":
            if val == '': pass
            else:
                inputs.append({
                    attr["name"]: {
                        attr["type"]: int(val)
                    }
                })
        elif attr["type"] == "select":
            if val == 'None': pass
            else:
                inputs.append({
                    attr["name"]: {
                        "select": {
                            "name": val
                        }
                    }
                })
        elif attr["type"] == "rich_text":
            if val == '': pass
            else:
                inputs.append({
                    attr["name"]: {
                        'rich_text': [{
                            "text": {
                                "content": val
                            }
                        }]
                    }
                })
        else:
            inputs.append({
                attr["name"]: {
                    attr["type"]: val
                }
            })

    # Create page for this day
    if not check_page_exists(datetime_obj):
        page_id = create_page(datetime_obj)
    else:
        page_id = get_page_id(datetime_obj)

    # Update the page
    res = update_page(page_id, inputs)

    if res.status_code == 200:
        messagebox.showinfo('Success', 'Page updated successfully.')
    else:
        messagebox.showerror('Error', f'Failed to update the page. Error: {res.status_code}')

button_text = tk.StringVar()
button_text.set("Update day")

button = ttk.Button(textvariable=button_text, command=on_button_click)
button.grid(row=len(attrs)+1, column=0, padx=15, pady=10, columnspan=2)


"""
Initialize Application
"""
root.mainloop()