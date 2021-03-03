from threading import Thread
from os.path import expanduser
import os
import time
import datetime
from multiprocessing import Process
import subprocess
import picamera
from picamera import PiCamera


def STREAM_CAMERA_COMMAND():
    PiCamera().close()
    camera = picamera.PiCamera(resolution=(1280, 720), framerate=30)
    stream_pipe = subprocess.Popen(
        "ffmpeg -use_wallclock_as_timestamps 1 -y -xerror -thread_queue_size 32K -f h264 -r 30 -itsoffset 0 -i - -f alsa -use_wallclock_as_timestamps 1 -ar 11025 -itsoffset 7 -async 1 -ac 1 -thread_queue_size 32K -i pulse -c:a aac -b:a 32k -async 1 -c:v copy -f flv -flags:v +global_header -rtmp_buffer 10000 -r 30 -async 1 rtmp://a.rtmp.youtube.com/live2/q1t6-jpmu-52bc-3yhy-be2a",
        stdin=subprocess.PIPE, shell=True)
    try:
        camera.framerate = 30
        camera.vflip = True
        camera.hflip = True
        camera.rotation = 90
        camera.start_recording(stream_pipe.stdin, format='h264', bitrate=6000000)
        while True:
            camera.wait_recording(1)
    except KeyboardInterrupt:
        camera.stop_recording()
        camera.close()
        stream_pipe.stdin.close()
        stream_pipe.wait()


def STREAM_SCREEN_COMMAND():
    stream_pipe = subprocess.Popen(
        "ffmpeg -f x11grab -s 330x200 -framerate 30 -i :0.0+5,35 -f alsa -ac 2 -i pulse -c:v libx264 -preset ultrafast -qp 0 -pix_fmt yuv420p -g 60 -f flv rtmp://a.rtmp.youtube.com/live2/q1t6-jpmu-52bc-3yhy-be2a",
        stdin=subprocess.PIPE, shell=True)


def STOP():
    subprocess.call('pkill -n ffmpeg', shell=True)
    try:
        t.stop()

    except:
        print("")

