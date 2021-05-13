# importing pyglet module
# import pyglet
# 
# def play_video(video_file):
#     # width / height of window 
#     width = 720
#     height = 720
# 
#     # creating a window 
#     title = "demo"
#     window = pyglet.window.Window(width, height, title) 
# 
#     # video path
#     vidPath ="done.mp4"
#     # creating a media player object
#     player = pyglet.media.Player()
#     source = pyglet.media.StreamingSource()
#     MediaLoad = pyglet.media.load(vidPath)
#     # add this media in the queue
#     player.queue(MediaLoad)
#     # play the video
#     player.play()
# 
#     # on draw event
#     @window.event
#     def on_draw():
#         
#         # clea the window
#         window.clear()
#         
#         # if player sorce exist
#         # and video format exist
#         if player.source and player.source.video_format:
#             
#             # get the texture of video and
#             # make surface to display on the screen
#             player.get_texture().blit(0, 0)
#             
#             
#     # # key press event     
#     # @window.event 
#     # def on_key_press(symbol, modifier): 
#     #     # key "p" get press 
#     #     if symbol == pyglet.window.key.P: 
#     #         # pause the video
#     #         player.pause()
#             
#     #         # printing message
#     #         print("Video is paused")
#             
#     #     # key "r" get press 
#     #     if symbol == pyglet.window.key.R: 
#     #         # resume the video
#     #         player.play()
#     #         # printing message
#     #         print("Video is resumed")
#             
#     # run the pyglet application
#     pyglet.app.run()
#beginning of comments
movie_path = '/home/pi/Adafruit_Python_PCA9685/examples/audio.mp4'

import subprocess
#import vlc
import multiprocessing
from multiprocessing import Process
import os

 #subprocess.Popen(['omxplayer',movie_path])
 #omxp = Popen(['omxplayer',movie_path])

#def play_video(video_file):
    #process = subprocess.Popen([vlc.MediaPlayer(video_file)])
    #media = vlc.MediaPlayer(video_file)
    #media.play()
#os.system('vlc /home/pi/Adafruit_Python_PCA9685/examples/audio.mp4 --play-and-exit')
os.system('omxplayer /home/pi/Adafruit_Python_PCA9685/examples/audio.mp4 --aspect-mode stretch --nodeinterlace --vol 1000')

