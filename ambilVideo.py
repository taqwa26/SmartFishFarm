# skript ini untuk mabil video seluruh kolam jik adiminta
import os

os.system('ffmpeg -f v4l2 -framerate 25 -video_size 640x480 -i /dev/video0 -t 5 dokumentasiVideo.mp4 -y')
#waktu menyesuaikan kolam yang diberi pakan