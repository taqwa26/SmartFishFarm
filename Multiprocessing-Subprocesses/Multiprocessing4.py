import subprocess
import multiprocessing
import time

def ffmpeg():
    pipeline = 'ffmpeg -f v4l2 -framerate 25 -video_size 640x480 -i /dev/video0 -t 15 dokumentasiVideo.mp4 -y'
    p = subprocess.Popen(pipeline, shell=True, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    out = p.communicate()[0]

proc = multiprocessing.Process(target=ffmpeg)
proc.start()
#print('rekam')
#time.sleep(5)
#print('stop')
for i in range (5):
    print('rekam')
    time.sleep(1)
proc.terminate()
exit()
