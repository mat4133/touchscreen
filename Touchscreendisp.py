from tkinter import *
from tkinter import messagebox, _setit, ttk
from PIL import Image, ImageTk
from ttkthemes import ThemedStyle
from Keyboard import create_keyboard, keyboard_on, function_maker
import Wifi_file as wf
import VideoSetting as vs
import pickle
import os
import threading
import cv2

# See README for information about this

starting = 0
audio_connection = 0
video_connection = 0

class Customise_button(ttk.Button):
    def __init__(self, parent, text, command):
        self.parent = parent
        if type(text).__name__ == 'PhotoImage':
            self.name = 'arrow'
            super().__init__(stream, image=text, command=command)
        else:
            self.name = text
            super().__init__(stream, text=text, command=command)

    def __repr__(self):
        return (self.name)


class Customise_window():
    def __init__(self, name):
        self.name = name
        self.button_list = []

    def add_button(self, button):
        if button.parent == self.name:
            self.button_list.append(button)

    def create_window(self):
        if len(self.button_list) == 1:
            self.button_list[0].grid(column=0, row=3, columnspan=2)
        if len(self.button_list) == 2:
            self.button_list[0].grid(column=0, row=3, columnspan=2)
            self.button_list[1].grid(column=2, row=1, rowspan=2)
        if len(self.button_list) == 4:
            self.button_list[0].grid(column=0, row=3)
            self.button_list[1].grid(column=1, row=3)
            self.button_list[2].grid(column=2, row=1)
            self.button_list[3].grid(column=2, row=2)

    def close_window(self):
        for i in self.button_list:
            i.grid_forget()

    def __repr__(self):
        return self.button_list.__repr__()

# Functions for resetting back to the default settings
def set_defaults():
    settings_file = open('settings_file', 'wb')
    settings_dic = {'bit_rate': 30, 'frame_rate': 30, 'audioless': False, 'audio_delay': 200}
    pickle.dump(settings_dic, settings_file)
    settings_file.close()


# Function for reading the settings from settings_file
def inital_settings():
    global frame_rate, delay_value, chk_state, bit_rate
    previous_settings = open('settings_file', 'rb')
    saved_values = pickle.load(previous_settings)
    chk_state = IntVar(value=saved_values['audioless'])
    bit_rate = DoubleVar(value=saved_values['bit_rate'])
    frame_rate = DoubleVar(value=saved_values['frame_rate'])
    delay_value = DoubleVar(value=saved_values['audio_delay'])
    previous_settings.close()


# Function for updating file every 5 seconds with new settings
def update_settings(*args):
    global frame_rate, delay_value, chk_state, bit_rate
    settings_dic = {'bit_rate': bit_rate.get(), 'frame_rate': frame_rate.get(), 'audioless': chk_state.get(),
                    'audio_delay': delay_value.get()}
    settings_file = open('settings_file', 'wb')
    pickle.dump(settings_dic, settings_file)
    settings_file.close()
    threading.Timer(5, update_settings).start()


app = Tk()

app.title('Streaming on a prayer')

app.geometry('480x320')  # swap to fullscreen when using touchscreen
# app.attributes('-fullscreen', True)

# initializing style
style = ThemedStyle(app)
style.set_theme("equilux")

# background colour from theme equilux
bg = style.lookup('TFrame', 'background')
fg = style.lookup('TFrame', 'foreground')
app.configure(bg=style.lookup('TFrame', 'background'))

# app.attributes('-fullscreen',True)

# Setting up windows for application (main menu, settings, stream)
style.configure('TNotebook.Tab', width=app.winfo_screenwidth())
style.configure("Tab", focuscolor=style.configure(".")["background"])
style.configure('TNotebook.Tab', anchor=CENTER, activebackground='#00ff00')
note = ttk.Notebook(app)
note.pack()

stream = ttk.Frame(note)
settings = ttk.Frame(note)
wifi_login = ttk.Frame(note)
tutorial = ttk.Frame(note)

note.add(stream, text="STREAM")
note.add(settings, text="SETTINGS")
note.add(wifi_login, text="WIFI")
note.add(tutorial, text="TUTORIAL")

settings2 = ttk.Frame(app)

# Settings display------------------------------------------------------------------------------------------------------

