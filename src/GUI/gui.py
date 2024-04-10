from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import tkfilebrowser
from table import *
import os
import subprocess
import numpy as np
import json


HOME_DIR = os.getcwd()
IMAGES_DIR = []
BULK_DIR = []
json_dict = {}
conditions_list = []
condition_names = [""]
all_conditions = []


# toggle_checkbox shows folder selection widgets if checkbox is checked
def toggle_checkbox_imaging():
    if var.get():
        folder_select_lbl.pack(side=TOP, anchor = "w", padx = 10, before = bulk_checkbox)
        folder_select_lbl_btn.pack(side=TOP, anchor = "w", padx = 10, before = bulk_checkbox)
        dir_entry.pack(side=TOP, anchor = "w", padx = 10, before = bulk_checkbox)
        good_data_checkbox.pack(side=TOP, anchor = "w", padx = 10, before = bulk_checkbox)
    else:
        folder_select_lbl.pack_forget()
        folder_select_lbl_btn.pack_forget()
        dir_entry.pack_forget()
        good_data_checkbox.pack_forget()

def toggle_checkbox_bulk():
    if bulk_var.get():
        bulk_folder_select_lbl.pack(side=TOP, anchor = "w", padx = 10, before = sample_name_label)
        bulk_folder_select_lbl_btn.pack(side=TOP, anchor = "w", padx = 10, before = sample_name_label)
        bulk_dir_entry.pack(side=TOP, anchor = "w", padx = 10, before = sample_name_label)
    else:
        bulk_folder_select_lbl.pack_forget()
        bulk_folder_select_lbl_btn.pack_forget()
        bulk_dir_entry.pack_forget()

def send_directory():
	send_dir_entry.insert(0, string=filedialog.askdirectory())

def images_directory():
    dir_entry.delete(0, "end")
    IMAGES_DIR.append(tkfilebrowser.askopendirnames())
    for i in range(len(IMAGES_DIR)):
        if i == 0:
            dir_entry.insert(i, string=IMAGES_DIR[i][0]+",")
        else:
            dir_entry.insert(len(dir_entry.get())+1, string=IMAGES_DIR[i][0]+",")
    return IMAGES_DIR

def bulk_directory():
    bulk_dir_entry.delete(0, "end")
    BULK_DIR.append(filedialog.askopenfilenames())
    for i in range(len(BULK_DIR)):
        if i == 0:
            bulk_dir_entry.insert(i, string=BULK_DIR[i][0]+",")
        else:
            bulk_dir_entry.insert(len(bulk_dir_entry.get())+1, string=BULK_DIR[i][0]+",")
    return BULK_DIR

# read_sample_name grabs the entry from the sample_name_entry widget
# if the enter_cells widget is inactive (widget to save cells in table)
# then it re-enables the widget, also re-enables the plate_count_option_menu widget
def read_sample_name():
    condition_names.clear()
    sample_name = sample_name_entry.get()
    sample_prompt_text.config(text = f"Enter cells for sample: {sample_name}")
    enter_cells.configure(state="active")
    plate_count_option_menu.configure(state="active")
    # for i in range(0, num_plots):
        # plot_normalization_option_menus[i]['menu'].add_command(label=sample_name, command=ttk._setit(plot_normalization_selections[i], sample_name))

# save_sample_cells() saves the current list of sample_cells to
# the conditions_list dictionary, then clears the selected cells and the table
def save_sample_cells():
    conditions = {}
    sample_name = sample_name_entry.get()
    conditions[sample_name] = sorted(list(sample_cells))
    conditions_list.append(conditions)
    print(conditions_list)
    if plate_cells_var.get() < plate_count_var.get():
        plate_cells_var.set(plate_cells_var.get() + 1)
    else:
        enter_cells.configure(state="disabled")
    sample_cells.clear()
    table.clear_color()

# disable_plate_count disables the plate_count_option_menu widget, prevents user from editing it after hitting "Enter"
def disable_plate_count():
    plate_count_option_menu.configure(state="disabled")
    plate_cells_var.set(1)


