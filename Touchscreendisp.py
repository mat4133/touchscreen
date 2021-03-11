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
import StreamSetting

# See README for information about this

starting = 0
audio_connection = 0
video_connection = 0
camera_stream_indicator = 0
screen_stream_indicator = 0


class Customise_button(ttk.Button):
    def __init__(self, parent, text, command):
        self.parent = parent
        if type(text).__name__ == 'PhotoImage':
            self.name = 'arrow'
            super().__init__(stream, image=text, command=command)
        else:
            self.name = text
            if self.name == 'LQ stream start' or self.name == 'HQ stream start':
                super().__init__(stream, text=text, command=command, style='W.TButton')
            elif self.name == 'Stop':
                super().__init__(stream, text=text, command=command, style='B.TButton')
            else:
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
            self.button_list[0].grid(column=0, row=3, columnspan=3)
        if len(self.button_list) == 2:
            self.button_list[0].grid(column=0, row=3, columnspan=3)
            self.button_list[1].grid(column=4, row=1, rowspan=2)
        if len(self.button_list) == 3:
            self.button_list[0].grid(column=0, row=3, columnspan=1, sticky='nesw')
            self.button_list[1].grid(column=1, row=3, columnspan=3, sticky='nesw')
            self.button_list[2].grid(column=4, row=3, sticky='nesw')
        if len(self.button_list) == 4:
            self.button_list[0].grid(column=0, row=3, columnspan=2)
            self.button_list[1].grid(column=2, row=3, columnspan=2)
            self.button_list[2].grid(column=4, row=1)
            self.button_list[3].grid(column=4, row=2)
        if len(self.button_list) == 6:
            self.button_list[0].grid(column=2, row=3)
            self.button_list[1].grid(column=2, row=4)
            self.button_list[2].grid(column=0, row=3, rowspan=2)
            self.button_list[3].grid(column=1, row=3, rowspan=2)
            self.button_list[4].grid(column=4, row=1)
            self.button_list[5].grid(column=4, row=2)

    def close_window(self):
        for i in self.button_list:
            i.grid_forget()

    def __repr__(self):
        return self.button_list.__repr__()


# Functions for resetting back to the default settings
def set_defaults():
    settings_file = open('/home/pi/touchscreen-main/settings_file', 'wb')
    settings_dic = {'frame_rate': 30, 'audioless': False, 'audio_delay': 0, 'platform': 0}
    pickle.dump(settings_dic, settings_file)
    settings_file.close()


# Function for reading the settings from settings_file
def inital_settings():
    global frame_rate, delay_value, chk_state, platform
    try:
        previous_settings = open('settings_file', 'rb')
        saved_values = pickle.load(previous_settings)
        chk_state = IntVar(value=saved_values['audioless'])
        frame_rate = DoubleVar(value=saved_values['frame_rate'])
        delay_value = DoubleVar(value=saved_values['audio_delay'])
        platform = IntVar(value=saved_values['platform'])
        previous_settings.close()
    except:
        set_defaults()
        chk_state = IntVar(value=False)
        frame_rate = DoubleVar(value=30)
        delay_value = DoubleVar(value=0)
        platform = IntVar(value=0)


# Function for updating file every 5 seconds with new settings
def update_settings(*args):
    global frame_rate, delay_value, chk_state, platform, screen_stream, camera_stream
    settings_dic = {'frame_rate': frame_rate.get(), 'audioless': chk_state.get(),
                    'audio_delay': delay_value.get(), 'platform': platform.get()}
    settings_file = open('/home/pi/touchscreen-main/settings_file', 'wb')
    pickle.dump(settings_dic, settings_file)
    settings_file.close()
    # screen_stream = function_maker(StreamSetting.STREAM_SCREEN_COMMAND, frame_rate.get(), bit_rate.get(),
    # delay_value.get(), code_dic[current_code['text']], platform.get(), 1)
    # camera_stream = function_maker(StreamSetting.STREAM_CAMERA_COMMAND, frame_rate.get(), bit_rate.get(),
    # delay_value.get(), code_dic[current_code['text']], platform.get(), 1)
    threading.Timer(2, update_settings).start()


