import time
import pickle
import cv2
from PIL import Image, ImageTk
import numpy as np
import io

cascPath = 'haarcascade_frontalface_default.xml'
facecascade = cv2.CascadeClassifier(cascPath)

input_width = 1280
input_height = 720
input_ratio = input_width/input_height

#file_name = 'saved_settings'
#settings_values = open(file_name,'rb')
#settings = pickle.load(settings_values)

#default settings
show_image = 1

settings = {'rotation': 0, 'top_offset': 0, 'bottom_offset': 0, 'left_offset': 0, 'right_offset': 0, 'colour':'Normal'}
last_change = np.array([0, input_height, 0, input_width]) #format is top bottom left right
effect_list = []
face_effects = []

def reduce_zoom(positions):
    print('OG positions', positions)
    acceptable_vzoom = 20
    acceptable_hzoom = acceptable_vzoom*input_ratio
    positions = np.array(positions)
    proposed_change = []
    for i in range(len(positions)):
        proposed_change.append(positions[i]-last_change[i])
    print(proposed_change)
    top_ratio = abs(proposed_change[0])/(abs(proposed_change[0])+abs(proposed_change[1]))
    bottom_ratio = 1 - top_ratio
    left_ratio = abs(proposed_change[2])/abs((proposed_change[2])+abs(proposed_change[3]))
    right_ratio = 1 - left_ratio
    ratio_list = [top_ratio, bottom_ratio, left_ratio, right_ratio]
    print(ratio_list)
    for i in range(len(positions)):
        if i >= 2:
            multiplier = input_ratio
        else:
            multiplier = 1
        if abs(positions[i] - last_change[i]) <= 10:
            positions[i] = last_change[i]
        elif positions[i] - last_change[i] > 10:
            positions[i] = int(last_change[i] + 9 * multiplier*ratio_list[i])
            last_change[i] = positions[i]
        elif positions[i] - last_change[i] < -10:
            positions[i] = int(last_change[i] - 9 * multiplier*ratio_list[i])
            last_change[i] = positions[i]
    print('New positions', list(positions))
    return list(positions)


def face_focus(faces):
    image_height = faces[0][3]
    extended_height = image_height * 1.5
    top_position = int(faces[0][1] + image_height * 0.5 - extended_height / 2)
    bottom_position = int(faces[0][1] + 0.5 * image_height + extended_height / 2)
    right_position = int(faces[0][0] + 0.5 * (image_height + extended_height * input_ratio))
    left_position = int(faces[0][0] + 0.5 * (image_height - extended_height * input_ratio))
    return [top_position,bottom_position, left_position, right_position]

