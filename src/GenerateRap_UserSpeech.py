"""
    Modification History:
        Date: 4/30/2021
        Time: 10:00PM
    Description:
        Generate rap (vocal, video, and movements) from input speech audio.
        Combines Forced alignment (Montreal Forced Aligner)
        and syllabifier in series [see aligner_to_rap] to perform speech to rap transformation.
        Then face movement is generated in MATLAB before video and audio is encoded to a final video file.
    Current inputs:
        Audio file (string).
        Lyrics (string),
        Flow choice (int)
        Beats per minute (bpm),
        Syllable length wrt subdivision sylLen (float),
        Beat choice (int)
        Volume (float)
        Flowtron/Waveglow model + config + inference script,
    Current output:
        Rap with beat and face 
    NOTES:
        Packages Downloaded (non-exaustive list):
            Flowtron (https://github.com/nvidia/flowtron)
            Nvidia Apex (https://github.com/nvidia/apex)
            Waveglow (https://github.com/nvidia/waveglow)
            Montreal forced aligner (see pypy distribution)
            FFMPEG with h264 (libx264)
            MATLAB
"""

import os, sys
from pathlib import Path
from AlignerOutputToSyllableAudio import aligner_to_rap
import matlab.engine
import numpy as np
import argparse

if __name__ == "__main__":
    # Create the parser
    my_parser = argparse.ArgumentParser(description='Convert speech into rap')

    # Add the arguments
    my_parser.add_argument('File', metavar='file', type=str, help='Path to file of user speech (.wav)')
    my_parser.add_argument('Text', metavar='text', type=str, help='Lyrics of speech file (transcript)')
    my_parser.add_argument('Method', metavar='flow', type=int, help='Flow choice (int 1-5)')
    my_parser.add_argument('Beat', metavar='beat', type=int, help='Beat choice (int 1-3)')
    my_parser.add_argument('BPM', metavar='bpm', type=int, help='Beats per minute of rap (60 <= bpm <= 200)')
    my_parser.add_argument('SylLen', metavar='sylLen', type=float, help='Syllable length relative to the subdivision length (0 < sylLen <= 1)')
    my_parser.add_argument('Volume', metavar='volume', type=float, help='Volume of output audio (0 <= vol <= 5)')

    # Execute parse_args()
    args = my_parser.parse_args()
    audio_file = Path(args.file)
    text = args.Text
    method = args.Method
    beat_num = args.Beat
    bpm = args.BPM
    sylLen = args.SylLen
    title = audio_file.stem
    volume = args.Volume

    # Input validation
    if not Path.is_file(audio_file):
        print('The path specified for the audio file does not exist')
        sys.exit()
    if method < 1 or method > 5:
        print('The flow choice is invalid. The flow choice will be 1.')
        method = 1
    if beat_num < 1 or beat_num > 3:
        print('The beat choice is invalid. The beat choice will be 1.')
        beat_num = 1
    if bpm < 60 or bpm > 200:
        print('The bpm is invalid. The bpm will be 100.')
        bpm = 100
    if sylLen <= 0 or sylLen > 1:
        print('The syllable length is invalid. The syllable length will be 0.75.')
        sylLen = 0.75
    if volume < 0 or volume > 5:
        print('The volume choice is invalid. The volume will be 5.0.')
        volume = 5.0
    
    volume = volume/5

    text_input = text.strip()
    wav_list = []
    textgrid_list = []


    # Set variables for mfa
    corpus_path = (Path.cwd().parent).joinpath("MFA",title)
    if not os.path.isdir(corpus_path):
        os.mkdir(corpus_path)
    wav_flowtron = audio_file
    resampled = (Path.cwd().parent).joinpath("results","temp_r.wav")
    wav = (Path.cwd().parent).joinpath("MFA",title ,title + ".wav")
    transcript = (Path.cwd().parent).joinpath("MFA",title ,title + ".txt")
    textgrid_path = (Path.cwd().parent).joinpath("MFA",title,title + ".TextGrid")
    if os.path.isdir(textgrid_path):
        cmd = "rm %s/*" % (textgrid_path)
        print(cmd)
        os.system(cmd)
        cmd = "rmdir %s/" % (textgrid_path)
        print(cmd)
        os.system(cmd)
        cmd = "rm %s/*" % (corpus_path)
        print(cmd)
        os.system(cmd)
        log_folder = "/home/deepcut/Documents/MFA/%s" % (title + "_" + str(text_pnt))
        cmd = "rm -rf %s/*" % (log_folder)
        print(cmd)
        os.system(cmd)

    dictionary_path = (Path.cwd().parent).joinpath("resource","librispeech-lexicon.txt")

    # Write transcript
    with open(transcript,'w') as out_txt:
        out_txt.write(text_input)

    # Resample audio
    cmd = "sox %s -b 16 -r 16000 %s" % (wav_flowtron, resampled)
    os.system(cmd)
    os.system("mv %s %s" % (resampled,wav))

    # Get phoneme timings
    cmd = "mfa align -v %s %s english %s " % (corpus_path, dictionary_path, textgrid_path)
    print(cmd)
    os.system(cmd)

    wav_list.append(wav)
    textgrid_list.append((wav.parent).joinpath(textgrid_path.name,textgrid_path.name))

    # Speech to rap transform
    save_fldr = (Path.cwd().parent).joinpath("results")
    if not os.path.isdir(save_fldr):
        os.mkdir(save_fldr)

    vocal = aligner_to_rap(wav_list, textgrid_list, save_fldr, bpm=bpm, sylLen=sylLen, method=method, volume=volume)


    # Run MATLAB to generate face
    eng = matlab.engine.start_matlab()
    print(str(Path.cwd()))
    eng.cd(str(Path.cwd()))
    beat = "/home/deepcut/deepcut/resource/beat" + str(beat_num) + ".wav"
    face = "/home/deepcut/deepcut/resource/Face_005.gif"
    [vidFile, mixFile] = eng.face_move_envelope(str(vocal), str(beat), str(face), nargout=2)
    vidFile = Path(vidFile)
    mixFile = Path(mixFile)
    print(vidFile,mixFile)
    # Re-encode video with audio
    cmd = "ffmpeg -i %s -i %s -c:v h264 -c:a aac %s -y" % (vidFile, mixFile, vocal.parent / (str(vidFile.stem) + ".mp4"))
    print(cmd)
    os.system(cmd)
    print("%s" % (vocal.parent / (str(vidFile.stem) + ".mp4")))