# Configuring grid layout for settings window
settings.grid_columnconfigure(0, weight=2)
settings.grid_columnconfigure((1, 2), weight=1)
settings.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8), weight=1)


# Wifi login and code ----------------------------------------------------------------------

def password_space_wifi(*args):
    connect_btn.grid_forget()
    wifi_label.grid_forget()
    wifi_connected.grid_forget()
    keyboard_frame3.grid(column=0, row=4, columnspan=2, rowspan=2)
    keyboard_on(keyboard_frame3.children['!frame'])


def password_keyboard_off(current_frame):
    current_frame.grid_forget()
    wifi_label.grid(column=0, row=0)
    wifi_connected.grid(column=1, row=0)
    search_label.grid(column=0, row=1)
    search_networks.grid(column=1, row=1)
    password_entr.grid(column=1, row=2)
    password_lbl.grid(column=0, row=2)
    connect_btn.grid(column=1, row=3)
    keyboard_frame3.grid_forget()
    # username_entr.grid(column=1, row=2)
    # username_lbl.grid(column=0, row=2)


wifi_login.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)
wifi_login.grid_columnconfigure((0, 1), weight=1)

# Code for Wifi connection
wifi_label = ttk.Label(wifi_login, text='WiFi')
wifi_label.grid(column=0, row=0)
wifi_connected = ttk.Label(wifi_login, text='Unconnected')
wifi_connected.grid(column=1, row=0)

search_label = ttk.Label(wifi_login, text='Nearby Networks')
search_label.grid(column=0, row=1)

def password_filler(*args):
    saved = 0
    for networks in wf.saved_networks:
        if networks.SSID == args[0]:
            password_text.set(networks.password)
            saved = 1
    for networks in search_list:
        if networks.SSID == args[0]:
            candidate_network = networks
    if saved == 0:
        password_text.set('')

candidate_network = 'none'

def connect():
    candidate_network.password = password_text.get()
    wf.save_conf(candidate_network)
    wf.dump()

#search_list = wf.scan()
search_list = ['list of networks', 'network 1', 'network 2']

'''
option_menu_list = []
for networks in search_list:
    option_menu_list.append(networks.SSID)
'''

current_network = StringVar(value='network 3')
search_networks = ttk.OptionMenu(wifi_login, current_network, *search_list, command=password_filler)
search_networks.grid(column=1, row=1)


password_lbl = ttk.Label(wifi_login, text='PASSWORD:')
password_lbl.grid(column=0, row=2)

password_text = StringVar()
password_entr = ttk.Entry(wifi_login, textvariable=password_text)
password_entr.grid(column=1, row=2)
password_entr.bind("<Button>", password_space_wifi)

connect_btn = ttk.Button(wifi_login, text='CONNECT/SAVE', command=connect)
connect_btn.grid(columnspan=2, row=3)

keyboard_frame3 = Frame(wifi_login)
keyboard_frame3.configure(bg=style.lookup('TFrame', 'background'))
keyboard_frame3.grid(column=0, row=4, columnspan=2, rowspan=2)
keyboard_frame3.rowconfigure(0, weight=1)
keyboard_frame3.columnconfigure(0, weight=1)

keyboard_frame3 = create_keyboard(keyboard_frame3, password_entr, password_text, style, password_keyboard_off)

# Settings frame--------------------------------------------------------------------------------------

# importing default settings -------------------------------------------------------------------------

if starting == 0:
    inital_settings()
    update_settings()
    starting = 1

# code for saving and importing streams

file_name = 'stream_codes'

# reading the stream codes from memory
stored_codes2 = open(file_name, 'rb')
code_list = pickle.load(stored_codes2)
stored_codes2.close()


# code for entering a new key
def enter_code():
    global code_list
    input_code = stream_code.get()

    # checks if this is the first key entered and if so deletes the '' that was in it's place
    if code_list[0] == '':
        code_list.remove('')
        existing_codes['menu'].delete(0)

    code_list.insert(0, input_code)

    # adds the new key to a file
    stored_codes1 = open(file_name, 'wb')
    pickle.dump(code_list, stored_codes1)
    stored_codes1.close()

    # redoes the label displaying the current code
    current_code['text'] = input_code

    # clears the key entry
    stream_code.delete(0, 'end')

    # adds the new key to the list of keys
    value.set(input_code)
    existing_codes['menu'].add_command(label=input_code, command=_setit(value, input_code))