#funtion to check which format stream code is in and whether that is correct
def stream_code_checker(stream_code):
    not_youtube = 0
    not_facebook = 0
    for i in range(len(stream_code)):
        if (i-4)%5 == 0:
            if stream_code[i] != '-':
                not_youtube += 1
        else:
            if stream_code[i] not in 'abcdefghijklmnopqrstuvwxyz0123456789':
                not_youtube += 1
    if len(stream_code) != 24:
        not_youtube += 1
    if ('?s_bl=1&s_ps' not in stream_code) or ('=api-s&a=' not in stream_code):
        not_facebook += 1
    if len(stream_code) != 75 and len(stream_code) != 90:
        not_facebook += 1
    if not_youtube > 0 and not_facebook > 0:
        return 'None'
    elif not_facebook > 0:
        return 'Youtube'
    elif not_youtube > 0:
        return 'Facebook'
    else:
        return 'Both'


app = Tk()

app.title('Streaming on a prayer')

app.geometry('480x320')

# swap to fullscreen when using touchscreen
#app.attributes('-fullscreen', True)

# initializing style
style = ThemedStyle(app)
style.set_theme("equilux")

style.configure('W.TButton', foreground='green', weight='bold')
style.configure('B.TButton', foreground='red', weight='bold')

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

stock_height = 250
stock_width = int(1.33333 * stock_height)
stock = Label(stream, bg=style.lookup('TFrame', 'background'))

note.add(stream, text="STREAM")
note.add(settings, text="SETTINGS")
note.add(wifi_login, text="WIFI")
note.add(tutorial, text="TUTORIAL")

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
    toggle_btn.grid(row=3, column=1)
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
    connect_btn.grid(columnspan=2, row=3)
    toggle_btn.grid_forget()
    keyboard_frame3.grid_forget()


saved_networks = wf.save_get()
print('Saved_networks:', saved_networks)

counter = 0
connected = False

while (counter < len(saved_networks) and connected == False):
    counter += 1
    connected = wf.save_conf(saved_networks[counter-1],0)
counter = 0

saved_networks = []
wifi_login.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)
wifi_login.grid_columnconfigure((0, 1), weight=1)

# Code for Wifi connection
wifi_label = ttk.Label(wifi_login, text='WiFi')
wifi_label.grid(column=0, row=0)

if connected == False:
    wifi_connected = ttk.Label(wifi_login, text='Unconnected')
else:
    wifi_connected = ttk.Label(wifi_login, text='Connected')
wifi_connected.grid(column=1, row=0)

search_label = ttk.Label(wifi_login, text='Nearby Networks')
search_label.grid(column=0, row=1)


def password_filler(*args):
    global candidate_network, saved_networks
    saved = 0
    for networks in saved_networks:
        if networks.SSID == args[0].SSID:
            password_text.set(networks.password)
            saved = 1
    for networks in search_list:
        # print(type(networks.SSID), type(args[0].SSID))
        if networks.SSID == args[0].SSID:
            candidate_network = networks
    if saved == 0:
        password_text.set('')


candidate_network = 'none'


def connect():
    global candidate_network
    print(candidate_network)
    try:
        candidate_network.password = password_text.get()
        if candidate_network in saved_networks:
            success = wf.save_conf(candidate_network, 0)
        else:
            success = wf.save_conf(candidate_network, 1)
        if success == False:
            failed_connection = messagebox.showerror("Wifi connection failed")
        else:
            wifi_connected.configure(text="Connected")
        wf.dump()
    except:
        print("No Network Detected")


search_list = wf.scan()
# search_list = ['list of networks', 'Glide0028763-5G', 'Glide0028763-2G']

option_menu_list = []
for networks in search_list:
    option_menu_list.append(networks.SSID)

current_network = StringVar(value='network 3')
search_networks = ttk.OptionMenu(wifi_login, current_network, *search_list, command=password_filler)
search_networks.grid(column=1, row=1)

password_lbl = ttk.Label(wifi_login, text='PASSWORD:')
password_lbl.grid(column=0, row=2)


def toggle_password():
    if password_entr.cget('show') == '':
        password_entr.config(show='*')
        toggle_btn.config(text='Show Password')
    else:
        password_entr.config(show='')
        toggle_btn.config(text='Hide Password')


password_text = StringVar()
password_entr = ttk.Entry(wifi_login, show='*', textvariable=password_text)
password_entr.grid(column=1, row=2)
password_entr.bind("<Button>", password_space_wifi)

