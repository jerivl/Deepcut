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

import os
from AlignerOutputToSyllableAudio import aligner_to_rap

if __name__ == "__main__":
    print(f"Arguments count: {len(sys.argv)}")
    for i, arg in enumerate(sys.argv):
        print(f"Argument {i:>6}: {arg}")

    # Set variables for flowtron
<<<<<<< Updated upstream
    inference_path = "inference.py"
    config_path = "config.json"
    flowtron_model = "models/flowtron_ljs.pt"
    waveglow_model = "models/waveglow_256channels_v5.pt"
    text = "It is well know that deep generative models have a deep latent space!"

    # Generate speech
    cmd = 'python %s -c %s -f %s -w %s -t "%s" -i 0' % (inference_path,config_path,flowtron_model,waveglow_model,text)
    print(cmd)
    os.chdir("/home/deepcut/flowtron")
    os.system(cmd)
=======
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
>>>>>>> Stashed changes

    # Split text
    text = "I am deep cut the rapper hear my rhymes they hit you like a blaster"
    words = text.split(sep=' ')
    w_num = int(len(words))
    rows = int(np.ceil(w_num / 10))
    for w in range(w_num, rows * 10):
        words.append('')

<<<<<<< Updated upstream
    # Set variables for mfa
    wav = "/home/deepcut/flowtron/results/sid0_sigma0.5.wav"
    resampled = "/home/deepcut/flowtron/results/sid0_sigma0.5_r.wav"
    transcript = "/home/deepcut/flowtron/results/sid0_sigma0.5.txt"
    dictionary_path = "/home/deepcut/deepcut/src/librispeech-lexicon.txt"
    textgrid_path = "/home/deepcut/flowtron/results/sid0_sigma0.5.TextGrid"
    corpus_path = os.path.dirname(wav)
=======
    phrases = np.reshape(words, (rows, 10))
    text_split = []
    for p in range(rows):
        string = list(phrases[p])
        temp = ' '.join(string)
        text_split.append(temp)
>>>>>>> Stashed changes

    wav_list = []
    textgrid_list = []
    for text_pnt in range(len(text_split)):
        # Generate speech
        cmd = 'python %s -c %s -f %s -w %s -t "%s" -i 0' % (inference_path,config_path,flowtron_model,waveglow_model,
                                                            text_split[text_pnt])
        print(cmd)
        src_dir = Path.cwd()
        flowtron_dir = (Path.cwd().parent).joinpath("flowtron")
        os.chdir(flowtron_dir)
        os.system(cmd)
        os.chdir(src_dir)


<<<<<<< Updated upstream
    cmd = "mfa align -v %s %s english %s " % (corpus_path, dictionary_path, textgrid_path)
    print(cmd)
    os.system(cmd)
=======
        # Set variables for mfa
        wav = (Path.cwd().parent).joinpath("flowtron","results","sid0_sigma0.5.wav")
        resampled = (Path.cwd().parent).joinpath("flowtron","results","sid0_sigma0.5_r.wav")
        transcript = (Path.cwd().parent).joinpath("flowtron","results","sid0_sigma0.5.txt")
        textgrid_path = (Path.cwd().parent).joinpath("flowtron","results","sid0_sigma0.5.TextGrid")
        dictionary_path = (Path.cwd().parent).joinpath("resource","librispeech-lexicon.txt")
        corpus_path = wav.parent

        # Write transcript
        with open(transcript,'w') as out_txt:
            out_txt.write(text)

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
        cmd = "copy %s %s" % (wav, wav2)
        os.system(cmd)

        textgrid_save = (wav.parent).joinpath(textgrid_path.name,"results_"+textgrid_path.name)
        textgrid_save2 = (Path.cwd().parent).joinpath("results", title + "_" + str(text_pnt) + ".TextGrid")
        cmd = "copy %s %s" % (textgrid_save, textgrid_save2)
        os.system(cmd)

        wav_list.append(wav2)
        textgrid_list.append(textgrid_save2)
>>>>>>> Stashed changes

    # Speech to rap transform

    save_fldr = '/home/deepcut/deepcut/src/'
    # save_fldr = '/home/deepcut/deepcut/scr/rap%s' % os.path.basename(wav)
    # if not os.path.isdir(save_fldr):
    #     os.mkdir(save_fldr)
    bpm = 100
<<<<<<< Updated upstream
    print(wav, save_fldr)
    aligner_to_rap(wav, "/home/deepcut/flowtron/results/sid0_sigma0.5.TextGrid/results_sid0_sigma0.5.TextGrid", save_fldr, bpm, subpb=4, sylLen=0.5)
=======
    sylLen = 0.5
    method = 1
    # print(wav, save_fldr)
    
    # vocal = aligner_to_rap(wav, (wav.parent).joinpath(textgrid_path.name,"results_"+textgrid_path.name), save_fldr, bpm, sylLen=0.5, method=1)
    vocal = aligner_to_rap(wav_list, textgrid_list, save_fldr, bpm=bpm, sylLen=sylLen, method=method)
>>>>>>> Stashed changes

    # TODO: Run MATLAB to generate face

    # Re-encode video  
    cmd = "ffmpeg -i /home/deepcut/deepcut/src/rap.avi -i /home/deepcut/deepcut/src/mix.wav -c:v h264 -c:a aac /home/deepcut/deepcut/src/done.mp4"
    