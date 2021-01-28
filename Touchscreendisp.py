from tkinter import *
from tkinter import messagebox, _setit
from PIL import Image, ImageTk
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


app = Tk()

app.title('Streaming on a prayer')
app.geometry('480x320')  # swap to fullscreen when using touchscreen
app.configure(bg='black')

# app.attributes('-fullscreen',True)

# Setting up windows for application (main menu, settings, stream)
main_menu = Frame(app, bg='black')
settings = Frame(app, bg='black')
stream = Frame(app, bg='black')
tutorial = Frame(app, bg='black')
wifi_login = Frame(app, bg='black')

# setting up main menu
main_menu.pack(padx=1, pady=1, expand=True, fill=BOTH)


# Changing from main menu to settings screen
def change_settings():
    main_menu.pack_forget()
    settings.pack(padx=0, pady=0, expand=True, fill=BOTH)
    # Insert code to check whether the user is connected to the internet


# Changing from main menu to stream screen
def change_stream():
    main_menu.pack_forget()
    stream.pack(padx=0, pady=0, expand=True, fill=BOTH)


# main menu to tutorial screen
def change_tutorial():
    main_menu.pack_forget()
    tutorial.pack(padx=0, pady=0, expand=TRUE, fill=BOTH)
    
# settings to wifi login    
def change_wifi():
    settings.pack_forget()
    wifi_login.pack(padx=0, pady=0, expand=TRUE, fill=BOTH)
    
# wifi login to settings
def back_settings():
    wifi_login.pack_forget()
    settings.pack(padx=0, pady=0, expand=TRUE, fill=BOTH)


# Main menu display (three buttons directing user to settings and then streaming)--------------------------------------

# need to add diocese of durham + durham uni logos
# (use PIL and copy resizing process used for arrows below to make your life easier [or I can add them in if you want])

main_menu.grid_rowconfigure((1, 2, 3), weight=2)
main_menu.grid_rowconfigure(0, weight=3)
main_menu.grid_columnconfigure((0, 1, 2), weight=1)

# Adding buttons for going to the three windows
set_btn = Button(main_menu, text="Settings", command=change_settings, font='14', bg='white')
set_btn.grid(column=1, row=1)

stream_btn = Button(main_menu, text="Stream", command=change_stream, font='14', bg='white')
stream_btn.grid(column=1, row=2)

tutorial_btn = Button(main_menu, text="Tutorial", command=change_tutorial, font='14', bg='white')
tutorial_btn.grid(column=1, row=3)

Menu_lbl = Label(main_menu, text="Main Menu", font='17', fg='white', bg='grey40')
Menu_lbl.grid(column=0, row=0, sticky='nesw', columnspan=3)

# Settings display------------------------------------------------------------------------------------------------------

# Configuring grid layout for settings window
settings.grid_columnconfigure(0, weight=1)
settings.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)
settings.grid_rowconfigure(7, weight=2)

# Code for Wifi connection
wifi_label = Label(settings, text='Wifi', bg='grey60', font=('bold', '12'))
wifi_label.grid(column=0, row=0, sticky='nesw')
wifi_connected = Label(settings, text='Unconnected', bg='grey60')
wifi_connected.grid(column=1, row=0, sticky='nesw')

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

wifi_login.grid_rowconfigure((0,1,2,3), weight = 1)
wifi_login.grid_columnconfigure((0,1), weight = 1)

saved_lbl = Label(wifi_login, text='Saved Networks', )
saved_lbl.grid(column=0,row=0, sticky='nesw')

saved_networks = ['Placeholder']
current_network = StringVar()
current_network.set('Placeholder')

saved_menu = OptionMenu(wifi_login, current_network, *saved_networks)
saved_menu.grid(column=1,row=0, sticky='nesw')

username_lbl = Label(wifi_login, text='Username:')
username_lbl.grid(column=0, row=1, sticky='nesw')

username_entr = Entry(wifi_login)
username_entr.grid(column=1, row=1, sticky='nesw')

