from tkinter import *
from tkinter import messagebox, _setit, ttk
from PIL import Image, ImageTk
from ttkthemes import ThemedStyle
from Keyboard import create_keyboard, keyboard_on
import pickle
import os

audio_connection = 0
video_connection = 0

# The following code should:
# Produce a touchscreen display with 3 windows: main menu, settings, and stream

# In the section stream:
# user to be able to start/stop stream
# user to be able to pan to focus on parts of the stream
# user to be warned if they try to stream w_out:
#   internet
#   valid stream key
#   audio and video devices connected

# In the settings:
# user to input a stream key which is then saved (and accessable on future uses of device)
# user to connect to wifi (and likewise have this saved to be done automatically)
# user to add it in a delay between audio and video (and likewise have this be saved)
# user to select whether streaming with/without audio is possible

# This application should boot up upon turning the power on the pi (needs to be configured within the pi you are using
# more work needs to be done)

# Possible other options that to investigate:
# Displaying current battery life
# Displaying the devices connected (if more than one are connected the user could choose between them???)
# Adding in a helpful tutorial explainig how this works from the main menu section
# Having it so that the user can download the os system for the pi with everything already set up
# (possibly by copying an already set up os onto an SD card,not too sure how to do this but would be useful)
# Turning off the screen after 5 minutes (like sleep mode or something to save battery)
# Potentially add in HDMI output


# SITA (i have removed the connection between the wifi button and anything so it calls nothing (and hence won't cause it
# to crash when you run it)

screen_size = 1 #to switch between 320x240, and 480x320 (0 is 320x240)

app = Tk()

app.title('Streaming on a prayer')
if screen_size == 0:
    app.geometry('320x240')  # swap to fullscreen when using touchscreen
else:
    app.geometry('480x320')

#initializing style
style = ThemedStyle(app)
style.set_theme("equilux")

#background colour from theme equilux
bg = style.lookup('TFrame', 'background')
fg = style.lookup('TFrame', 'foreground')
app.configure(bg=style.lookup('TFrame', 'background'))

# app.attributes('-fullscreen',True)

# Setting up windows for application (main menu, settings, stream)
settings = Frame(app)
settings.configure(bg=style.lookup('TFrame', 'background'))
stream = Frame(app)
stream.configure(bg=style.lookup('TFrame', 'background'))
tutorial = Frame(app)
tutorial.configure(bg=style.lookup('TFrame', 'background'))
wifi_login = Frame(app)
wifi_login.configure(bg=style.lookup('TFrame', 'background'))

# setting up main menu
stream.pack(padx=0, pady=0, expand=True, fill=BOTH)

# Changing from stream to settings screen
def change_settings():
    stream.pack_forget()
    settings.pack(padx=0, pady=0, expand=True, fill=BOTH)

def back_tutorial():
    tutorial.pack_forget()
    stream.pack(padx=0, pady=0, expand=True, fill=BOTH)

# stream to tutorial screen
def change_tutorial():
    stream.pack_forget()
    tutorial.pack(padx=0, pady=0, expand=TRUE, fill=BOTH)
    
# settings to wifi login    
def change_wifi():
    settings.pack_forget()
    wifi_login.pack(padx=0, pady=0, expand=TRUE, fill=BOTH)
    
# wifi login to settings
def back_settings():
    wifi_login.pack_forget()
    settings.pack(padx=0, pady=0, expand=TRUE, fill=BOTH)

# Main menu display (now removed)--------------------------------------------------------------------------------------

# need to add diocese of durham + durham uni logos
# (use PIL and copy resizing process used for arrows below to make your life easier [or I can add them in if you want])

"""
main_menu.grid_rowconfigure((1, 2, 3), weight=2)
main_menu.grid_rowconfigure(0, weight=3)
main_menu.grid_columnconfigure((0, 1, 2), weight=1)
"""

# Adding buttons for going to the three windows
set_btn = ttk.Button(stream, text="SETTINGS", command=change_settings)
set_btn.grid(column=0, row=0, sticky='nesw')

"""
stream_btn = ttk.Button(main_menu, text="STREAM", command=change_stream)
stream_btn.grid(column=1, row=2)
"""

