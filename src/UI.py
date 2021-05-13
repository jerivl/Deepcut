"""
    Modification History:
        Date: 5/05/2021
        Time: 8:00PM
    Description:
        User Interface for the robot. It will allow the user to input their desire lyrics and choose
        what beat, mode, BPM, and syllable length for their rap. The user is also able to increase
        and decrease the volume of the rap.
        There are 2 buttons. The play button will get all of the input and sent it to the computer
        to be compiled into rap. It will call a terminal command to other python scripts with the
        desire input of the user. The second button will be a quit button for the user to exit
        the interface.
    User Inputs:
        Lyrics: This will be in the form of a text box
        BPM: Slider that the user will be able to move to their chosen BPM with an incrementation of 5.
            Range: 60 to 200 and set at 100
        Syllable Length: Slider that user will move to their desired syllable length with an incrementation of 0.01.
            Range: 0.1 to 1.0 and set at 0.5
        Beats: A drop down with choices from 1 to 3, so the user can chose what beat they would like to use
        Mode: A drop down with the choices of 1 to 5. The user will chose was mode they would like to choose
    Current Outputs:
        file path of output rap video
    Errors/Warnings to work on:
        Change line 52 to a different script file/location
    NOTES:
        If output line/frame is not needed then delete that have to do anything with output or out
"""
import tkinter as tk
from tkinter import Text
import os
from pathlib import Path
from SendFinal import sendRPI
 

root = tk.Tk()
root.title("Deepcut")
root.geometry("600x300")


class Test(Text):
    def __init__(self, master, **kw):
        Text.__init__(self, master, **kw)
        self.bind('<Control-c>', self.copy)
        self.bind('<Control-x>', self.cut)
        self.bind('<Control-v>', self.paste)

    def copy(self, event=None):
        self.clipboard_clear()
        text = self.get("sel.first", "sel.last")
        self.clipboard_append(text)

    def cut(self, event):
        self.copy()
        self.delete("sel.first", "sel.last")

    def paste(self, event):
        text = self.selection_get(selection='CLIPBOARD')
        self.insert('insert', text)


def remover(inLyrics):
    # split by spaces
    words = inLyrics.split(' ')
    outLyrics = ''
    for w in range(len(words)):
        word = words[w].strip()
        if not word.isalpha():
            new_word = ''
            for c in range(len(word)):
                if word[c].isalpha():
                    new_word = new_word + word[c]
            word = new_word
        outLyrics = outLyrics + word + ' '
    
    return outLyrics


def detector(inLyrics):
    words = inLyrics.split(' ')
    invalid = 0
    w = 0
    while not invalid and w < len(words):
        word = words[w].strip()
        if not word.isalpha():
            invalid = 1
        w = w + 1
    
    return invalid


# Displays all of the choices that the user inputs
def get_entry():
    audioTitle = titleInput.get()
    lyrics = userInput.get()
    chosenBeat = beatsVar.get()
    chosenMode = modeVar.get()
    bpm = bpmSlider.get()
    syllableLength = syllableSlider.get()
    volume = volumeSlider.get()
    beatMode = int(chosenBeat[-1])
    mode = int(chosenMode[-1])

    # Input validation
    secret_code = "MAKE ME RAP "
    if audioTitle[0:12] in secret_code and len(audioTitle) > 12:
        # Input is a speech file
        audio_file = Path(audioTitle[12:len(audioTitle)])
        extension = audio_file.suffix
        # Check if file exists
        if not Path.is_file(audio_file) or extension != '.wav':
            error_message = 'The full path specified for the audio file does not exist or is not a .wav file'
            output.config(text=error_message)
        else:
            # Check if transcript has any special characters
            if detector(lyrics):
                error_message = 'The lyrics specified for the audio file contain special characters or numbers'
                output.config(text=error_message)
            else:
                # Run rap generation
                # print('Run')
                cmd = 'python GenerateRap_UserSpeech.py "%s" "%s" %d %d %d %f %f' % (str(audio_file), lyrics, mode, beatMode, bpm, syllableLength, volume)
                os.system(cmd)
                with open('output.txt','r') as out_txt:
                    output_file = out_txt.read()
                output.config(text=output_file)
                sendRPI(output_file)
    else:
        # Input is rap lyrics
        # Check if transcript has any special characters
        lyrics = remover(lyrics)
        print(lyrics)
        title = audioTitle.replace(" ", "_")
        # Run rap generation
        # print('Run')
        cmd = 'python GenerateRap.py "%s" "%s" %d %d %d %f %f' % (title, lyrics, mode, beatMode, bpm, syllableLength, volume)
        os.system(cmd)
        with open('output.txt','r') as out_txt:
            output_file = out_txt.read()
        output.config(text=output_file)
        sendRPI(output_file)
        

    # add command here add user input as arguements for other scripts
    # Change path for script
    #os.system('python C:\\Deepcut\\testing\\Issue2_GetPhonemeList.py audioTitle lyrics mode beatMode bpm syllableLength')

    # make a variable to store path
    # output.config(text=pathLocation)

    # output.config(text=audioTitle + " "
    #                    + lyrics + " "
    #                    + str(beatMode) + " "
    #                    + str(mode) + " "
    #                    + str(bpm) + " "
    #                    + str(syllableLength) + " "
    #                    + str(volumeSlider.get()))


