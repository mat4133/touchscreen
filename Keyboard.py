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
    lowerframe, upperframe, specialframe, numframe = Frame(frame, bg=style.lookup('TFrame', 'background')), Frame(
        frame, bg=style.lookup('TFrame', 'background')), Frame(frame, bg=style.lookup('TFrame', 'background')), Frame(
        frame, bg=style.lookup('TFrame', 'background'))

    # list of lowercase keys
    lower_btn_list = ['close', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
                      'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'caps', 'special', 'num', 'del', 'space']

    # list of uppercase keys
    upper_btn_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'E',
                      'F', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
                      'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'close', 'special', 'lower', 'del', 'space']

    # list of numbers
    numbers_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'close', 'special', 'caps', 'lower', 'del',
                    'space']

    # list of special characters
    special_character = ['/', "\ ", '.', ',', '-', '!', '&', '?', '+', '*', '^', '_', 'close', 'lower', 'caps', 'space',
                         'num', 'del']

    number_charrow = 5  # number of keys per row

    Framelist = [lowerframe, upperframe, numframe, specialframe]

    lowerframe.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)
    lowerframe.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)

    total_keyboard_list = [lower_btn_list, upper_btn_list, numbers_list,
                           special_character]  # list of lists of characters
    total_length = len(lower_btn_list) + len(upper_btn_list) + len(numbers_list) + len(
        special_character)  # total number of keys

    n, l = 0, 0  # key counter and keyboard counter
    btn = list(range(total_length))  # creates list of the length of the number of buttons

    for lists in total_keyboard_list:  # iterating through the different lists
        r, c, = 0, 0  # rows and columns for each keyboard
        for i in lists:  # iterating through the keys on each keyboard
            # Creating special buttons to change to other keyboards/close the keyboard
            if i == "caps":
                cmd = function_maker(frame_change, Framelist[l], upperframe)
            elif i == "special":
                cmd = function_maker(frame_change, Framelist[l], specialframe)
            elif i == "lower":
                cmd = function_maker(frame_change, Framelist[l], lowerframe)
            elif i == "close":
                cmd = function_maker(off, Framelist[l])
            elif i == "num":
                cmd = function_maker(frame_change, Framelist[l], numframe)
            elif i == "del":
                cmd = function_maker(delete)
            elif i == "space":
                cmd = function_maker(click, ' ', entry, text)
            elif i == "\ ":
                cmd = function_maker(click, i[:-1], entry, text)
            else:
                cmd = function_maker(click, i, entry, text)
            btn[n] = ttk.Button(Framelist[l], text=i, command=cmd)  # creating each button
            btn[n].grid(row=r, column=c)  # placing each button
            n += 1
            c += 1
            if c > number_charrow:
                c = 0
                r += 1
        l += 1

    return frame
