import time
import pickle
import cv2
from PIL import Image, ImageTk
import numpy as np
import io

cascPath = 'haarcascade_frontalface_default.xml'
facecascade = cv2.CascadeClassifier(cascPath)

input_width = 640
input_height = 480
input_ratio = input_width/input_height

cap = cv2.VideoCapture(0)

#file_name = 'saved_settings'
#settings_values = open(file_name,'rb')
#settings = pickle.load(settings_values)

#default settings
show_image = 1
brightness = 0
check = 1
check_2 = 0

settings = {'rotation': 3, 'top_offset': 0, 'bottom_offset': 0, 'left_offset': 0, 'right_offset': 0}
last_change = np.array([0, input_height, 0, input_width]) #format is top bottom left right

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
    positions[0] = max(0, positions[0])
    positions[1] = min(input_height, positions[1])
    positions[2] = max(0, positions[2])
    positions[3] = min(input_width, positions[3])
    return list(positions)


def face_focus(faces,zoom):
    image_height = faces[0][3]
    extended_height = image_height * zoom
    top_position = max(int(faces[0][1] + image_height * 0.5 - extended_height / 2), 0)
    bottom_position = min(int(faces[0][1] + 0.5 * image_height + extended_height / 2), input_height)
    right_position = min(int(faces[0][0] + 0.5 * (image_height + extended_height * input_ratio)), input_width)
    left_position = max(int(faces[0][0] + 0.5 * (image_height - extended_height * input_ratio)), 0)
    return [top_position,bottom_position, left_position, right_position]

def face_stuff(cv2image):
    global show_image
    if show_image >= 10:
        grey = cv2.cvtColor(cv2image, cv2.COLOR_BGR2GRAY)
        detected_faces = facecascade.detectMultiScale(grey, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        if show_image == 11:
            for (x, y, w, h) in detected_faces:
                cv2.rectangle(cv2image, (x, y), (x + w, y + h), (0, 200, 0), 4)
        if show_image == 12:
            if len(detected_faces) == 1:
                positions = face_focus(detected_faces, 1.5)
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
        if show_image == 13:
            if len(detected_faces) == 1:
                positions = face_focus(detected_faces, 1.2)
                face = cv2image[positions[0]:positions[1], positions[2]:positions[3]]
                focused_face = cv2.filter2D(face, -1, np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]]))
                blurred_face = cv2.GaussianBlur(cv2image, (35, 35), 0)
                blurred_face[positions[0]:positions[1], positions[2]:positions[3]] = focused_face
                cv2image = blurred_face
        return cv2image
    else:
        return cv2image

def function_maker(function, *part_args):  # takes in the function to make more of + values needed in that function
    def wraps(*extra_args):
        argument = list(part_args)
        argument.extend(extra_args)
        return function(*argument)
    return wraps

def make_full_reset(*args):
    global show_image, brightness, settings
    settings['top_offset'] = 0
    settings['bottom_offset'] = 0
    settings['left_offset'] = 0
    settings['right_offset'] = 0
    settings['rotation'] = 3
    brightness = 0
    show_image = 1

def make_colour_reset(*args):
    global show_image
    show_image = 1

def make_brightness_reset(*args):
    global brightness
    brightness = 0

def make_zoom_reset(*args):
    global settings
    settings['top_offset'] = 0
    settings['bottom_offset'] = 0
    settings['left_offset'] = 0
    settings['right_offset'] = 0

def make_pan_centre(*args):
    global settings
    difference = settings['bottom_offset'] + settings['top_offset']
    settings['top_offset'] = int(difference/2)
    settings['bottom_offset'] = int(difference/2)
    settings['left_offset'] = int(difference/2)
    settings['right_offset'] = int(difference/2)

def make_grey(*args):
    global show_image
    show_image = 2

def make_blur(*args):
    global show_image
    show_image = 3

def make_bright(*args):
    global brightness
    brightness = brightness + 25

def make_dark(*args):
    global brightness
    brightness = brightness - 25

def make_edge_detection(*args):
    global show_image
    show_image = 6

def make_emboss(*args):
    global show_image
    show_image = 7

def make_sharpen(*args):
    global show_image
    show_image = 8

def make_sepia(*args):
    global show_image
    show_image = 9

def make_zoom_in():
    pot_hos_diff = (input_width-(settings['right_offset']+10)*input_ratio) - settings['left_offset']*input_ratio
    pot_vert_diff = input_height-settings['bottom_offset'] - settings['top_offset']
    if pot_hos_diff > 20 and pot_vert_diff > 20:
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
    global check, check_2
    check = 0
    check_2 = 0
    settings['rotation'] += 1
    if settings['rotation'] == 4:
        settings['rotation'] = 0