tutorial_btn = ttk.Button(stream, text="TUTORIAL", command=change_tutorial)
tutorial_btn.grid(column=1, row=0, sticky='nesw')

"""
Menu_lbl = ttk.Label(stream, text="MAIN MENU")
Menu_lbl.grid(column=1, row=0)
"""

# Settings display------------------------------------------------------------------------------------------------------

# Configuring grid layout for settings window
settings.grid_columnconfigure(0, weight=2)
settings.grid_columnconfigure((1,2), weight=1)
settings.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)
settings.grid_rowconfigure(7, weight=2)

# Code for Wifi connection
wifi_label = ttk.Label(settings, text='WiFi')
wifi_label.grid(column=0, row=0)
wifi_connected = ttk.Label(settings, text='Unconnected')
wifi_connected.grid(column=1, row=0)

# Wifi login and code ----------------------------------------------------------------------

#DONT UNCOMMENT THIS (or it will not work)
''' 
wifi_storage = 'wifi_storage'

sample_wifi_list = {'network1':'GNU'}

stored_network = open(wifi_storage, 'wb')
pickle.dump(sample_wifi_list,stored_network)
stored_network.close()

stored_network1 = open(wifi_storage, 'rb')
saved_networks = pickle.load(stored_network1)
stored_network1.close()

def wifi_connect():
    try:
        os.system('sudo ifconfig wlan0 up')
        command = 'sudo iwconfig wlan0 essid' + username_entr.get() + 'key s:' + password_entr.get()
        os.system(command)
        os.system('sudo dhclient wlan0')
    except:
        messagebox.showwarning('Either: wrong username/password or wrong type of network (still working on WPA/WPA2)')

'''

def username_space_wifi(*args):
    back_btn.grid_forget()
    connect_btn.grid_forget()
    password_lbl.grid_forget()
    password_entr.grid_forget()
    keyboard_on(keyboard_frame2.children['!frame'])

def username_keyboard_off(current_frame):
    current_frame.grid_forget()
    keyboard_frame2.grid_forget()
    back_btn.grid(column=0, row=3)
    connect_btn.grid(column=1, row=3)
    password_lbl.grid(column=0, row=2)
    password_entr.grid(column=1, row=2)

def password_space_wifi(*args):
    back_btn.grid_forget()
    connect_btn.grid_forget()
    username_entr.grid_forget()
    username_lbl.grid_forget()
    password_entr.grid(column=1, row=1)
    password_lbl.grid(column=0, row=1)
    keyboard_on(keyboard_frame3.children['!frame'])

def password_keyboard_off(current_frame):
    current_frame.grid_forget()
    keyboard_frame3.grid_forget()
    password_entr.grid(column=1, row=2)
    password_lbl.grid(column=0,row=2)
    username_entr.grid(column=1, row=1)
    username_lbl.grid(column=0, row=1)
    back_btn.grid(column=0, row=3)
    connect_btn.grid(column=1, row=3)

wifi_login.grid_rowconfigure((0,1,2,3), weight = 1)
wifi_login.grid_columnconfigure((0,1), weight = 1)

saved_lbl = ttk.Label(wifi_login, text='SAVED NETWORKS', )
saved_lbl.grid(column=0,row=0)

saved_networks = ['Placeholder']
current_network = StringVar()
current_network.set('Placeholder')

saved_menu = ttk.OptionMenu(wifi_login, current_network, *saved_networks)
saved_menu.grid(column=1,row=0)

username_lbl = ttk.Label(wifi_login, text='USERNAME:')
username_lbl.grid(column=0, row=1)

username_text = StringVar()
username_entr = ttk.Entry(wifi_login, textvariable = username_text )
username_entr.grid(column=1, row=1)
username_entr.bind("<Button>", username_space_wifi)

password_lbl = ttk.Label(wifi_login, text='PASSWORD:')
password_lbl.grid(column=0, row=2)

password_text = StringVar()
password_entr = ttk.Entry(wifi_login, textvariable = password_text)
password_entr.grid(column=1, row=2)
password_entr.bind("<Button>", password_space_wifi)

back_btn = ttk.Button(wifi_login, text='BACK', command=back_settings)
back_btn.grid(column=0, row=3)