password_lbl = Label(wifi_login, text='Password:')
password_lbl.grid(column=0, row=2, sticky='nesw')

password_entr = Entry(wifi_login)
password_entr.grid(column=1, row=2, sticky='nesw')

back_btn = Button(wifi_login, text='back', command=back_settings)
back_btn.grid(column=0, row=3, sticky='nesw')

connect_btn = Button(wifi_login, text='Connect (and save)')
connect_btn.grid(column=1, row=3, sticky='nesw')

#Settings frame--------------------------------------------------------------------------------------

wifi_button = Button(settings, text='Connect', command=change_wifi)
wifi_button.grid(column=2, row=0, sticky='nesw')

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
stream_label = Label(settings, text='Current stream code:', bg='grey60', font=('bold', '12'))
stream_label.grid(column=0, row=1, sticky='nesw')
current_code = Label(settings, text=current_codetext, bg='grey60')
current_code.grid(column=1, row=1, sticky='nesw', columnspan=2)

# user to input stream key
stream_inputlabel = Label(settings, text='Enter new stream code:', bg='grey60', font=('bold', '12'))
stream_inputlabel.grid(column=0, row=2, sticky='nesw')
stream_code = Entry(settings)
stream_code.grid(column=1, row=2, sticky='nesw')
stream_enter = Button(settings, text='Use code', command=enter_code)
stream_enter.grid(column=2, row=2, sticky='nesw')

# User to choose stream key (should appear in order of last used)
stream_p_label = Label(settings, text="Previous stream codes:", bg='grey60', font=('bold', 12))
stream_p_label.grid(column=0, row=3, sticky='nesw')
value = StringVar()
value.set(current_codetext)  # Setting the key (should be last key used)
existing_codes = OptionMenu(settings, value, *code_list)
existing_codes.grid(column=1, row=3, sticky='nesw')
stream_p_enter = Button(settings, text="Use code", command=change_code)
stream_p_enter.grid(column=2, row=3, sticky='nesw')

# Clearing list of stream codes
clear_label = Label(settings, text='Clear saved stream codes:', bg='grey60', font=('bold', 12))
clear_label.grid(column=0, row=4, sticky='nesw')
clr_lbl_bck = Label(settings, text='', bg='grey60')
clr_lbl_bck.grid(column=1, row=4, columnspan=2, sticky='nesw')
clear_button = Button(settings, text='Clear codes', command=clear_code)
clear_button.grid(column=1, row=4, columnspan=2)

# Allow stream w_out audio?
chk_state = IntVar()
chk_state.set(False)
audio_chklbl = Label(settings, text='Allow streaming without audio:', bg='grey60', font=('bold', '12'))
audio_chklbl.grid(column=0, row=5, sticky='nesw')
audio_chk = Checkbutton(settings, var=chk_state, bg='grey60')
audio_chk.grid(column=1, row=5, sticky='nesw', columnspan=2)

# Code for delay_option
delay_lbl = Label(settings, text="Audio-video delay (Milliseconds)", bg='grey60', font=('bold', '12'))
delay_lbl.grid(column=0, row=6, sticky='nesw')
BckLbl = Label(settings, text='', bg='grey60')
BckLbl.grid(column=1, row=6, sticky='nesw', columnspan=2)
var = DoubleVar(value=200)  # initial value
delay = Spinbox(settings, from_=-5000, to=5000, increment=20, textvariable=var)
delay.grid(column=1, row=6, columnspan=2)


# return to main_menu

def main_return():
    settings.pack_forget()
    main_menu.pack(padx=1, pady=1, expand=True, fill=BOTH)


# Button to deal with return to main menu
main_menur = Button(settings, text="Main menu", command=main_return)
main_menur.grid(column=0, row=7, columnspan=3, rowspan=2)

# Stream display--------------------------------------------------------------------------------------------------------

stream.grid_rowconfigure(0, weight=4)
stream.grid_columnconfigure(0, weight=4)


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
go_btn = Button(stream, text='Go', command=start_stream, bg='green')
go_btn.grid(column=1, row=1, sticky='nesw')

