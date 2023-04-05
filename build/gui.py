# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer
import os.path
import openpyxl
from threading import Thread
from dataclasses import asdict, fields
from pathlib import Path
from tkinterdnd2.tkinterdnd2 import *
from quarterly_diff import compare_portfolios, CompanyInvestment

# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Frame, LEFT, Scrollbar, VERTICAL, Y, RIGHT, messagebox

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"D:\Projects\Python\quarterly_diff_automation\build\assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


prev_quarter_path = ""
curr_quarter_path = ""


def dict_to_excel(output_path, fieldnames, *args, force=True):
    # create a new workbook
    if force and os.path.exists(output_path):
        os.remove(output_path)
    wb = openpyxl.Workbook()
    for i, values_tuple in enumerate(args):
        sheet_name, values_iter = values_tuple
        ws = wb.create_sheet(title=sheet_name, index=i)

        # append headers
        ws.append(fieldnames)

        # append data
        # iterate `list` of `dict`
        for value in values_iter:
            # create a `generator` yield value `value`
            # use the fieldnames in desired order as `key`
            values = (value[k] for k in fieldnames)

            # append the `generator values`
            ws.append(values)

    wb.save(output_path)


def save_diff_result():
    new_investments, updated_investments, deprecated_investments = compare_portfolios(prev_quarter_path,
                                                                                      curr_quarter_path)
    dict_to_excel("results.xlsx", [field.name for field in fields(CompanyInvestment)],
                  ("new investments", (asdict(inv) for inv in new_investments.values())),
                  ("updated investments", (asdict(inv) for inv in updated_investments.values())),
                  ("deprecated investments", (asdict(inv) for inv in deprecated_investments.values())),
                  force=True
                  )
    messagebox.showinfo("", "Done writing :)")


window = TkinterDnD.Tk()

window.geometry("1440x626")

window.configure(bg="#FFFFFF")
canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=626,
    width=1440,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)

# Background
canvas.place(x=0, y=0)

# Prev quarter
canvas.create_rectangle(
    720.0,
    0.0,
    1440.0,
    626.0,
    fill="#7FE4D2",
    outline="")
canvas.create_rectangle(
    805.0,
    181.0,
    1358.0,
    512.0,
    fill="#FFFFFF",
    outline="")

# White rectangle area
prev = canvas.create_rectangle(
    839.0,
    118.0,
    1320.0,
    162.0,
    fill="#FFFFFF",
    outline="")

canvas.create_text(
    856.0,
    124.0,
    anchor="nw",
    text="Drag the current quarter file to the box:",
    fill="#000000",
    font=("Inter", 24 * -1)
)

canvas.create_rectangle(
    0.0,
    0.0,
    720.0,
    626.0,
    fill="#475855",
    outline="")

# current quarter
canvas.create_rectangle(
    85.0,
    181.0,
    638.0,
    512.0,
    fill="#FFFFFF",
    outline="")

canvas.create_rectangle(
    119.0,
    118.0,
    600.0,
    162.0,
    fill="#FFFFFF",
    outline="")

canvas.create_text(
    128.0,
    124.0,
    anchor="nw",
    text="Drag the previous quarter file to the box:",
    fill="#000000",
    font=("Inter", 24 * -1)
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))

button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: Thread(target=save_diff_result).start(),
    relief="flat"
)
button_1.place(
    x=667.0,
    y=512.0,
    width=107.0,
    height=107.0
)
# canvas.create_rectangle(
#     0.0,
#     625.0,
#     1440.0,
#     1024.0,
#     fill="#F4F4F4",
#     outline="")
#
# canvas.create_rectangle(
#     56.0,
#     673.0,
#     1389.0,
#     959.0,
#     fill="#FFFFFF",
#     outline="")

prev_quarter_frame = Frame(window)
prev_quarter_frame.place(x=85, y=181)
prev_quarter_textarea = Text(prev_quarter_frame, height=18, width=68)

curr_quarter_frame = Frame(window)
curr_quarter_frame.place(x=805, y=181)
curr_quarter_textarea = Text(curr_quarter_frame, height=18, width=68)


def load_prev_path(event):
    global prev_quarter_path
    prev_quarter_textarea.delete("1.0", "end")
    prev_quarter_textarea.insert("end", event.data)
    prev_quarter_path = event.data


def load_curr_path(event):
    global curr_quarter_path
    curr_quarter_textarea.delete("1.0", "end")
    curr_quarter_textarea.insert("end", event.data)
    curr_quarter_path = event.data


prev_quarter_textarea.pack(side=LEFT)
prev_quarter_textarea.drop_target_register(DND_FILES)
prev_quarter_textarea.dnd_bind('<<Drop>>', load_prev_path)

curr_quarter_textarea.pack(side=LEFT)
curr_quarter_textarea.drop_target_register(DND_FILES)
curr_quarter_textarea.dnd_bind('<<Drop>>', load_curr_path)

window.resizable(False, False)
window.mainloop()
