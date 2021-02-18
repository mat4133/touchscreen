import time
import pickle
import cv2
from PIL import Image, ImageTk
import numpy as np
import io


cap = cv2.VideoCapture(0)

#file_name = 'saved_settings'
#settings_values = open(file_name,'rb')
#settings = pickle.load(settings_values)


#default settings
show_image = 1

settings = {'rotation':0, 'zoom':0, 'pan_horizontal':0, 'pan_vertical':0, 'colour':'Normal'}
effect_list = []

def function_maker(function, *part_args):  # takes in the function to make more of + values needed in that function
    def wraps(*extra_args):
        argument = list(part_args)
        argument.extend(extra_args)
        return function(*argument)
    return wraps
    

#brightness 0 - 99
#saturation -99 --> 99
#sharpness -99 --> 99
#contrast -99 --> 99

#to increase the slider

#to decrease the slider


#to rotate


#Modes are as follows:
'''
def awb(sliders_list, mode):
    print(mode)
    video.AWB_MODES[mode]
    display(*sliders_list)

#Effects are as follows

def motion(motion_slider):
    step = 1
    Num_images = 1
    Capture_count = 0
    thresh_percent = motion_slider.get() / 100
    threshold = 30
    resolution_height = 1080
    resolution_width = 1440
    min_pixel_change = resolution_height * resolution_width * thresh_percent
    stream = io.BytesIO()

    time.sleep(1)
    try:
        while threshold > 0:
            video.resolution = (1440,1080)
            if step == 1:
                stream.seek(0)
                video.capture(stream,'rgba',True)
                frame1 = np.fromstring(stream.getvalue(), dtype=np.uint8)
                step = 2
            if step == 2:
                stream.seek(0)
                video.capture(stream,'rgba', True)
                frame2 = np.fromstring(stream.getvalue(), dtype=np.uint8)
                step = 1
            Num_images = Num_images + 1

            if Num_images > 4:
                if Capture_count <= 0:
                    frame_diff = np.abs(frame1-frame2)

    except:
        print('stuff went wrong')
        GPI0.cleanup()
        exit()

    finally:
        video.close()
        print('Motion detecter terminated')
'''

def make_normal(*args):
    global settings, effect_list
    effect_list = []
    settings['colour'] = 'Normal'

def make_grey(*args):
    settings['colour'] = 'Grey'

def make_blur(*args):
    effect_list.append('Blur')
    try:
        effect_list.remove('Sharpen')
    except ValueError:
        print('Sharpen not happened yet')

def make_bright(*args):
    effect_list.append('Bright')
    try:
        effect_list.remove('Dark')
    except ValueError:
        print('Dark not happened yet')

def make_dark(*args):
    effect_list.append('Dark')
    try:
        effect_list.remove('Bright')
    except ValueError:
        print('Dark not happened yet')


def make_edge_detection(*args):
    effect_list.append('Edge Detection')

def make_emboss(*args):
    effect_list.append('Emboss')

def make_sharpen(*args):
    effect_list.append('Sharpen')
    try:
        effect_list.remove('Blur')
    except ValueError:
        print('Blur not happened yet')

def make_sepia(*args):
    settings['colour'] = 'Sepia'

def make_zoom_in():
    settings['zoom'] += 10

def make_zoom_out():
    settings['zoom'] -= 10

def make_pan_right():
    settings['pan_horizontal'] += 10

def make_pan_left():
    settings['pan_horizontal'] -= 10

def make_pan_up():
    settings['pan_vertical'] += 10

def make_pan_down():
    settings['pan_vertical'] -= 10

def make_clockwise_rotate():
    settings['rotation'] += 1
    if settings['rotation'] == 4:
        settings['rotation'] = 0

def make_anticlockwise_rotate():
    settings['rotation'] -= 1
    if settings['rotation'] == -1:
        settings['rotation'] = 3

def make_show_image():
    global show_image
    if show_image == 0:
        show_image = 1
    elif show_image == 1:
        show_image = 0


def show_frame(video_frame, height, width):
    global show_image, settings, effect_list
    _, frame = cap.read()
    cv2image = cv2.flip(frame, 1)
    zoom = settings['zoom']
    pan_horizontal = settings['pan_horizontal']
    pan_vertical = settings['pan_vertical']
    rotation = settings['rotation']
    if show_image == 1:
        for effect in effect_list:
            cv2image = effects(effect, cv2image)
        if settings['zoom'] != 0:
            cv2image = cv2image[int(zoom - pan_vertical):int((480-zoom) - pan_vertical), int(1.33333*(zoom + pan_horizontal)):int(640-(1.33333*(zoom - pan_horizontal)))]
        #if rotation != 0:
            #cv2image = cv2.rotate(cv2image, rotateCode=(rotation - 1))
        if ('Emboss' not in effect_list) and ('Edge Detection' not in effect_list):
            cv2image = effects(settings['colour'], cv2image)
        img = Image.fromarray(cv2image)
    elif show_image == 0:
        img = Image.open("/home/pi/Nothing_To_see.jpg")
    '''
    if int(float(img.size[0]) / float(img.size[1])) < int(4 / 3):
        hsize = int((float(img.size[1]) / float(width / float(img.size[0]))))
        wsize = int(hsize * float(3 / 4))
    else:
        hsize = int((float(img.size[1]) * float(width / float(img.size[0]))))
        wsize = width
    '''
    wsize = width
    hsize = height
    img = img.resize((int(wsize), int(hsize)), Image.ANTIALIAS)
    imgtk = ImageTk.PhotoImage(image=img)
    video_frame.imgtk = imgtk
    video_frame.configure(image=imgtk)
    frame_show = function_maker(show_frame, video_frame, height, width)
    video_frame.after(5, frame_show)

def effects(effect_input, frame):
    effect = {'Normal': cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA),
              'Grey': cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY),
              'Blur': cv2.GaussianBlur(frame, (15, 15), 0),
              'Bright': cv2.convertScaleAbs(frame, beta=100),
              'Dark': cv2.convertScaleAbs(frame, beta=-50),
              'Edge Detection': cv2.Canny(frame, 100, 100),
              'Emboss': cv2.filter2D(frame, -1, np.array([[0, -1, -1], [1, 0, -1], [1, 1, 0]])),
              'Sharpen': cv2.filter2D(frame, -1, np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])),
              'Sepia': cv2.filter2D(frame, -1,
                                    np.array([[0.272, 0.534, 0.131], [0.349, 0.686, 0.168], [0.393, 0.769, 0.189]]))}
    return effect[effect_input]