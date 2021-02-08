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

def display(Brightness_slider, Saturation_slider, Contrast_slider, Sharpness_slider):
    video.preview_fullscreen = False
    video.preview_window = (0,0,100,100) #Where the window should go
    video.video_stabilization = True
    video.brightness = Brightness_slider.get()
    video.contrast = Contrast_slider.get()
    video.saturation = Saturation_slider.get()
    video.sharpness = Sharpness_slider.get()

#brightness 0 - 99
#saturation -99 --> 99
#sharpness -99 --> 99
#contrast -99 --> 99

#to increase the slider
def slider_increase(slider, sliders_list):
    if slider.name == "Brightness":
        parameter = video.brightness
    elif slider.name == "Contrast":
        parameter = video.contrast
    elif slider.name == "Saturation":
        parameter = video.saturation
    elif slider.name == "Sharpness":
        parameter = video.sharpness
    else:
        print('parameter error')
    if parameter > (slider.max-5):
        parameter += 5
    else:
        parameter = max
    slider.set(parameter)
    display(*sliders_list)

#to decrease the slider
def slider_decrease(slider,sliders_list):
    if slider == "Brightness":
        parameter = video.brightness
    elif slider == "Contrast":
        parameter = video.contrast
    elif slider == "Saturation":
        parameter = video.saturation
    elif slider == "Sharpness":
        parameter = video.sharpness
    else:
        print('parameter error')
    if parameter < (slider.min+5):
        parameter -= 5
    else:
        parameter = min
    slider.set()
    display(*sliders_list)

#to rotate
def rotate_clock(sliders_list):
    video.rotation += 90
    display(*sliders_list)

def rotate_anticlock(sliders_list):
    video.rotation -= 90
    display(*sliders_list)

#zooming in/out
def zoom_in():
    #need to work out how the zoom function works here
    print('test tommorow')

def zoom_out():
    #need to work out how the zoom function works for this
    print('test tommorow')

#Modes are as follows:

def awb(mode, sliders_list):
    video.AWB_MODES[mode]
    display(*sliders_list)

#Effects are as follows

def effects(effect, sliders_list):
    effect.image_effect = effect
    display(*sliders_list)

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