def plate_count_select(value):
    plate_count_var.set(value)
    
def save_plot_number():
    plot_number = plot_number_entry.get("1.0", "end-1c")
    with open("temp_plot_num.txt", "w") as fw:
        fw.write(plot_number)

def create_new_window():
    json_dict["notes"] = notes_entry.get("1.0", "end-1c")
    json_dict["acquisition_frequency"] = int(acquisition_freq.get("1.0", "end-1c"))
    json_dict["images_directory"] = [s[0].replace("\\", "/") for s in IMAGES_DIR]
    json_dict["bulk_data"] = [s[0] for s in BULK_DIR]
    json_dict["conditions"] = conditions_list
    json_dict["acquisition_frequency"] = 2
    if good_data_var.get():
        good_data_directory = "B:/Good imaging data"
    else:
        good_data_directory = ""
    json_dict["good_data_directory"] = good_data_directory
    json_dict["experiment_directory"] = send_dir_entry.get()
    with open(HOME_DIR + "/temp_config.json", "w") as file:
        json.dump(json_dict, file, indent = 4)
    
    for cond in conditions_list:
        all_conditions.append(next(iter(cond.keys())))
    print(all_conditions)
    with open("temp_conditions.txt", "w") as fw:
        for cond in all_conditions:
            fw.write(cond)
            fw.write("\n")
    os.system('export LANG="en_US.UTF-8"; python3 plotoptions.py')
    