connect_btn = ttk.Button(wifi_login, text='CONNECT / SAVE')
connect_btn.grid(column=1, row=3)

keyboard_frame2 = Frame(wifi_login)
keyboard_frame2.configure(bg=style.lookup('TFrame', 'background'))
keyboard_frame2.grid(column=0, row=2, columnspan=2, rowspan=2)
keyboard_frame2.rowconfigure(0,weight=1)
keyboard_frame2.columnconfigure(0,weight=1)

keyboard_frame2 = create_keyboard(keyboard_frame2, username_entr, username_text, style, username_keyboard_off)

keyboard_frame3 = Frame(wifi_login)
keyboard_frame3.configure(bg=style.lookup('TFrame', 'background'))
keyboard_frame3.grid(column=0, row=2, columnspan=2, rowspan=2)
keyboard_frame3.rowconfigure(0, weight=1)
keyboard_frame3.columnconfigure(0, weight=1)

keyboard_frame3 = create_keyboard(keyboard_frame3, password_entr, password_text, style, password_keyboard_off)

#Settings frame--------------------------------------------------------------------------------------

wifi_button = ttk.Button(settings, text='Connect', command=change_wifi)
wifi_button.grid(column=2, row=0)

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
    main_menur.grid_forget()

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
    main_menur.grid(column=0, row=7, columnspan=3, rowspan=2)

# user to input stream key
stream_inputlabel = ttk.Label(settings, text='Enter key:')
stream_inputlabel.grid(column=0, row=2)
stream_text = StringVar()
stream_code = ttk.Entry(settings, textvariable=stream_text)
stream_code.bind("<Button>",keyboard_space_settings)
stream_code.grid(column=1, row=2)
stream_enter = ttk.Button(settings, text='Use key', command=enter_code)
stream_enter.grid(column=2, row=2)

keyboard_frame1 = Frame(settings)
keyboard_frame1.configure(bg=style.lookup('TFrame', 'background'))
keyboard_frame1.grid(column=0, row=4, columnspan=3, rowspan=4)
keyboard_frame1.rowconfigure(0, weight=1)
keyboard_frame1.columnconfigure(0, weight=1)

keyboard_frame1 = create_keyboard(keyboard_frame1,stream_code,stream_text,style,reset_page)

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
chk_state = IntVar()
chk_state.set(False)
audio_chklbl = ttk.Label(settings, text='Audioless streaming:')
audio_chklbl.grid(column=0, row=5)
audio_chk = ttk.Checkbutton(settings, var=chk_state)
audio_chk.grid(column=1, row=5, columnspan=2)

# Code for delay_option
delay_lbl = ttk.Label(settings, text="Audio-video delay:")
delay_lbl.grid(column=0, row=6)
BckLbl = ttk.Label(settings, text='')
BckLbl.grid(column=1, row=6, columnspan=2)
var = DoubleVar(value=200)  # initial value
delay = ttk.Spinbox(settings, from_=-5000, to=5000, increment=20, textvariable=var)
delay.grid(column=1, row=6, columnspan=2)


# return to main_menu

def stream_return():
    settings.pack_forget()
    stream.pack(padx=1, pady=1, expand=True, fill=BOTH)


# Button to deal with return to main menu
main_menur = ttk.Button(settings, text="Stream", command=stream_return)
main_menur.grid(column=0, row=7, columnspan=3, rowspan=2)

# Stream display--------------------------------------------------------------------------------------------------------

stream.grid_rowconfigure((0,3), weight=2)
stream.grid_rowconfigure((1,2), weight=3)
stream.grid_columnconfigure((0,1), weight=1)
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
        #
        #
        #
        #
        #


def stop_stream():
    # insert code for stopping stream here
    #
    #
    #
    #
    #
    go_btn.configure(text='Go', bg='green', command=start_stream)


# Go button
go_btn = ttk.Button(stream, text='Go', command=start_stream)
go_btn.grid(column=2, row=3)

# Button to deal with return to main menu from stream screen
#main_menur = ttk.Button(stream, text="Main menu", command=main_return)
#main_menur.grid(column=1, row=1)

# Buttons for panning on screen

#60 and 50 for big screen