# Program to clear stream keys from memory+screen

def clear_code():
    global code_list, stream_code

    # Clearing stream keys from memory
    code_list = ['']
    stored_codes = open(file_name, 'wb')
    pickle.dump(code_list, stored_codes)
    stored_codes.close()

    # Clearing stream keys from GUI
    current_code['text'] = ''
    stream_code.delete(0, 'end')
    value.set('')
    existing_codes['menu'].delete(0, 'end')


# Program to select new stream code from existing ones

def change_code():
    global existing_codes

    chosen_code = value.get()
    current_code['text'] = chosen_code


# check to make see if this is the first time (check list in file is not empty, if empty have none come up)

current_codetext = code_list[0]

# current stream key should be the last used stream key (if any)
stream_label = ttk.Label(settings, text='Current stream key:')
stream_label.grid(column=0, row=1)
current_code = ttk.Label(settings, text=current_codetext)
current_code.grid(column=1, row=1, columnspan=2)


# function to clear space for keyboard
def keyboard_space_settings(*args):
    clear_label.grid_forget()
    clr_lbl_bck.grid_forget()
    clear_button.grid_forget()
    audio_chklbl.grid_forget()
    audio_chk.grid_forget()
    delay_lbl.grid_forget()
    BckLbl.grid_forget()
    delay.grid_forget()
    frame_rate_label.grid_forget()
    bit_rate_label.grid_forget()
    frame_rate_scroller.grid_forget()
    bit_rate_scroller.grid_forget()
    keyboard_on(keyboard_frame1.children['!frame'])


def reset_page(current_frame):
    current_frame.grid_forget()
    clear_label.grid(column=0, row=4)
    clr_lbl_bck.grid(column=1, row=4, columnspan=2)
    audio_chklbl.grid(column=0, row=5)
    audio_chk.grid(column=1, row=5, columnspan=2)
    clear_button.grid(column=1, row=4, columnspan=2)
    delay_lbl.grid(column=0, row=6)
    BckLbl.grid(column=1, row=6, columnspan=2)
    delay.grid(column=1, row=6, columnspan=2)
    frame_rate_label.grid(column=0, row=7)
    bit_rate_label.grid(column=0, row=8)
    frame_rate_scroller.grid(column=1, row=7, columnspan=2)
    bit_rate_scroller.grid(column=1, row=8, columnspan=2)


# user to input stream key
stream_inputlabel = ttk.Label(settings, text='Enter key:')
stream_inputlabel.grid(column=0, row=2)
stream_text = StringVar()
stream_code = ttk.Entry(settings, textvariable=stream_text)
stream_code.bind("<Button>", keyboard_space_settings)
stream_code.grid(column=1, row=2)
stream_enter = ttk.Button(settings, text='Use key', command=enter_code)
stream_enter.grid(column=2, row=2)

keyboard_frame1 = Frame(settings)
keyboard_frame1.configure(bg=style.lookup('TFrame', 'background'))
keyboard_frame1.grid(column=0, row=4, columnspan=3, rowspan=4)
keyboard_frame1.rowconfigure(0, weight=1)
keyboard_frame1.columnconfigure(0, weight=1)

keyboard_frame1 = create_keyboard(keyboard_frame1, stream_code, stream_text, style, reset_page)

# User to choose stream key (should appear in order of last used)
stream_p_label = ttk.Label(settings, text="Saved keys:")
stream_p_label.grid(column=0, row=3)
value = StringVar()
value.set(current_codetext)  # Setting the key (should be last key used)
existing_codes = ttk.OptionMenu(settings, value, *code_list)
existing_codes.grid(column=1, row=3)
stream_p_enter = ttk.Button(settings, text="Use key", command=change_code)
stream_p_enter.grid(column=2, row=3)

# Clearing list of stream codes
clear_label = ttk.Label(settings, text='Clear keys:')
clear_label.grid(column=0, row=4)
clr_lbl_bck = ttk.Label(settings, text='')
clr_lbl_bck.grid(column=1, row=4, columnspan=2)
clear_button = ttk.Button(settings, text='Clear keys', command=clear_code)
clear_button.grid(column=1, row=4, columnspan=2)