if __name__ == "__main__":
    root = Tk()
    root.title("Scanner")
    root.geometry("1000x800")
    frm = ttk.Frame(root)
    frm.grid()
    frm.pack(padx=2, pady=0)

    # EXPERIMENT NOTES ENTRY
    notes_lbl = ttk.Label(root, text = "Experiment Notes")
    notes_lbl.pack(side=TOP, anchor = "w", padx = 10)

    notes_entry = Text(root, width = 35, height = 4)
    notes_entry.pack(side=TOP, anchor = "w", padx = 10)

    # PLOT NUMBERS  
    plot_number_frm = ttk.Frame(root)
    plot_number_frm.pack(side=TOP, anchor="w", padx=5, pady=5)
    plot_number_lbl = ttk.Label(plot_number_frm, text = "Enter number of plots")
    plot_number_lbl.pack(side=LEFT, anchor = "w", padx = 10)
    plot_number_entry = Text(plot_number_frm, width = 5, height = 1)
    plot_number_entry.pack(side=LEFT, anchor = "w", padx = 10)
    plot_number_btn = ttk.Button(plot_number_frm, text = "Enter", command = save_plot_number)
    plot_number_btn.pack(side=LEFT, anchor = "w", padx = 10)
    

    

    # ACQUISITION FREQUENCY
    acquisition_lbl = ttk.Label(root, text = "Acquisition Frequency (#/hr)")
    acquisition_lbl.pack(side=TOP, anchor = "w", padx = 10)

    acquisition_freq = Text(root, width = 35, height = 1)
    acquisition_freq.pack(side=TOP, anchor = "w", padx = 10)

    # PLATE COUNTS
    plate_count_options = [1,2,3]
    plate_count_var = ttk.IntVar()
    plate_count_var.set(plate_count_options[0])
    plate_count_frame = ttk.Frame(root)
    plate_count_frame.pack(side=TOP, anchor = "w", padx=5)
    plate_count_label = ttk.Label(plate_count_frame, text = "Enter number of plates:")
    plate_count_label.pack(side=LEFT, anchor = "w", padx = 5, pady = 3)
    plate_count_option_menu = ttk.OptionMenu(plate_count_frame, plate_count_var, *plate_count_options, command = plate_count_select)
    plate_count_option_menu.pack(side=LEFT, anchor = "w", padx = 5, pady = 3)
    plate_count_enter = ttk.Button(plate_count_frame, text="Enter", command = disable_plate_count)
    plate_count_enter.pack(side=LEFT, anchor = "w", padx = 5, pady = 3)

    # CHOOSE FOLDER TO SEND DATA
    send_folder_select_lbl = ttk.Label(root, text="Choose folder to store this experiment")
    send_folder_select_lbl_btn = ttk.Button(root, text="Choose folder to store this experiment", command=send_directory)
    send_dir_entry = ttk.Entry(root, width = 35)
    send_folder_select_lbl.pack(side=TOP, anchor = "w", padx = 10)
    send_folder_select_lbl_btn.pack(side=TOP, anchor = "w", padx = 10)
    send_dir_entry.pack(side=TOP, anchor = "w", padx = 10)

    # CHECKBOX FOR IMAGES DIRECTORY
    var = ttk.IntVar()
    checkbox = ttk.Checkbutton(root, text="Imaging Included (y/n)", variable=var, command = toggle_checkbox_imaging)
    checkbox.pack(side=TOP, anchor = "w", padx = 10)

    # FOLDER SELECTION
    images_dirs = []
    folder_select_lbl = ttk.Label(root, text="Choose folder where images are located")
    folder_select_lbl_btn = ttk.Button(root, text="Choose folder where images are located", command=images_directory)
    dir_entry = ttk.Entry(root, width = 35)

    # CHECKBOX FOR GOOD DATA
    good_data_var = ttk.IntVar()
    good_data_checkbox = ttk.Checkbutton(root, text="Good data (y/n)", variable=good_data_var)

    # BULK DATA SELECTION
    bulk_var = ttk.IntVar()
    bulk_checkbox = ttk.Checkbutton(root, text="Bulk Data Included (y/n)", variable=bulk_var, command = toggle_checkbox_bulk)
    bulk_checkbox.pack(side=TOP, anchor = "w", padx = 10)
    bulk_folder_select_lbl = ttk.Label(root, text="Choose file for bulk data")
    bulk_folder_select_lbl_btn = ttk.Button(root, text="Choose file for bulk data", command=bulk_directory)
    bulk_dir_entry = ttk.Entry(root, width = 35)

    # SAMPLE NAME
    sample_name_label = ttk.Label(root, text = "Sample Name")
    sample_name_label.pack(side=TOP, anchor = "w", padx = 10)
    sample_name_entry = ttk.Entry(root, width = 35)
    sample_name_entry.pack(side=TOP, anchor = "w", padx = 10)

    enter_sample_button = ttk.Button(root, text="Enter", command=read_sample_name)
    enter_sample_button.pack(side=TOP, anchor = "w", padx = 10, pady = 3)

    sample_prompt_text = ttk.Label(root, text = f"Enter cells for sample:")
    sample_prompt_text.pack(side=TOP, anchor = "w", padx = 10, pady = 3)


    plate_cells_frame = ttk.Frame(root)
    plate_cells_frame.pack(side=TOP, anchor = "w", padx=5)

    plate_cells_label = ttk.Label(plate_cells_frame, text = f"Enter cells for plate: ")
    plate_cells_label.pack(side=LEFT, anchor = "w", padx = 10, pady = 3)

    plate_cells_var = ttk.IntVar()
    plate_cells_var.set(1)
    plate_cells_entry = ttk.Entry(plate_cells_frame, textvariable=plate_cells_var)
    plate_cells_entry.pack(side=LEFT,anchor="w", padx=10,pady=5)

    # TABLE
    table = Table(root, rows=8, columns=12)
    table.pack(expand=True, fill = "both", side=TOP, anchor="w",padx = 10)

    enter_cells_frame = ttk.Frame(root)
    enter_cells_frame.pack(side=TOP, after=table, anchor = "w", padx=5)

    enter_cells = ttk.Button(enter_cells_frame, text="Enter", command=save_sample_cells)
    enter_cells.pack(side=LEFT, anchor = "w",pady=5)    
    
    
    # NEXT
    next_btn = ttk.Button(root, text="Next", command=create_new_window)
    next_btn.pack(side=TOP, anchor = "e", padx = 10)
    root.mainloop()