def make_anticlockwise_rotate():
    global check, check_2
    check = 0
    check_2 = 0
    settings['rotation'] -= 1
    if settings['rotation'] == -1:
        settings['rotation'] = 3

def detect_face():
    global show_image
    show_image = 11

def motion_tracker():
    global show_image
    show_image = 12

def auto_focus():
    global show_image
    show_image = 13

def make_show_image():
    global show_image
    if show_image == 0:
        show_image = 1
    elif show_image == 1:
        show_image = 0

def cap_set(video_frame, height, width):
    cap.set(3,input_height)
    cap.set(4,input_width)
    show_frame(video_frame, height, width)

def rotate():
    global check
    if check == 0:
        check = 1
        cap.set(4,input_height)
        cap.set(3,input_width)

def rotate2():
    global check_2
    if check_2 == 0:
        check_2 = 1
        cap.set(3,input_height)
        cap.set(4,input_width)

def show_frame(video_frame, height, width):
    global show_image, settings, last_change, brightness
    top_offset = settings['top_offset']
    bottom_offset = settings['bottom_offset']
    left_offset = settings['left_offset']
    right_offset = settings['right_offset']
    rotation = settings['rotation']
    _, frame = cap.read()
    cv2image = cv2.rotate(frame, rotateCode=2)
    #if show_image == 0:
    #    img = Image.open("/home/pi/Nothing_To_See.jpeg")
    if show_image == 1:
        # Make Normal
        cv2image = cv2.cvtColor(cv2image, cv2.COLOR_BGR2RGBA)
    elif show_image == 2:
        # Make Grey
        cv2image = cv2.cvtColor(cv2image, cv2.COLOR_BGR2GRAY)
    elif show_image == 3:
        # Blur
        cv2image = cv2.GaussianBlur(cv2image, (15, 15), 0)
        cv2image = cv2.cvtColor(cv2image, cv2.COLOR_BGR2RGBA)
    elif show_image == 6:
        # Edge Detection
        cv2image = cv2.Canny(cv2image, 100, 100)
    elif show_image == 7:
        # Emboss
        cv2image = cv2.filter2D(cv2image, -1, np.array([[0, -1, -1], [1, 0, -1], [1, 1, 0]]))
    elif show_image == 8:
        # Sharpen
        cv2image = cv2.filter2D(cv2image, -1, np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]]))
        cv2image = cv2.cvtColor(cv2image, cv2.COLOR_BGR2RGBA)
    elif show_image == 9:
        # Sepia
        cv2image = cv2.filter2D(cv2image, -1, np.array([[0.272, 0.534, 0.131], [0.349, 0.686, 0.168], [0.393, 0.769, 0.189]]))
    elif show_image >=10:
        cv2image = face_stuff(cv2image)
        cv2image = cv2.cvtColor(cv2image, cv2.COLOR_BGR2RGBA)
    #elif show_image == 0:
        #img = Image.open("/home/pi/Nothing_To_see.jpg")
    if settings['top_offset'] != 0 or settings['bottom_offset'] != 0 or settings['left_offset'] != 0 or settings['right_offset'] != 0:
        bottom_position = int(input_height-bottom_offset)
        top_position = int(top_offset)
        left_position = int(1.33333*(left_offset))
        right_position = int(input_width-(1.33333*(right_offset)))
        cv2image = cv2image[top_position:bottom_position, left_position:right_position]
    if rotation == 1:
        rotate2()
        cv2image = cv2.rotate(cv2image, rotateCode=rotation)
    if rotation == 3:
        rotate2()
    if rotation == 0 or rotation == 2:
        rotate()
        cv2image = cv2.rotate(cv2image, rotateCode=rotation)
    cv2image = cv2.convertScaleAbs(cv2image, beta=brightness)
    img = Image.fromarray(cv2image)
    wsize = width
    hsize = height
    img = img.resize((int(wsize), int(hsize)), Image.ANTIALIAS)
    imgtk = ImageTk.PhotoImage(image=img)
    video_frame.imgtk = imgtk
    video_frame.configure(image=imgtk)
    frame_show = function_maker(show_frame, video_frame, height, width)
    video_frame.after(1, frame_show)

def stop_view():
    time.sleep(0.5)
    cap.release()

def start_view():
    time.sleep(1)
    cap.open(0)
    make_full_reset()