# Make space for the window
# Frames initialization
instructionFrame = tk.Frame(root)
titleFrame = tk.Frame(root, padx=5, pady=5)
inputFrame = tk.Frame(root, padx=5, pady=5)
outputFrame = tk.Frame(root, padx=5)
leftFrame = tk.Frame(root, padx=25, pady=10)
centerFrame = tk.Frame(root, padx=25, pady=10)
rightFrame = tk.Frame(root, padx=25, pady=10)
buttonFrame = tk.Frame(root, padx=25, pady=10)

# Instructions
instructions = tk.Label(instructionFrame, text='Welcome! Enter lyrics (no special characters or numbers) into the box below')
instructions.pack()

# Title name input
titleLabel = tk.Label(titleFrame, width=10, text="Rap Title")
titleInput = tk.Entry(titleFrame)
titleInput.focus()
titleInput.bind("<Return>", get_entry)
titleLabel.pack(side=tk.LEFT, padx=5, pady=5)
titleInput.pack(side=tk.LEFT, expand=tk.YES, fill=tk.X)

# Input LABEL and ENTRY box
inputLabel = tk.Label(inputFrame, width=10, text="Input")
userInput = tk.Entry(inputFrame)
userInput.focus()
userInput.bind("<Return>", get_entry)
inputLabel.pack(side=tk.LEFT, padx=5, pady=5)
userInput.pack(side=tk.LEFT, expand=tk.YES, fill=tk.X)

# Output LABEL and ENTRY box
outputLabel = tk.Label(outputFrame, width=10, text="Output")
output = tk.Label(outputFrame, text=" ")
outputLabel.pack(side=tk.LEFT, padx=5, pady=5)
output.pack(side=tk.LEFT, expand=tk.YES, fill=tk.X)

# Drop down for beats
beatsOptions = ["Beat 1", "Beat 2", "Beat 3"]
beatsVar = tk.StringVar(root)
beatsVar.set("Beat Options")
beatsDrop = tk.OptionMenu(leftFrame, beatsVar, *beatsOptions)
beatsDrop.config(width=15)
beatsDrop.pack(pady=10)

# Drop down for the modes
modeOptions = ["Flow 1", "Flow 2", "Flow 3", "Flow 4", "Flow 5"]
modeVar = tk.StringVar(root)
modeVar.set("Mode Options")
modeDrop = tk.OptionMenu(leftFrame, modeVar, *modeOptions)
modeDrop.config(width=15)
modeDrop.pack(pady=10)

# BPM slider
bpmLabel = tk.Label(centerFrame, width=10, text="BPM")
bpmSlider = tk.Scale(centerFrame, orient='horizontal', from_=60, to=200, resolution=5)
bpmSlider.set(100)
bpmLabel.pack()
bpmSlider.pack(pady=2.5)

# Syllable length slider
syllableLabel = tk.Label(centerFrame, width=15, text="Syllable Length")
syllableSlider = tk.Scale(centerFrame, orient='horizontal', from_=0.1, to=1.0, resolution=0.01)
syllableSlider.set(0.5)
syllableLabel.pack()
syllableSlider.pack(pady=2.5)

# Volume Slider
volumeLabel = tk.Label(rightFrame, width=15, text="Volume")
volumeSlider = tk.Scale(rightFrame, orient='vertical', from_=5.0, to=0.0, resolution=0.1)
volumeSlider.set(2.0)
volumeLabel.pack()
volumeSlider.pack()

# Code for the button
playButton = tk.Button(buttonFrame, text="Play", command=get_entry)
# playButton = tk.Button(buttonFrame, text="Play")
playButton.pack(pady=5)

quitButton = tk.Button(buttonFrame, text="Quit", command=root.destroy)
quitButton.pack(pady=5)

# Pack all frames
instructionFrame.pack()
titleFrame.pack(side=tk.TOP, fill=tk.X)
inputFrame.pack(side=tk.TOP, fill=tk.X)
outputFrame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
leftFrame.pack(side=tk.LEFT)
centerFrame.pack(side=tk.LEFT)
rightFrame.pack(side=tk.LEFT)
buttonFrame.pack(side=tk.LEFT)

# copy and paste
copyPaste = Test(root)
copyPaste.pack(fill='both', expand=1)

root.mainloop()

