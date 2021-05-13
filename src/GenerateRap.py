"""
    Modification History:
        Date: 4/30/2021
        Time: 10:00PM
    Description:
        Generate rap (vocal, video, and movements) from input text.
        Combines Text-to-Speech (Flowtron TTS), Forced alignment (Montreal Forced Aligner),
        and syllabifier in series [see aligner_to_rap] to perform speech to rap transformation.
        Then face movement is generated in MATLAB before video and audio is encoded to a final video file.
    Current inputs:
        Title (string).
        Lyrics (string),
        Flow choice (int)
        Beats per minute (bpm),
        Syllable length wrt subdivision sylLen (float),
        Beat choice (int)
        Volume (float)
        Flowtron/Waveglow model + config + inference script,
    Current output:
    Final video of Face + Beat + Rap Audio (.mp4)
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
    # print(f"Arguments count: {len(sys.argv)}")
    # for i, arg in enumerate(sys.argv):
    #     print(f"Argument {i:>6}: {arg}")

    '''
    Still trying to figure out args for system
    argv[0]: "GenerateRap.py"
    argv[1]: title
    argv[2]: text
    argv[3]: bpm
    argv[4]: syllable length
    argv[5]: flow choice (method)
    argv[6]: 
    others? maybe path to flowtron and waveglow models. maybe path to MFA if not on linux. also matlab
    '''
    # Create the parser
    my_parser = argparse.ArgumentParser(description='Convert text into rap')


    # Add the arguments
    my_parser.add_argument('Title', metavar='title', type=str, help='Title for the rap')
    my_parser.add_argument('Text', metavar='text', type=str, help='Lyrics of rap')
    my_parser.add_argument('Method', metavar='flow', type=int, help='Flow choice (int 1-5)')
    my_parser.add_argument('Beat', metavar='beat', type=int, help='Beat choice (int 1-3)')
    my_parser.add_argument('BPM', metavar='bpm', type=int, help='Beats per minute of rap (60 <= bpm <= 200)')
    my_parser.add_argument('SylLen', metavar='sylLen', type=float, help='Syllable length relative to the subdivision length (0 < sylLen <= 1)')
    my_parser.add_argument('Volume', metavar='volume', type=float, help='Volume of output audio (0 <= vol <= 5)')
    

    # title = "TRIAL"
    # text = "Villain get the money like curls they just trying to get a nut like squirrels in this mad world mad world"
    # bpm = 100
    # sylLen = 0.75
    # method = 5

    # Execute parse_args()
    args = my_parser.parse_args()

    title = args.Title
    text = args.Text
    method = args.Method
    beat_num = args.Beat
    bpm = args.BPM
    sylLen = args.SylLen
    volume = args.Volume

    # Input validation
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



    # Set variables for flowtron
    inference_path = (Path.cwd().parent).joinpath("flowtron","inference.py")
    config_path = (Path.cwd().parent).joinpath("flowtron","config.json")
    flowtron_model = (Path.cwd().parent).joinpath("resource","models","flowtron_ljs.pt")
    waveglow_model = (Path.cwd().parent).joinpath("resource","models","waveglow_256channels_universal_v5.pt")
    print(waveglow_model,Path.is_file(flowtron_model))
    if not Path.is_file(flowtron_model):
        raise FileNotFoundError("Ensure that the Flowtron model exists at %s" % str(flowtron_model.parent))
    if not Path.is_file(waveglow_model):
        raise FileNotFoundError("Ensure that the Waveglow model exists at %s" % str(waveglow_model.parent))



    # Split text
    text = text.strip()
    words = text.split(sep=' ')
    w_num = int(len(words))
    rows = int(np.ceil(w_num / 10))
    for w in range(w_num, rows * 10):
        words.append('')

    phrases = np.reshape(words, (rows, 10))
    text_split = []
    for p in range(rows):
        string = list(phrases[p])
        temp = ' '.join(string)
        text_split.append(temp)

    # text_split = [text]

    wav_list = []
    textgrid_list = []
    for text_pnt in range(len(text_split)):
        text_input = text_split[text_pnt]
        text_input = text_input.strip()

        # Generate speech
        cmd = 'python %s -c %s -f %s -w %s -t "%s" -i 0' % (inference_path,config_path,flowtron_model,waveglow_model,
                                                            text_input)
        print(cmd)
        src_dir = Path.cwd()
        flowtron_dir = (Path.cwd().parent).joinpath("flowtron")
        os.chdir(flowtron_dir)
        os.system(cmd)
        os.chdir(src_dir)


        # Set variables for mfa
        corpus_path = (Path.cwd().parent).joinpath("MFA",title + "_" + str(text_pnt))
        if not os.path.isdir(corpus_path):
            os.mkdir(corpus_path)
        wav_flowtron = (Path.cwd().parent).joinpath("flowtron","results","sid0_sigma0.5.wav")
        # wav_flowtron = Path("/home/deepcut/Documents/Survey_data/nat_speech_luz.wav")
        resampled = (Path.cwd().parent).joinpath("flowtron","results","sid0_sigma0.5_r.wav")
        wav = (Path.cwd().parent).joinpath("MFA",title + "_" + str(text_pnt),title + "_" + str(text_pnt)+ ".wav")
        transcript = (Path.cwd().parent).joinpath("MFA",title + "_" + str(text_pnt),title + "_" + str(text_pnt)+ ".txt")
        textgrid_path = (Path.cwd().parent).joinpath("MFA",title + "_" + str(text_pnt),title + "_" + str(text_pnt)+ ".TextGrid")
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
    # save_fldr = '/home/deepcut/deepcut/scr/rap%s' % os.path.basename(wav)
    # if not os.path.isdir(save_fldr):
    #     os.mkdir(save_fldr)
    # print(wav, save_fldr)

    # vocal = aligner_to_rap(wav, (wav.parent).joinpath(textgrid_path.name,"results_"+textgrid_path.name), save_fldr, bpm, sylLen=0.5, method=1)
    vocal = aligner_to_rap(wav_list, textgrid_list, save_fldr, bpm=bpm, sylLen=sylLen, method=method, volume=volume)

    # TODO: Run MATLAB to generate face
    # # vocal = Path("/home/deepcut/Documents/Survey_data/nat_speech_luz.wav")
    # resampled = Path("/home/deepcut/Documents/Survey_data/resampled.wav")
    # vocal = Path("/home/deepcut/Documents/Survey_data/tts_flowtron_ljs_combined.wav")
    # cmd = "sox %s -b 16 -r 16000 %s" % (vocal, resampled)
    # os.system(cmd)
    # os.system("rm %s" % vocal)
    # os.system("mv %s %s" % (resampled,vocal))

    # Run MATLAB to generate face
    eng = matlab.engine.start_matlab()
    print(str(Path.cwd()))
    eng.cd(str(Path.cwd()))
    beat = "/home/deepcut/deepcut/resource/beat" + str(beat_num) + ".wav"
    face = "/home/deepcut/deepcut/resource/Face_004_gr.gif"
    [vidFile, mixFile] = eng.face_move_envelope(str(vocal), str(beat), str(face), str(bpm), nargout=2)
    vidFile = Path(vidFile)
    mixFile = Path(mixFile)
    print(vidFile,mixFile)
    # Re-encode video with audio
    cmd = "ffmpeg -i %s -i %s -vf scale=720x720 -sws_flags neighbor -sws_dither none -c:v h264 -c:a aac %s -y" % (vidFile, mixFile, vocal.parent / (str(vidFile.stem) + ".mp4"))
    print(cmd)
    os.system(cmd)
    with open('output.txt','w') as out_txt:
        out_txt.write(str(vocal.parent / (str(vidFile.stem) + ".mp4")))
    