# Allow stream w_out audio?
audio_chklbl = ttk.Label(settings, text='Audioless streaming:')
audio_chklbl.grid(column=0, row=5)
audio_chk = ttk.Checkbutton(settings, var=chk_state)
audio_chk.grid(column=1, row=5, columnspan=2)

# Code for delay_option
delay_lbl = ttk.Label(settings, text="Audio-video delay:")
delay_lbl.grid(column=0, row=6)
BckLbl = ttk.Label(settings, text='')
BckLbl.grid(column=1, row=6, columnspan=2)

# initial value
delay = ttk.Spinbox(settings, from_=-5000, to=5000, increment=20, textvariable=delay_value)
delay.grid(column=1, row=6, columnspan=2)

frame_rate_label = ttk.Label(settings, text='Frame Rate:')
frame_rate_scroller = ttk.Spinbox(settings, from_=0, to=100, textvariable=frame_rate)
frame_rate_scroller.grid(column=1, row=7, columnspan=2)
frame_rate_label.grid(column=0, row=7)

bit_rate_label = ttk.Label(settings, text='Bit Rate: ')
bit_rate_scroller = ttk.Spinbox(settings, from_=0, to=100, textvariable=bit_rate)
bit_rate_label.grid(column=0, row=8)
bit_rate_scroller.grid(column=1, row=8, columnspan=2)


# More settings ---------------------------------------------------------------------------------------------


# Touchscreen calibration
def touchscreen_calibration():
    os.system("usr/bin/xinput_calibrator | tail -6 > /etc/X11/xorg.conf.d/99-calibration.conf")


screen_calib = ttk.Button(settings2, text="Touchscreen Calibration", command=touchscreen_calibration)
screen_calib.grid(column=0, row=0, columnspan=2)

# Stream display--------------------------------------------------------------------------------------------------------

stream.grid_rowconfigure((0, 3), weight=2)
stream.grid_rowconfigure((1, 2), weight=3)
stream.grid_columnconfigure((0, 1), weight=1)
stream.grid_rowconfigure(1, weight=4)


def start_stream():
    # insert code here for checking WiFi connection, stream code (if it is in the correct format), camera + audio.
    #
    #
    #
    #
    #
    #

    if wifi_connected['text'] != "Connected":
        messagebox.showwarning("Wifi warning", "Please connect to wifi to stream")
    elif current_code['text'] == "AHAHAHA":
        messagebox.showwarning("Stream code warning", "Please input a valid stream code")
    elif audio_connection == 0:
        messagebox.showwarning("Audio warning", "No audio input detected")
    elif video_connection == 0:
        messagebox.showwarning("Video warning", "No video input detected")
    else:
        messagebox.showinfo("Full speed ahead", "Checks complete: We're good to go")
        # code for turning button red
        go_btn.configure(text='Stop', bg='red', command=stop_stream)
        go_btn.pack()

        # Here is the section where the code to start the stream should go
        #


def stop_stream():
    # insert code for stopping stream here
    #
    go_btn.configure(text='Go', bg='green', command=start_stream)


# Go button
go_btn = ttk.Button(stream, text='Go', command=start_stream)
go_btn.grid(column=2, row=3)


# Button to select between video options

arrow_width = 40
arrow_height = 40

uparrow = Image.open(
    "\\Users\\Matthew Scholar\\PycharmProjects\\touchscreen-main\\Touchscreen_photos\\UpArrow.png")  # needs to be
# whatever your directory is
up_per = (arrow_width / float(uparrow.size[0]))
height = int((float(uparrow.size[1]) * float(up_per)))
uparrow = uparrow.resize((arrow_width, height))
uparrowrender = ImageTk.PhotoImage(uparrow)

downarrow = Image.open(
    "\\Users\\Matthew Scholar\\PycharmProjects\\touchscreen-main\\Touchscreen_photos\\DownArrow.png")  # needs to be
# whatever your directory is
down_per = (arrow_width / float(downarrow.size[0]))
height = int((float(downarrow.size[1]) * float(down_per)))
downarrow = downarrow.resize((arrow_width, height))
downarrowrender = ImageTk.PhotoImage(downarrow)

