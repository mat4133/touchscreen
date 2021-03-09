from threading import Thread
from os.path import expanduser
import os
import time
import datetime
from multiprocessing import Process
import subprocess
import picamera
from picamera import PiCamera


flag = 0
def STOP():
    global flag
    flag = 1

def STOP_SCREEN():
    subprocess.call('pkill -n ffmpeg', shell=True)
    try:
        t.stop()
    except:
        print("")

def STREAM_CAMERA_COMMAND(FPS, BITRATE, VIDEOBUFFER, KEY, PLATFORM, AUDIO):
    global flag
    PiCamera().close()
    camera = picamera.PiCamera(resolution=(1280, 720), framerate=FPS)
    if AUDIO == 1:
        VOLUME = 0
    elif AUDIO == 0:
        VOLUME = 256
    if PLATFORM == 1:
        STREAMURL = 'rtmp://a.rtmp.youtube.com/live2/'
    elif PLATFORM == 0:
        STREAMURL = 'rtmps://live-api-s.facebook.com:443/rtmp/'
        KEY = "\"" + str(KEY) + "\""
    print(KEY)
    stream_pipe = subprocess.Popen(
        '/home/pi/FFmpeg-n4.1.3/ffmpeg -use_wallclock_as_timestamps 1 -thread_queue_size 32K -f h264 -r ' + str(FPS) + ' -itsoffset 0 -i - -f alsa -ar 11025 -itsoffset ' + str(VIDEOBUFFER) + ' -ac 1 -thread_queue_size 32K -i pulse -use_wallclock_as_timestamps 1 -vol ' + str(VOLUME) + ' -c:a aac -async 1 -c:v libx264 -preset ultrafast -f flv -r ' + str(FPS) + ' ' + str(STREAMURL) + str(KEY),
        stdin=subprocess.PIPE, shell=True)
    if flag == 0:
        camera.framerate = FPS
        camera.vflip = True
        camera.hflip = True
        camera.rotation = 90
        camera.start_recording(stream_pipe.stdin, format='h264', bitrate=int(BITRATE))
        while True:
            if flag == 1:
                camera.stop_recording()
                camera.close()
                stream_pipe.stdin.close()
                break
            camera.wait_recording(1)
    flag = 0
    subprocess.call('pkill -n ffmpeg', shell=True)
    stream_pipe.wait()


def STREAM_SCREEN_COMMAND(FPS, BITRATE, VIDEOBUFFER, KEY, PLATFORM, AUDIO):
    if AUDIO == 1:
        VOLUME = 0
    elif AUDIO == 0:
        VOLUME = 256
    if PLATFORM == 1:
        STREAMURL = 'rtmp://a.rtmp.youtube.com/live2/'
    elif PLATFORM == 0:
        STREAMURL = 'rtmps://live-api-s.facebook.com:443/rtmp/'
        KEY = "\"" + str(KEY) + "\""
    stream_pipe = subprocess.Popen(
        '/home/pi/FFmpeg-n4.1.3/ffmpeg -use_wallclock_as_timestamps 1 -thread_queue_size 32k -f x11grab -s 330x200 -r ' + str(FPS) + ' -itsoffset 0 -i :0.0+5,35 -f alsa -use_wallclock_as_timestamps 1 -ac 1 -ar 11025 -thread_queue_size 32k -itsoffset ' + str(VIDEOBUFFER) + ' -i pulse -async 1 -c:v libx264 -c:a aac -minrate ' + str(BITRATE) + ' -pix_fmt yuv420p -qp 0 -r ' + str(FPS) + ' -vol ' + str(VOLUME) + ' -f flv "rtmps://live-api-s.facebook.com:443/rtmp/2864819093784274?s_bl=1&s_ps=1&s_psm=1&s_sw=0&s_vt=api-s&a=AbwJJqZ6dMhN7ogc"',# + str(KEY),
        stdin=subprocess.PIPE, shell=True)