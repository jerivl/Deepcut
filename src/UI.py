"""
    Modification History:
        Date: 4/30/2021
        Time: 9:15PM
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
        Beats: A drop down with choices from 1 to 4, so the user can chose what beat they would like to use
        Mode: A drop down with the choices of 1 to 4. The user will chose was mode they would like to choose
    Current Outputs:
        String of all of the inputs from the user and Issue2_GetPhonemesList.py (not in UI window)
    Errors/Warnings to work on:
        Change line 52 to a different script file/location
    NOTES:
        If output line/frame is not needed then delete that have to do anything with output or out
"""
import tkinter as tk
import os

root = tk.Tk()
root.title("Deepcut")
root.geometry("600x300")


# Displays all of the choices that the user inputs
def get_entry():
    audioTitle = titleInput.get()
    lyrics = userInput.get()
    chosenBeat = beatsVar.get()
    chosenMode = modeVar.get()
    bpm = bpmSlider.get()
    syllableLength = syllableSlider.get()
    beatMode = int(chosenBeat[-1])
    mode = int(chosenMode[-1])

    # add command here add user input as arguements for other scripts
    # Change path for script
    #os.system('python C:\\Deepcut\\testing\\Issue2_GetPhonemeList.py audioTitle lyrics mode beatMode bpm syllableLength')

    # make a variable to store path
    # output.config(text=pathLocation)

    output.config(text=audioTitle + " "
                       + lyrics + " "
                       + str(beatMode) + " "
                       + str(mode) + " "
                       + str(bpm) + " "
                       + str(syllableLength) + " "
                       + str(volumeSlider.get()))


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
instructions = tk.Label(instructionFrame, text='Welcome! Enter lyrics (no special characters) into the box below')
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

root.mainloop()