toggle_btn = ttk.Button(wifi_login, text='Show Password', command=toggle_password)

clear_btn = ttk.Button(wifi_login, text='Clear Saved Networks', command=wf.clear)
clear_btn.grid(column=0, row=3)

connect_btn = ttk.Button(wifi_login, text='CONNECT/SAVE', command=connect)
connect_btn.grid(column =1, row=3)

keyboard_frame3 = Frame(wifi_login)
keyboard_frame3.configure(bg=style.lookup('TFrame', 'background'))
keyboard_frame3.grid(column=0, row=4, columnspan=2, rowspan=2)
keyboard_frame3.rowconfigure(0, weight=1)
keyboard_frame3.columnconfigure(0, weight=1)

keyboard_frame3 = create_keyboard(keyboard_frame3, password_entr, password_text, style, password_keyboard_off)

# Settings frame--------------------------------------------------------------------------------------

'''

# Adding scrollbar to frame-----------------------------------

canvas = Canvas(settings2, borderwidth=0, highlightthickness=0, bd=0, bg=style.lookup('TFrame', 'background'))
canvas.pack(side=LEFT, fill=BOTH, expand=True)

scroll = ttk.Scrollbar(settings2, orient='vertical', command=canvas.yview)
scroll.pack(side=RIGHT, fill=Y, expand='false')
scroll.config(command=canvas.yview)

canvas.config(yscrollcommand=scroll.set, scrollregion=(0, 0, 0, 600))
canvas.pack(fill=BOTH, side=LEFT, expand=TRUE)

# reset the view
canvas.xview_moveto(0)
canvas.yview_moveto(0)

# create frame inside canvas

settings = ttk.Frame(canvas)
settings.pack()
settings_id = canvas.create_window(50, 0, window=settings, anchor=NW)


# settings.config(width=466)


def _configure_interior(event):
    # update the scrollbars to match the size of the inner frame
    size = (settings.winfo_reqwidth(), settings.winfo_reqheight())
    canvas.config(scrollregion="0 0 %s %s" % size)
    if settings.winfo_reqwidth() != canvas.winfo_width():
        # update the canvas's width to fit the inner frame
        canvas.config(width=settings.winfo_reqwidth())


settings.bind('<Configure>', _configure_interior)


def _configure_canvas(event):
    settings.configure(width=canvas.winfo_width())
    if settings.winfo_reqwidth() != canvas.winfo_width():
        # update the inner frame's width to fill the canvas
        canvas.itemconfigure(settings_id, width=canvas.winfo_width())


canvas.bind('<Configure>', _configure_canvas)

'''

# importing default settings -------------------------------------------------------------------------

# code for saving and importing streams

file_name = '/home/pi/touchscreen-main/stream_codes'

# reading the stream codes from memory
stored_codes2 = open(file_name, 'rb')
codedic_list = pickle.load(stored_codes2)
code_list = codedic_list[0]
code_dic = codedic_list[1]
stored_codes2.close()


# code for entering a new key
def enter_code():
    global code_list, code_dic, screen_stream, camera_stream
    input_code = stream_code.get()
    actual_code = input_code
    # checks if this is the first key entered and if so deletes the '' that was in it's place
    if len(input_code) > 30:
        input_code = input_code[0:30] + '...'
    code_dic[input_code] = actual_code
    if code_list[0] == '':
        code_list.remove('')
        existing_codes['menu'].delete(0)

    code_list.insert(0, input_code)
    codedic_list = [code_list, code_dic]
    # adds the new key to a file
    stored_codes1 = open(file_name, 'wb')
    pickle.dump(codedic_list, stored_codes1)
    stored_codes1.close()

    # redoes the label displaying the current code
    current_code['text'] = input_code

    # clears the key entry
    stream_code.delete(0, 'end')

    # adds the new key to the list of keys
    value.set(input_code)
    #screen_stream = function_maker(StreamSetting.STREAM_SCREEN_COMMAND, frame_rate.get(), bit_rate.get(),
    #delay_value.get(), code_dic[current_code['text']], platform.get(), 1)
    #camera_stream = function_maker(StreamSetting.STREAM_CAMERA_COMMAND, frame_rate.get(), bit_rate.get(),
    #delay_value.get(), code_dic[current_code['text']], platform.get(), 1)
    existing_codes['menu'].add_command(label=input_code, command=_setit(value, input_code))


