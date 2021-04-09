"""
    Modification History:
        Date: 3/16/2021
        Time: 6:00PM
    Description:
        Will extract the phonemes from a TextGrid file and change them into
        syllables using the ARPABET dictionary. Two functions will be used
        to do this process. First function, get_phoneme, will get all of the
        phonemes and their timings from the TextGrid file into arrays. The second
        function, phoneme_to_syllables, will convert the set of phonemes into
        syllables. The syllabifier package will be used for the conversion.
        The syllable codes and syllable timings are saved.
    Current inputs:
        TextGrid File
    Current output:
        Size of the phoneme interval
        Output all of the phonemes from the phoneme intervals.
    NOTES:
        The code only works iff all TextGrid files are formatted the same as the current input
        Currently using Anaconda interpreter in base/root environment
        Packages Downloaded:
            Download the packages via cmd or anaconda cmd
            ARPABET dictionary: https://github.com/vgautam/arpabet-syllabifier/blob/master/tests/tmp.ipynb
            Textgrid Tool: https://github.com/kylebgorman/textgrid
                CMD download: pip install TextGrid
"""

# importing pyglet module
import pyglet

def play_video(video_file):
    # width / height of window 
    width = 720
    height = 720

    # creating a window 
    title = "demo"
    window = pyglet.window.Window(width, height, title) 

    # video path
    vidPath ="facetest.mp4"
    # creating a media player object
    player = pyglet.media.Player()
    source = pyglet.media.StreamingSource()
    MediaLoad = pyglet.media.load(vidPath)
    # add this media in the queue
    player.queue(MediaLoad)
    # play the video
    player.play()

    # on draw event
    @window.event
    def on_draw():
        
        # clea the window
        window.clear()
        
        # if player sorce exist
        # and video format exist
        if player.source and player.source.video_format:
            
            # get the texture of video and
            # make surface to display on the screen
            player.get_texture().blit(0, 0)
            
            
    # # key press event     
    # @window.event 
    # def on_key_press(symbol, modifier): 
    #     # key "p" get press 
    #     if symbol == pyglet.window.key.P: 
    #         # pause the video
    #         player.pause()
            
    #         # printing message
    #         print("Video is paused")
            
    #     # key "r" get press 
    #     if symbol == pyglet.window.key.R: 
    #         # resume the video
    #         player.play()
    #         # printing message
    #         print("Video is resumed")
            
    # run the pyglet application
    pyglet.app.run()
