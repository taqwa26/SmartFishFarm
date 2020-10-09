import shlex
import time
from subprocess import Popen, DEVNULL, STDOUT

pipeline = 'ffmpeg -f v4l2 -framerate 25 -video_size 640x480 -i /dev/video0 -t 15 dokumentasiVideo.mp4 -y'

p = Popen(shlex.split(pipeline), stdin=DEVNULL, stdout=DEVNULL, stderr=STDOUT)
# call p.terminate() any time you like, to terminate the ffmpeg process

for i in range (10):
    print('rekam')
    time.sleep(1)
p.terminate()