# Program to clear stream keys from memory+screen

def clear_code():
    global code_list, stream_code

    # Clearing stream keys from memory
    code_list = ['']
    codedic_list = [code_list, {}]
    stored_codes = open(file_name, 'wb')
    pickle.dump(codedic_list, stored_codes)
    stored_codes.close()

    # Clearing stream keys from GUI
    current_code['text'] = ''
    stream_code.delete(0, 'end')
    value.set('')
    existing_codes['menu'].delete(0, 'end')


# Program to select new stream code from existing ones

def change_code(*args):
    global existing_codes, screen_stream, camera_stream, code_list, code_dic

    chosen_code = value.get()
    current_code['text'] = chosen_code
    
    code_list.remove(chosen_code)
    code_list.insert(0, chosen_code)
    codedic_list = [code_list, code_dic]
    # adds the new key to a file
    stored_codes1 = open(file_name, 'wb')
    pickle.dump(codedic_list, stored_codes1)
    stored_codes1.close()

    #screen_stream = function_maker(StreamSetting.STREAM_SCREEN_COMMAND, frame_rate.get(), bit_rate.get(),
    #delay_value.get(), code_dic[current_code['text']], platform.get(), 1)
    #camera_stream = function_maker(StreamSetting.STREAM_CAMERA_COMMAND, frame_rate.get(), bit_rate.get(),
    #delay_value.get(), code_dic[current_code['text']], platform.get(), 1)


# check to make see if this is the first time (check list in file is not empty, if empty have none come up)

current_codetext = code_list[0]

# current stream key should be the last used stream key (if any)
stream_label = ttk.Label(settings, text='Current stream key:')
stream_label.grid(column=0, row=0)
current_code = ttk.Label(settings, text=current_codetext)
current_code.grid(column=1, row=0, columnspan=2)

# thing to start settings updator
if starting == 0:
    inital_settings()
    update_settings()
    starting = 1


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
    platform_btn.grid_forget()
    platform_label.grid_forget()
    current_platform.grid_forget()
    screen_calib.grid_forget()
    frame_rate_label.grid_forget()
    frame_rate_scroller.grid_forget()
    
    keyboard_on(keyboard_frame1.children['!frame'])


def reset_page(current_frame):
    current_frame.grid_forget()
    clear_label.grid(column=0, row=3)
    clr_lbl_bck.grid(column=1, row=3, columnspan=2)
    audio_chklbl.grid(column=0, row=5)
    audio_chk.grid(column=1, row=5, columnspan=2)
    clear_button.grid(column=1, row=3, columnspan=2)
    delay_lbl.grid(column=0, row=6)
    BckLbl.grid(column=1, row=5, columnspan=2)
    delay.grid(column=1, row=6, columnspan=2)
    platform_btn.grid(row=4, column=2)
    platform_label.grid(row=4, column=0)
    current_platform.grid(row=4, column=1)
    screen_calib.grid(row=8, column=1)
    frame_rate_label.grid(column=0, row=7)
    frame_rate_scroller.grid(column=1, row=7, columnspan=2)


# user to input stream key
stream_inputlabel = ttk.Label(settings, text='Enter key:')
stream_inputlabel.grid(column=0, row=1)
stream_text = StringVar()
stream_code = ttk.Entry(settings, textvariable=stream_text)
stream_code.bind("<Button>", keyboard_space_settings)
stream_code.grid(column=1, row=1)
stream_enter = ttk.Button(settings, text='Use key', command=enter_code)
stream_enter.grid(column=2, row=1)

keyboard_frame1 = Frame(settings)
keyboard_frame1.configure(bg=style.lookup('TFrame', 'background'))
keyboard_frame1.grid(column=0, row=4, columnspan=3, rowspan=4)
keyboard_frame1.rowconfigure(0, weight=1)
keyboard_frame1.columnconfigure(0, weight=1)

keyboard_frame1 = create_keyboard(keyboard_frame1, stream_code, stream_text, style, reset_page)