def face_stuff(cv2image, face_effects):
    if len(face_effects) > 0:
        grey = cv2.cvtColor(cv2image, cv2.COLOR_BGR2GRAY)
        detected_faces = facecascade.detectMultiScale(grey, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        if 'Face detection' in face_effects:
            for (x, y, w, h) in detected_faces:
                cv2.rectangle(cv2image, (x, y), (x + w, y + h), (0, 200, 0), 4)
        if 'Motion Tracker' in face_effects:
            if len(detected_faces) == 1:
                positions = face_focus(detected_faces)
                positions = reduce_zoom(positions)
                cv2image = cv2image[positions[0]:positions[1], positions[2]:positions[3]]
            else:
                top_offset = settings['top_offset']
                bottom_offset = settings['bottom_offset']
                left_offset = settings['left_offset']
                right_offset = settings['right_offset']
                bottom_position = int(input_height - bottom_offset)
                top_position = int(top_offset)
                left_position = int(input_ratio * (left_offset))
                right_position = int(input_width - (input_ratio * (right_offset)))
                positions = [top_position, bottom_position, left_position, right_position]
                positions = reduce_zoom(positions)
                cv2image = cv2image[positions[0]:positions[1], positions[2]:positions[3]]
        if 'Autofocus' in face_effects:
            if len(detected_faces) == 1:
                positions = face_focus(detected_faces)
        return cv2image
    else:
        return cv2image

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
    face_effects = []
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
    #problem cross over zoom
    settings['left_offset'] += 10
    settings['right_offset'] += 10
    settings['top_offset'] += 10
    settings['bottom_offset'] += 10

def make_zoom_out():
    if settings['left_offset'] <=0 and settings['right_offset'] <=0:
        print('max_size')
    elif settings['left_offset'] <= 0:
        settings['right_offset'] -= 20
        settings['right_offset'] = max(settings['right_offset'], 0)
    elif settings['right_offset'] <=0:
        settings['left_offset'] -= 20
        settings['left_offset'] = max(settings['left_offset'], 0)
    else:
        settings['left_offset'] -= 10
        settings['right_offset'] -= 10
    if settings['top_offset'] <=0 and settings['bottom_offset'] <=0:
        print('max size')
    elif settings['top_offset'] <= 0:
        settings['bottom_offset'] -= 20
        settings['bottom_offset'] = max(settings['bottom_offset'], 0)
    elif settings['bottom_offset'] <= 0:
        settings['top_offset'] -= 20
        settings['top_offset'] = max(settings['top_offset'], 0)
    else:
        settings['top_offset'] -= 10
        settings['bottom_offset'] -= 10

def make_pan_right():
    if settings['right_offset']:
        settings['right_offset'] -= 10
        settings['left_offset'] += 10

def make_pan_left():
    if settings['left_offset'] >= 10:
        settings['right_offset'] += 10
        settings['left_offset'] -= 10


def make_pan_up():
    if settings['top_offset'] >= 10:
        settings['top_offset'] -= 10
        settings['bottom_offset'] += 10

def make_pan_down():
    if settings['bottom_offset'] >= 10:
        settings['top_offset'] += 10
        settings['bottom_offset'] -= 10

def make_clockwise_rotate():
    settings['rotation'] += 1
    if settings['rotation'] == 4:
        settings['rotation'] = 0

def make_anticlockwise_rotate():
    settings['rotation'] -= 1
    if settings['rotation'] == -1:
        settings['rotation'] = 3

def detect_face():
    face_effects.append('Face detection')

def motion_tracker():
    face_effects.append('Motion Tracker')

def auto_focus():
    face_effects.append('Autofocus')

def make_show_image():
    global show_image
    if show_image == 0:
        show_image = 1
    elif show_image == 1:
        show_image = 0


def show_frame(video_frame, height, width, cap):
    global show_image, settings, effect_list, last_change
    _, frame = cap.read()
    cv2image = cv2.flip(frame, 1)
    #zoom = settings['zoom']
    top_offset = settings['top_offset']
    bottom_offset = settings['bottom_offset']
    left_offset = settings['left_offset']
    right_offset = settings['right_offset']
    rotation = settings['rotation']
    if show_image == 1:
        for effect in effect_list:
            if effect != 'Face detection' and effect != 'Motion Tracker':
                cv2image = effects(effect, cv2image)
        #if settings['top_offset'] != 0 or settings['bottom_offset'] != 0 or settings['left_offset'] != 0 or settings['right_offset'] != 0:
        if 'Motion Tracker' not in face_effects:
            bottom_position = int(input_height-bottom_offset)
            top_position = int(top_offset)
            left_position = int(input_ratio*(left_offset))
            right_position = int(input_width-(input_ratio*(right_offset)))
            positions = [top_position, bottom_position, left_position, right_position]
            cv2image = cv2image[positions[0]:positions[1], positions[2]:positions[3]]
            last_change = [positions[0], positions[1], positions[2], positions[3]]
        #if rotation != 0:
            #cv2image = cv2.rotate(cv2image, rotateCode=(rotation - 1))
        if ('Emboss' not in effect_list) and ('Edge Detection' not in effect_list):
            cv2image = effects(settings['colour'], cv2image)
    elif show_image == 0:
        img = Image.open("/home/pi/Nothing_To_see.jpg")
    cv2image = face_stuff(cv2image, face_effects)
    img = Image.fromarray(cv2image)
    wsize = width
    hsize = height
    img = img.resize((int(wsize), int(hsize)), Image.ANTIALIAS)
    imgtk = ImageTk.PhotoImage(image=img)
    video_frame.imgtk = imgtk
    video_frame.configure(image=imgtk)
    frame_show = function_maker(show_frame, video_frame, height, width, cap)
    video_frame.after(2, frame_show)

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