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


    # Set variables for mfa
    wav = "/home/deepcut/flowtron/results/sid0_sigma0.5.wav"
    resampled = "/home/deepcut/flowtron/results/sid0_sigma0.5_r.wav"
    transcript = "/home/deepcut/flowtron/results/sid0_sigma0.5.txt"
    dictionary_path = "/home/deepcut/deepcut/src/librispeech-lexicon.txt"
    textgrid_path = "/home/deepcut/flowtron/results/sid0_sigma0.5.TextGrid"
    corpus_path = os.path.dirname(wav)

    # Write transcript
    with open(transcript,'w') as out_txt:
        out_txt.write(text)

    # Resample audio
    cmd = "sox %s -b 16 -r 16000 %s" % (wav, resampled)
    os.system(cmd)
    os.system("del %s" % wav)
    os.system("mv %s %s" % (resampled,wav))

    cmd = "mfa align -v %s %s english %s " % (corpus_path, dictionary_path, textgrid_path)
    print(cmd)
    os.system(cmd)

    # Speech to rap transform

    save_fldr = '/home/deepcut/deepcut/src/'
    # save_fldr = '/home/deepcut/deepcut/scr/rap%s' % os.path.basename(wav)
    # if not os.path.isdir(save_fldr):
    #     os.mkdir(save_fldr)
    bpm = 100
    print(wav, save_fldr)
    aligner_to_rap(wav, "/home/deepcut/flowtron/results/sid0_sigma0.5.TextGrid/results_sid0_sigma0.5.TextGrid", save_fldr, bpm, subpb=4, sylLen=0.5)

    # TODO: Run MATLAB to generate face

    # Re-encode video  
    cmd = "ffmpeg -i /home/deepcut/deepcut/src/rap.avi -i /home/deepcut/deepcut/src/mix.wav -c:v h264 -c:a aac /home/deepcut/deepcut/src/done.mp4"
    