# User to choose stream key (should appear in order of last used)
stream_p_label = ttk.Label(settings, text="Saved keys:")
stream_p_label.grid(column=0, row=2)
value = StringVar()
value.set(current_codetext)# Setting the key (should be last key used)
value.trace('w', change_code)
existing_codes = ttk.OptionMenu(settings, value, *code_list)
existing_codes.grid(column=1, row=2, columnspan=2)

# Clearing list of stream codes
clear_label = ttk.Label(settings, text='Clear keys:')
clear_label.grid(column=0, row=3)
clr_lbl_bck = ttk.Label(settings, text='')
clr_lbl_bck.grid(column=1, row=3, columnspan=2)
clear_button = ttk.Button(settings, text='Clear keys', command=clear_code)
clear_button.grid(column=1, row=3, columnspan=2)

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
delay = ttk.Spinbox(settings, from_=-50, to=50, increment=0.1, textvariable=delay_value)
delay.grid(column=1, row=6, columnspan=2)

frame_rate_label = ttk.Label(settings, text='Frame Rate:')
frame_rate_scroller = ttk.Spinbox(settings, from_=0, to=100, textvariable=frame_rate)
frame_rate_scroller.grid(column=1, row=7, columnspan=2)
frame_rate_label.grid(column=0, row=7)



# More settings ---------------------------------------------------------------------------------------------


# Touchscreen calibration
def touchscreen_calibration():
    os.system("/usr/bin/xinput_calibrator | tail -6 > /etc/X11/xorg.conf.d/99-calibration.conf")


screen_calib = ttk.Button(settings, text="Calibrate screen", command=touchscreen_calibration)
screen_calib.grid(column=1, row=8)


# Change streaming platform-----------------------------------------------------------------------------

def change_platform():
    global platform
    if platform.get() == 1:
        platform = IntVar(value=0)
        platform_name = ' Facebook '
    elif platform.get() == 0:
        platform = IntVar(value=1)
        platform_name = ' YouTube '
    # print(platform)
    current_platform = ttk.Label(settings, text=platform_name)
    current_platform.grid(row=4, column=1)


platform_label = ttk.Label(settings, text='Streaming Platform:')
platform_label.grid(row=4, column=0)
platform_btn = ttk.Button(settings, text='Change Platform', command=change_platform)
platform_btn.grid(row=4, column=2)

if platform.get() == 0:
    platform_name = ' Facebook '
elif platform.get() == 1:
    platform_name = ' YouTube '
current_platform = ttk.Label(settings, text=platform_name)
current_platform.grid(row=4, column=1)

# Stream display--------------------------------------------------------------------------------------------------------

stream.grid_rowconfigure((0, 3), weight=2)
stream.grid_rowconfigure((1, 2), weight=3)
stream.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)
stream.grid_rowconfigure(1, weight=4)

def start_camera_stream_command():
    camera_stream = function_maker(StreamSetting.STREAM_CAMERA_COMMAND, frame_rate.get(), delay_value.get(), code_dic[current_code['text']], platform.get(), chk_state.get())
    return camera_stream

def start_camera_stream():
    global camera_stream_indicator, stream_btn, stream_btn1
    if platform.get() == 1 and stream_code_checker(code_dic[current_code['text']]) == 'Facebook':
        messagebox.showerror("", "Stream code is formatted for Facebook and you are trying to stream to Youtube. Change either stream key or platform in settings")
    elif platform.get() == 0 and stream_code_checker(code_dic[current_code['text']]) == 'Youtube':
        messagebox.showerror("", 'Stream code is formatted for Youtube and you are trying to stream to Facebook. Change either stream key or platform in settings')
    elif stream_code_checker(code_dic[current_code['text']]) == 'None':
        messagebox.showerror("", 'Stream key is in an invalid format. Check your stream key')
    else:
        camera_stream = start_camera_stream_command()
        #stream_btn.configure(text='Streaming', command=None)
        #stream_btn1.configure(text='Streaming', command=None)
        print(buttons[18])
        print(buttons[19])
        buttons[18].configure(text='Streaming', state=DISABLED)
        buttons[19].configure(text='Streaming', state=DISABLED)
        camera_stream_indicator = 1
        vs.stop_view()
        threading.Thread(target = camera_stream).start()

def start_screen_stream_command():
    screen_stream = function_maker(StreamSetting.STREAM_SCREEN_COMMAND, frame_rate.get(), delay_value.get(), code_dic[current_code['text']], platform.get(), chk_state.get())
    return screen_stream

