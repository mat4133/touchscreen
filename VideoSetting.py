import time
import picamera
import RPi.GPIO as GPIO
import numpy as np
import io

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, GPIO.PUD_UP)

video = picamera.PICamera()

#default settings
zoom = 1
preview_Time = 3
awb_counter = 0
effect_num = 0
operation = 1
Image_num = 1
Count_capture = 0
Sav_num = 0

def display(Brightness_slider,Saturation_slider,Contrast_slider):
    video.preview_fullscreen = False
    video.preview_window = (0,0,100,100) #Where the window should go
    video.video_stabilization = True
    video.brightness = Brightness_slider.get()
    video.contrast = Contrast_slider.get()
    video.saturation = Saturation_slider.get()


#brightness 0 - 99
#saturation -99 --> 99
#sharpness -99 --> 99
#contrast -99 --> 99

#to increase the slider
def slider_increase(slider, max):
    if video.brightness < (max-5):
        video.brightness += 5
    else:
        video.brightness = max
    slider.set()
    display()

#to decrease the slider
def slider_decrease(slider, min):
    if (video.brightness+5) > min:
        video.brightness -= 5
    else:
        video.brightness = min
    slider.set()
    display()

#to rotate
def rotate(Rotation_Label):
    video.rotation += 90
    display()


#zooming in/out
def zoom_in():
    #need to work out how the zoom function works here
    print('test tommorow')

def zoom_out():
    #need to work out how the zoom function works for this
    print('test tommorow')

#Modes are as follows:

def awb(mode):
    video.AWB_MODES[mode]
    display()

#Effects are as follows

def effects(effect):
    effect.image_effect = effect
    display()


#function to detect motion

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





