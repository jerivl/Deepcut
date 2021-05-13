# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
# 
# #beginning of comments
# movie_path = '/home/pi/Adafruit_Python_PCA9685/examples/audio.mp4'
# 
# import subprocess
# import vlc
# import multiprocessing
# from multiprocessing import Process
# import os
# 
#  #subprocess.Popen(['omxplayer',movie_path])
#  #omxp = Popen(['omxplayer',movie_path])
# 
# def play_video():
#     #process = subprocess.Popen([vlc.MediaPlayer(video_file)])
#     #media = vlc.MediaPlayer(video_file)
#     #media.play()
#     os.system('vlc /home/pi/Adafruit_Python_PCA9685/examples/audio.mp4 --play-and-exit')
# 
# import os
# 
# def run_process(process):
#     os.system('python {}'.format(process))
# 
# def move_arms():
#     os.system("python move_arms.py")
#     
# def run(x):
#     os.system(x)
# 
# if __name__ == '__main__':
#     print("wehere")
#     p = multiprocessing.Pool(2)
#     processes = ['python /home/pi/Adafruit_Python_PCA9685/examples/move_arms.py',
#                  'python /home/pi/Adafruit_Python_PCA9685/examples/PlayVideo.py']
#     p.map(run,processes)

#import subprocess
#import vlc
import multiprocessing
from multiprocessing import Process
import os
from ReceiveFinal import receiveRapFile
from cv2 import VideoCapture, CAP_PROP_FPS, CAP_PROP_FRAME_COUNT
from PIL import Image, ImageTk

def run(x):
    os.system(x)
    
def getMP4Length(x):
    cap = VideoCapture(x)
    fps = cap.get(CAP_PROP_FPS)      # OpenCV2 version 2 used "CV_CAP_PROP_FPS"
    frame_count = int(cap.get(CAP_PROP_FRAME_COUNT))
    cap.release()
    duration = frame_count/fps
    return duration





if __name__ == '__main__':
    
    while True:
        
        
        
        movie_path = '/home/pi/Adafruit_Python_PCA9685/examples/audio.mp4'
        bpm = 100
        duration = getMP4Length(movie_path)
        
        print("wehere")
        p = multiprocessing.Pool(2)
        processes = ['python /home/pi/Adafruit_Python_PCA9685/examples/move_arms.py %f %d' % (duration, bpm),
                     'python /home/pi/Adafruit_Python_PCA9685/examples/PlayVideo.py']
        p.map(run,processes)