def start_screen_stream():
    global screen_stream_indicator, stream_btn, stream_btn1
    if platform.get() == 1 and stream_code_checker(code_dic[current_code['text']]) == 'Facebook':
        messagebox.showerror('Stream code is formatted for Facebook and you are trying to stream to Youtube. Change either stream key or platform in settings')
    elif platform.get() == 0 and stream_code_checker(code_dic[current_code['text']]) == 'Youtube':
        messagebox.showerror('Stream code is formatted for Youtube and you are trying to stream to Facebook. Change either stream key or platform in settings')
    elif stream_code_checker(code_dic[current_code['text']]) == 'None':
        messagebox.showerror('Stream key is in an invalid format. Check your stream key')
    else:
        screen_stream_indicator = 1
        screen_stream = start_screen_stream_command()
        note.tab(1, state='disabled')
        note.tab(2, state='disabled')
        note.tab(3, state='disabled')
        #stream_btn.configure(text='Streaming', command=None)
        #stream_btn1.configure(text='Streaming', command=None)
        buttons[18].configure(text='Streaming', state=DISABLED)
        buttons[19].configure(text='Streaming', state=DISABLED)
        threading.Thread(target = screen_stream).start()


def stop_stream():
    global stock, stock_height, stock_width, camera_stream_indicator, screen_stream_indicator
    if camera_stream_indicator == 1:
        StreamSetting.STOP()
        vs.start_view()
        vs.cap_set(stock, stock_height, stock_width)
        camera_stream_indicator = 0
        #stream_btn.configure(text='HQ Stream', command=start_camera_stream)
        #stream_btn1.configure(text='LQ Stream', command=start_screen_stream)
    elif screen_stream_indicator == 1:
        note.tab(1, state='normal')
        note.tab(2, state='normal')
        note.tab(3, state='normal')
        #stream_btn.configure(text='HQ Stream', command=start_camera_stream)
        #stream_btn1.configure(text='LQ Stream', command=start_screen_stream)
        StreamSetting.STOP_SCREEN()
        screen_stream_indicator = 0
    buttons[18].configure(text='LQ Stream', command=start_screen_stream, state=ACTIVE)
    buttons[19].configure(text='HQ Stream', command=start_camera_stream, state=ACTIVE)


# Go button
StreamButtons = Frame(stream)
stream_btn = ttk.Button(StreamButtons, text='HQ Stream', command=start_camera_stream)
stream_btn.grid(column=0, row=0)
stream_btn1 = ttk.Button(StreamButtons, text='LQ Stream', command=start_screen_stream)
stream_btn1.grid(column=0, row=1)
stream_btn2 = ttk.Button(StreamButtons, text='Stop', command=stop_stream)
stream_btn2.grid(column=0, row=2)
StreamButtons.grid(column=4, row=3, rowspan=2)

stream_btn3 = ttk.Button(stream, text='Stop', command=stop_stream)
stream_btn3.grid(column=4, row=3, rowspan=2, sticky='nesw')

# Button to select between video options

arrow_width = 40
arrow_height = 40

uparrow = Image.open(
    #'\\Users\\Matthew Scholar\\PycharmProjects\\touchscreen-main\\Touchscreen_photos\\UpArrow.png')
    "/home/pi/touchscreen-main/Touchscreen_photos/UpArrow.png")  # needs to be
#
up_per = (arrow_width / float(uparrow.size[0]))
height = int((float(uparrow.size[1]) * float(up_per)))
uparrow = uparrow.resize((arrow_width, height))
uparrowrender = ImageTk.PhotoImage(uparrow)

downarrow = Image.open(
    #'\\Users\\Matthew Scholar\\PycharmProjects\\touchscreen-main\\Touchscreen_photos\\DownArrow.png')
    "/home/pi/touchscreen-main/Touchscreen_photos/DownArrow.png")  # needs to be
# whatever your directory is
down_per = (arrow_width / float(downarrow.size[0]))
height = int((float(downarrow.size[1]) * float(down_per)))
downarrow = downarrow.resize((arrow_width, height))
downarrowrender = ImageTk.PhotoImage(downarrow)

