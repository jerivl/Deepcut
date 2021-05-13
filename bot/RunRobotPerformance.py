import subprocess
import vlc
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
    
import sys
if sys.version_info[0] == 2:  # the tkinter library changed it's name from Python 2 to 3.
    import Tkinter
    tkinter = Tkinter #I decided to use a library reference to avoid potential naming conflicts with people's programs.
else:
    import tkinter

# Shows image on screen
def showPIL(pilImage):
    root = tkinter.Tk()
    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    root.overrideredirect(1)
    root.geometry("%dx%d+0+0" % (w, h))
    root.focus_set()    
    root.bind("<Escape>", lambda e: (e.widget.withdraw(), e.widget.quit()))
    canvas = tkinter.Canvas(root,width=w,height=h)
    canvas.pack()
    canvas.configure(background='black')
    imgWidth, imgHeight = pilImage.size
    if imgWidth > w or imgHeight > h:
        ratio = min(w/imgWidth, h/imgHeight)
        imgWidth = int(imgWidth*ratio)
        imgHeight = int(imgHeight*ratio)
        pilImage = pilImage.resize((imgWidth,imgHeight), Image.ANTIALIAS)
    image = ImageTk.PhotoImage(pilImage)
    imagesprite = canvas.create_image(w/2 - 50,h/2,image=image)
    root.mainloop()
    

if __name__ == '__main__':
    movie_path = '/home/pi/Adafruit_Python_PCA9685/examples/audio.mp4'
#     TODO: Make idle screen appear when the robot is receiving
#     idle_img_path = '/home/pi/Adafruit_Python_PCA9685/examples/idle.png'
#     pilImage = Image.open(idle_img_path)
#     
#     q = multiprocessing.Queue()
#     procs = []
#     p1 = Process(target=showPIL, args=(pilImage,))
#     p1.start()
#     procs.append(p1)
#     p2 = Process(target=receiveRapFile, args=(movie_path,q))    
#     p2.daemon = True
#     p2.start()
#     procs.append(p2)
#     for p in procs:
#          p.join()
#     bpm = q.get()
    bpm = receiveRapFile(movie_path)
    duration = getMP4Length(movie_path)
    
    p = multiprocessing.Pool(2)
    processes = ['python /home/pi/Adafruit_Python_PCA9685/examples/move_arms.py %f %d' % (duration, bpm),
                 'python /home/pi/Adafruit_Python_PCA9685/examples/PlayVideo.py']
    p.map(run,processes)

