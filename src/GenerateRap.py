"""
    Modification History:
        Date: 4/02/2021
        Time: 6:00PM
    Description:
        Generate rap (vocal, video, and movements) from input text.
        Combines Text-to-Speech (Flowtron TTS), Forced alignment (Montreal Forced Aligner),
        and syllabifier in series [see aligner_to_rap] to perform speech to rap transformation.
        Then face movement is generated in MATLAB before video and audio is encoded to a final video file.
    Current inputs:
        Lyrics (string),
        Beats per minute (bpm),
        Number of beat subdivisions (subpb),
        Syllable length wrt subdivision  (sylLen),
        TODO: Add beat here instead of in MATLAB
        Flowtron/Waveglow model + config + inference script,
    Current output:
        Rap vocal (audio only no beat)
        TODO: Final video of Face + Beat Rap Audio (.mp4)
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

if __name__ == "__main__":
    print(f"Arguments count: {len(sys.argv)}")
    for i, arg in enumerate(sys.argv):
        print(f"Argument {i:>6}: {arg}")

    '''
    Still trying to figure out args for system
    argv[0]: "GenerateRap.py"
    argv[1]: title
    argv[2]: text
    argv[3]: bpm
    argv[4]: syllable length
    argv[5]: flow choice (method)
    others? maybe path to flowtron and waveglow models. maybe path to MFA if not on linux. also matlab
    '''


    # Set variables for flowtron
    inference_path = (Path.cwd().parent).joinpath("flowtron","inference.py")
    config_path = (Path.cwd().parent).joinpath("flowtron","config.json")
    flowtron_model = (Path.cwd().parent).joinpath("resource","models","flowtron_ljs.pt")
    waveglow_model = (Path.cwd().parent).joinpath("resource","models","waveglow_256channels_v5.pt")
    print(waveglow_model,Path.is_file(flowtron_model))
    if not Path.is_file(flowtron_model):
        raise FileNotFoundError("Ensure that the Flowtron model exists at %s" % str(flowtron_model.parent))
    if not Path.is_file(waveglow_model):
        raise FileNotFoundError("Ensure that the Waveglow model exists at %s" % str(waveglow_model.parent))


    title = "TRIAL"

    # Split text
    text = "Villain get the money like curls They just tryin' to get a nut like squirrels in this mad world Land of milk"
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
        wav = (Path.cwd().parent).joinpath("flowtron","results","sid0_sigma0.5.wav")
        resampled = (Path.cwd().parent).joinpath("flowtron","results","sid0_sigma0.5_r.wav")
        transcript = (Path.cwd().parent).joinpath("flowtron","results","sid0_sigma0.5.txt")
        textgrid_path = (Path.cwd().parent).joinpath("flowtron","results","sid0_sigma0.5.TextGrid")
        dictionary_path = (Path.cwd().parent).joinpath("resource","librispeech-lexicon.txt")
        corpus_path = wav.parent

        # Write transcript
        with open(transcript,'w') as out_txt:
            out_txt.write(text_input)

        # Resample audio
        cmd = "sox %s -b 16 -r 16000 %s" % (wav, resampled)
        os.system(cmd)
        os.system("del %s" % wav)
        os.system("mv %s %s" % (resampled,wav))

        # Get phoneme timings
        cmd = "mfa align -v %s %s english %s " % (corpus_path, dictionary_path, textgrid_path)
        print(cmd)
        os.system(cmd)

        wav2 = (Path.cwd().parent).joinpath("results",title + "_" + str(text_pnt) + ".wav")
        cmd = "mv %s %s" % (wav, wav2)
        print(cmd)
        os.system(cmd)

        textgrid_save = (wav.parent).joinpath(textgrid_path.name,"results_"+textgrid_path.name)
        textgrid_save2 = (Path.cwd().parent).joinpath("results", title + "_" + str(text_pnt) + ".TextGrid")
        cmd = "mv %s %s" % (textgrid_save, textgrid_save2)
        print(cmd)
        os.system(cmd)

        wav_list.append(wav2)
        textgrid_list.append(textgrid_save2)

    # Speech to rap transform
    save_fldr = (Path.cwd().parent).joinpath("results")
    # save_fldr = '/home/deepcut/deepcut/scr/rap%s' % os.path.basename(wav)
    # if not os.path.isdir(save_fldr):
    #     os.mkdir(save_fldr)
    bpm = 100
    sylLen = 0.5
    method = 1
    # print(wav, save_fldr)

    # vocal = aligner_to_rap(wav, (wav.parent).joinpath(textgrid_path.name,"results_"+textgrid_path.name), save_fldr, bpm, sylLen=0.5, method=1)
    vocal = aligner_to_rap(wav_list, textgrid_list, save_fldr, bpm=bpm, sylLen=sylLen, method=method)

    # TODO: Run MATLAB to generate face

    # Run MATLAB to generate face
    eng = matlab.engine.start_matlab()
    print(str(Path.cwd()))
    eng.cd(str(Path.cwd()))
    beat = "/home/deepcut/deepcut/resource/beat1.wav"
    face = "/home/deepcut/deepcut/resource/Face_005.gif"
    [vidFile, mixFile] = eng.face_move_envelope(str(vocal), str(beat), str(face), nargout=2)
    vidFile = Path(vidFile)
    mixFile = Path(mixFile)
    print(vidFile,mixFile)
    # Re-encode video with audio
    cmd = "ffmpeg -i %s -i %s -c:v h264 -c:a aac %s -y" % (vidFile, mixFile, vocal.parent / (str(vidFile.stem) + ".mp4"))
    print(cmd)
    os.system(cmd)