leftarrow = Image.open(
    #'\\Users\\Matthew Scholar\\PycharmProjects\\touchscreen-main\\Touchscreen_photos\\LeftArrow.png')
     "/home/pi/touchscreen-main/Touchscreen_photos/LeftArrow.png")  # needs to be
# whatever your directory is
left_per = (arrow_height / float(leftarrow.size[0]))
height = int((float(leftarrow.size[1]) * float(left_per)))
leftarrow = leftarrow.resize((arrow_height, height))
leftarrowrender = ImageTk.PhotoImage(leftarrow)

rightarrow = Image.open(
    "/home/pi/touchscreen-main/Touchscreen_photos/RightArrow.png")
    #'\\Users\\Matthew Scholar\\PycharmProjects\\touchscreen-main\\Touchscreen_photos\\RightArrow.png')  # needs to be
# whatever your directory is
right_per = (arrow_height / float(rightarrow.size[0]))
rightarrow = rightarrow.resize((arrow_height, height))
rightarrowrender = ImageTk.PhotoImage(rightarrow)

customise_names = [['Make Grey', vs.make_grey, 'Colour'],
                   ['Brightness up', vs.make_bright, 'Properties'], ['Brightness down', vs.make_dark, 'Properties'],
                   ['Blur', vs.make_blur, 'Properties'], ['Sharpen', vs.make_sharpen, 'Properties'],
                   ['Rotate clock', vs.make_clockwise_rotate, 'Rotate'],
                   ['Rotate anticlock', vs.make_anticlockwise_rotate
                       , 'Rotate'], ['Zoom in', vs.make_zoom_in, 'Zoom/Pan'],
                   ['Zoom out', vs.make_zoom_out, 'Zoom/Pan'], [leftarrowrender, vs.make_pan_left, 'Zoom/Pan'],
                   [rightarrowrender, vs.make_pan_right, 'Zoom/Pan'], [uparrowrender, vs.make_pan_up, 'Zoom/Pan'],
                   [downarrowrender, vs.make_pan_down, 'Zoom/Pan'],
                   ['Outline', vs.make_edge_detection, 'Effects'], ['Low Light', vs.make_sepia, 'Colour'],
                   ['Face Detection', vs.detect_face, 'Effects'], ['Motion Tracker', vs.motion_tracker, 'Effects'],
                   ['Autofocus', vs.auto_focus, 'Effects'], ['LQ stream start', start_screen_stream, 'Start'],
                   ['HQ stream start', start_camera_stream, 'Start'], ['Stop', stop_stream, 'Start'],
                   ['Colour Reset', vs.make_colour_reset, 'Reset'], 
                   ['Zoom Reset', vs.make_zoom_reset, 'Reset'],['Full Reset', vs.make_full_reset, 'Reset'], ['Centre Zoom', vs.make_centre_pan, 'Reset']]

windows_names = ['Reset', 'Colour', 'Properties', 'Rotate', 'Zoom/Pan', 'Effects', 'Start']
windows = list(range(len(windows_names)))
buttons = list(range(len(customise_names)))

for i in range(len(buttons)):
    buttons[i] = Customise_button(customise_names[i][2], customise_names[i][0], customise_names[i][1])

for i in range(len(windows)):
    windows[i] = Customise_window(windows_names[i])
    for j in buttons:
        windows[i].add_button(j)

windows_dic = {'Reset': windows[0], 'Colour': windows[1], 'Properties': windows[2], 'Rotate': windows[3],
               'Zoom/Pan': windows[4], 'Effects': windows[5], 'Start': windows[6]}

current_window = windows_dic['Start']
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
labelscus.extend(windows_names)

video_customise = ttk.OptionMenu(stream, customise, *labelscus, command=change_mode)
video_customise.grid(column=4, row=0)

# displaying preview of stream

# 400 for big, 300 for small
stock.grid(column=0, row=0, columnspan=3, rowspan=3, sticky='nw')

vs.cap_set(stock, stock_height, stock_width)
# Tutorial section

rick_roll = ttk.Label(tutorial, text="""Guide to using this touchscreen explaining what a stream key 
is,how the process works (i.e. that they need wifi, a video and audio device connected and a valid stream key. Also will 
explain what the delay between audio/video is and why it is necessary,
along with other necessary things...""")
rick_roll.grid(column=0, row=1)

app.mainloop()