leftarrow = Image.open(
    "\\Users\\Matthew Scholar\\PycharmProjects\\touchscreen-main\\Touchscreen_photos\\LeftArrow.png")  # needs to be
# whatever your directory is
left_per = (arrow_height / float(leftarrow.size[0]))
height = int((float(leftarrow.size[1]) * float(left_per)))
leftarrow = leftarrow.resize((arrow_height, height))
leftarrowrender = ImageTk.PhotoImage(leftarrow)

rightarrow = Image.open(
    "\\Users\\Matthew Scholar\\PycharmProjects\\touchscreen-main\\Touchscreen_photos\\RightArrow.png")  # needs to be
# whatever your directory is
right_per = (arrow_height / float(rightarrow.size[0]))
rightarrow = rightarrow.resize((arrow_height, height))
rightarrowrender = ImageTk.PhotoImage(rightarrow)

customise_names = [['Reset', vs.make_normal, 'Reset'], ['Make Grey', vs.make_grey, 'Grey'],
                   ['Brightness up', vs.make_bright, 'Brightness'], ['Brightness down', vs.make_dark, 'Brightness'],
                   ['Blur', vs.make_blur, 'Blur/Sharpen'], ['Sharpen', vs.make_sharpen, 'Blur/Sharpen'],
                   ['Rotate clock', vs.make_clockwise_rotate, 'Rotate'],
                   ['Rotate anticlock', vs.make_anticlockwise_rotate
                       , 'Rotate'], ['Zoom in', vs.make_zoom_in, 'Zoom'],
                   ['Zoom out', vs.make_zoom_out, 'Zoom'], [leftarrowrender, vs.make_pan_left, 'Pan'],
                   [rightarrowrender, vs.make_pan_right, 'Pan'], [uparrowrender, vs.make_pan_up, 'Pan'],
                   [downarrowrender, vs.make_pan_down, 'Pan'], ['Emboss', vs.make_emboss, 'Emboss'],
                   ['Outline', vs.make_edge_detection, 'Outline'], ['Sepia', vs.make_sepia, 'Sepia']]

windows_names = ['Reset', 'Grey', 'Brightness', 'Blur/Sharpen', 'Rotate', 'Zoom', 'Pan', 'Emboss', 'Outline', 'Sepia']
windows = list(range(len(windows_names)))
buttons = list(range(len(customise_names)))

for i in range(len(buttons)):
    buttons[i] = Customise_button(customise_names[i][2], customise_names[i][0], customise_names[i][1])

for i in range(len(windows)):
    windows[i] = Customise_window(windows_names[i])
    for j in buttons:
        windows[i].add_button(j)

windows_dic = {'Reset': windows[0], 'Grey': windows[1], 'Brightness': windows[2], 'Blur/Sharpen': windows[3],
               'Rotate': windows[4], 'Zoom': windows[5], 'Pan': windows[6], 'Emboss': windows[7], 'Outline': windows[8],
               'Sepia': windows[9]}

current_window = windows_dic['Pan']
current_window.create_window()


# function to change the thing being customized

def change_mode(new_window):
    global current_window, windows_dic
    current_window.close_window()
    windows_dic[new_window].create_window()
    current_window = windows_dic[new_window]


# button for dropdown list where user can change video type

customise = StringVar()
customise.set('Customise')

labelscus = ['Customise']
print(labelscus)
labelscus.extend(windows_names)
print(labelscus)

video_customise = ttk.OptionMenu(stream, customise, *labelscus, command=change_mode)
video_customise.grid(column=2, row=0)

# displaying preview of stream

# 400 for big, 300 for small
stock_height = 250
stock_width = int(1.3333333 * stock_height)

stock = Label(stream, bg=style.lookup('TFrame', 'background'))
stock.grid(column=0, row=0, columnspan=2, rowspan=3, sticky='nw')

vs.show_frame(stock, stock_height, stock_width)
# Tutorial section

rick_roll = ttk.Label(tutorial, text="""Guide to using this touchscreen explaining what a stream key 
is,how the process works (i.e. that they need wifi, a video and audio device connected and a valid stream key. Also will 
explain what the delay between audio/video is and why it is necessary,
along with other necessary things...""")
rick_roll.pack(fill=BOTH)

app.mainloop()