# Buttons for panning on screen
arrow_width = 75
arrow_height = 60

# Buttons for panning up and down

updown = Frame(stream, bg='black')

# Setting up frame for up/down arrows
updown.grid(column=1, row=0, sticky='nesw')
updown.columnconfigure(0, weight=1)
updown.rowconfigure((0, 1), weight=1)

uparrow = Image.open("//home//pi//touchscreen//Touchscreen_photos//UpArrow.png")  # needs to be whatever your directory is

# adjusting up arrow size
up_per = (arrow_width / float(uparrow.size[0]))
height = int((float(uparrow.size[1]) * float(up_per)))
uparrow = uparrow.resize((arrow_width, height))
uparrowrender = ImageTk.PhotoImage(uparrow)

up_arr = Button(updown, image=uparrowrender, bg='black', highlightthickness=0)
up_arr.image = uparrowrender
up_arr.grid(column=0, row=0)

downarrow = Image.open("//home//pi//touchscreen//Touchscreen_photos//DownArrow.png")  # needs to be whatever your directory is

# adjusting down arrow size
down_per = (arrow_width / float(downarrow.size[0]))
height = int((float(downarrow.size[1]) * float(down_per)))
downarrow = downarrow.resize((arrow_width, height))
downarrowrender = ImageTk.PhotoImage(downarrow)

down_arr = Button(updown, image=downarrowrender, bg='black', highlightthickness=0)
down_arr.image = downarrowrender
down_arr.grid(column=0, row=1)

# buttons for panning left/right

# Setting up frame for left/right arrows
leftright = Frame(stream, bg='black')
leftright.grid(column=0, row=1, sticky='nesw')
leftright.grid_columnconfigure((0, 1), weight=1)
leftright.grid_rowconfigure(0, weight=1)

leftarrow = Image.open("//home//pi//touchscreen//Touchscreen_photos//LeftArrow.png")  # needs to be whatever your directory is

# adjusting left arrow size
left_per = (arrow_height / float(leftarrow.size[0]))
height = int((float(leftarrow.size[1]) * float(left_per)))
leftarrow = leftarrow.resize((arrow_height, height))
leftarrowrender = ImageTk.PhotoImage(leftarrow)
left_arr = Button(leftright, image=leftarrowrender, bg='black', highlightthickness=0)

left_arr.image = leftarrowrender
left_arr.grid(row=0, column=0)

rightarrow = Image.open("//home//pi//touchscreen//Touchscreen_photos//RightArrow.png")  # needs to be whatever your directory is

# adjusting right arrow size

right_per = (arrow_height / float(rightarrow.size[0]))
rightarrow = rightarrow.resize((arrow_height, height))
rightarrowrender = ImageTk.PhotoImage(rightarrow)
right_arr = Button(leftright, image=rightarrowrender, bg='black', highlightthickness=0)

right_arr.image = rightarrowrender
right_arr.grid(row=0, column=1)

# Sample picture (for where steam will go)

stock_height = 500
stock = Frame(stream, bg='black')
Sample_photo = Image.open("//home//pi//touchscreen//Touchscreen_photos//Crowley.jpg")  # needs to be whatever your directory is
crowley_per = stock_height / float(Sample_photo.size[0])
width = int((float(Sample_photo.size[1]) * float(crowley_per)))
Sample_photo = Sample_photo.resize((stock_height, width))
crowley = ImageTk.PhotoImage(Sample_photo)
aziraphale = Label(stock, image=crowley, bg='black')
aziraphale.image = crowley
aziraphale.pack()
stock.grid(column=0, row=0)

# Tutorial section

rick_roll = Label(tutorial, text="""Guide to using this touchscreen explaining what a stream key 
is,how the process works (i.e. that they need wifi, a video and audio device connected and a valid stream key. Also will 
explain what the delay between audio/video is and why it is necessary,
along with other necessary things...""", bg='black', foreground='white')
rick_roll.pack(fill=BOTH)

app.mainloop()
