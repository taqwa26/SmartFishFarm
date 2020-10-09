import os
import sys

os.system('ffmpeg -f v4l2 -framerate 25 -video_size 640x480 -i /dev/video0 dokumentasiVideo.mp4 -y')

if x==10:
    sys.exit()
    pritn('gagal')
    exit()