if screen_size == 0:
    arrow_width = 40
    arrow_height = 40
else:
    arrow_width = 60
    arrow_height = 50


# Setting up frame for up/down arrows

uparrow = Image.open("\\Users\\Matthew Scholar\\PycharmProjects\\touchscreen-main\\Touchscreen_photos\\UpArrow.png")  # needs to be whatever your directory is

# adjusting up arrow size
up_per = (arrow_width / float(uparrow.size[0]))
height = int((float(uparrow.size[1]) * float(up_per)))
uparrow = uparrow.resize((arrow_width, height))
uparrowrender = ImageTk.PhotoImage(uparrow)

up_arr = ttk.Button(stream, image=uparrowrender)
up_arr.image = uparrowrender
up_arr.grid(column=2, row=1)

downarrow = Image.open("\\Users\\Matthew Scholar\\PycharmProjects\\touchscreen-main\\Touchscreen_photos\\DownArrow.png")  # needs to be whatever your directory is

# adjusting down arrow size
down_per = (arrow_width / float(downarrow.size[0]))
height = int((float(downarrow.size[1]) * float(down_per)))
downarrow = downarrow.resize((arrow_width, height))
downarrowrender = ImageTk.PhotoImage(downarrow)

down_arr = ttk.Button(stream, image=downarrowrender)
down_arr.image = downarrowrender
down_arr.grid(column=2, row=2)

# buttons for panning left/right

# Setting up frame for left/right arrows

leftarrow = Image.open("\\Users\\Matthew Scholar\\PycharmProjects\\touchscreen-main\\Touchscreen_photos\\LeftArrow.png")  # needs to be whatever your directory is

# adjusting left arrow size
left_per = (arrow_height / float(leftarrow.size[0]))
height = int((float(leftarrow.size[1]) * float(left_per)))
leftarrow = leftarrow.resize((arrow_height, height))
leftarrowrender = ImageTk.PhotoImage(leftarrow)
left_arr = ttk.Button(stream, image=leftarrowrender)

left_arr.image = leftarrowrender
left_arr.grid(row=3, column=0)

rightarrow = Image.open("\\Users\\Matthew Scholar\\PycharmProjects\\touchscreen-main\\Touchscreen_photos\\RightArrow.png")  # needs to be whatever your directory is

# adjusting right arrow size

right_per = (arrow_height / float(rightarrow.size[0]))
rightarrow = rightarrow.resize((arrow_height, height))
rightarrowrender = ImageTk.PhotoImage(rightarrow)
right_arr = ttk.Button(stream, image=rightarrowrender)

right_arr.image = rightarrowrender
right_arr.grid(row=3, column=1)

# Sample picture (for where steam will go)

#400 for big, 300 for small
if screen_size == 0:
    stock_height = 300
else:
    stock_height = 400

stock = Frame(stream, bg=style.lookup('TFrame', 'background'))
Sample_photo = Image.open("\\Users\\Matthew Scholar\\PycharmProjects\\touchscreen-main\\Touchscreen_photos\\Crowley.jpg")  # needs to be whatever your directory is
crowley_per = stock_height / float(Sample_photo.size[0])
width = int((float(Sample_photo.size[1]) * float(crowley_per)))
Sample_photo = Sample_photo.resize((stock_height, width))
crowley = ImageTk.PhotoImage(Sample_photo)
aziraphale = Label(stock, image=crowley, bg='#484848')
aziraphale.image = crowley
aziraphale.pack()
stock.grid(column=0, row=1, columnspan=2, rowspan=2)

# Tutorial section

rick_roll = ttk.Label(tutorial, text="""Guide to using this touchscreen explaining what a stream key 
is,how the process works (i.e. that they need wifi, a video and audio device connected and a valid stream key. Also will 
explain what the delay between audio/video is and why it is necessary,
along with other necessary things...""")
rick_roll.pack(fill=BOTH)

stream_btn = ttk.Button(tutorial, text="Stream",command=back_tutorial)
stream_btn.pack()

# Button to deal with return to main menu from tutorial screen
#main_menur = ttk.Button(tutorial, text="Main menu", command=main_return)
#main_menur.grid(column=1, row=1)

app.mainloop()
