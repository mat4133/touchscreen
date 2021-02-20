from tkinter import *
from tkinter import ttk


# function to create other functions

def function_maker(function, *part_args):  # takes in the function to make more of + values needed in that function
    def wraps(*extra_args):
        argument = list(part_args)
        argument.extend(extra_args)
        return function(*argument)

    return wraps


# function to display which button was clicked
def click(btn, entry, text):
    current_text = entry.get()
    new_text = current_text + btn
    text.set(new_text)


def delete(entry, text):
    current_text = entry.get()
    text.set(current_text[:-1])


# function to switch between keyboard frames
def frame_change(currentframe, newframe):
    currentframe.grid_forget()
    newframe.grid(column=0, row=0, sticky='nesw')


# function to turn on keyboard
def keyboard_on(lowerframe, *args):
    lowerframe.grid(column=0, row=0, sticky='nesw')


# frame for each keyboard
def create_keyboard(frame, entry, text, style, off):
    lowerframe, upperframe, specialframe = Frame(frame, bg=style.lookup('TFrame', 'background')), Frame(
        frame, bg=style.lookup('TFrame', 'background')), Frame(frame, bg=style.lookup('TFrame', 'background'))

    # list of lowercase keys
    lower_btn_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'close', '⬅', 'q', 'w', 'e', 'r', 't', 'y',
                      'u', 'i', 'o', 'p', 'caps', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'z', 'special',
                      'x', 'c', 'v', 'b', 'n', 'm', 'space']

    # list of uppercase keys
    upper_btn_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'close', '⬅', 'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O',
                      'P', 'lower', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L',
                      'Z', 'special', 'X', 'C', 'V', 'B', 'N', 'M', 'space']

    # list of special characters
    special_character = ['close', '/', "\ ", '.', ',', '-', '!', '&', '?', '*', '^',
                         '⬅', '_', '[', ']', '{', '}', '@', '~', '`', '#', '(', 'caps', ')', '=', '+', '|', '<', '>', ':', ';', '"', "'",
                          'lower', '$', 'space']

    number_charrow = 12  # number of keys per row

    Framelist = [lowerframe, upperframe, specialframe]

    lowerframe.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)
    lowerframe.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12), weight=1)

    total_keyboard_list = [lower_btn_list, upper_btn_list,
                           special_character]  # list of lists of characters
    total_length = len(lower_btn_list) + len(upper_btn_list) + len(
        special_character)  # total number of keys

    n, l = 0, 0  # key counter and keyboard counter
    btn = list(range(total_length))  # creates list of the length of the number of buttons

    for lists in total_keyboard_list:  # iterating through the different lists
        r, c, = 0, 0  # rows and columns for each keyboard
        for i in lists:  # iterating through the keys on each keyboard
            # Creating special buttons to change to other keyboards/close the keyboard
            cspan = 1
            c_extra = 0
            r_extra = 0
            if i == "caps":
                cspan = 2
                c_extra = 1
                cmd = function_maker(frame_change, Framelist[l], upperframe)
            elif i == "special":
                cmd = function_maker(frame_change, Framelist[l], specialframe)
                cspan = 3
                c_extra = 2
            elif i == "lower":
                cspan =2
                c_extra = 1
                cmd = function_maker(frame_change, Framelist[l], lowerframe)
            elif i == "close":
                cspan = 2
                c_extra = 1
                cmd = function_maker(off, Framelist[l])
            elif i == "⬅":
                cspan = 2
                c_extra = 1
                cmd = function_maker(delete, entry, text)
            elif i == "space":
                cmd = function_maker(click, ' ', entry, text)
                c_extra = 2
                cspan = 3
            elif i == "\ ":
                cmd = function_maker(click, i[:-1], entry, text)
            else:
                cmd = function_maker(click, i, entry, text)
            btn[n] = ttk.Button(Framelist[l], text=i, command=cmd, width=500/number_charrow)  # creating each button
            btn[n].grid(row=r, column=c, columnspan=cspan, sticky='nesw')  # placing each button
            n += 1
            c += (1+c_extra)
            if c >= number_charrow:
                c = 0
                r += 1
        l += 1
    return frame
