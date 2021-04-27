import numpy as np
import os
from scipy.io import wavfile

from Issue1_PhonemeToSyllables import get_phoneme, phoneme_to_syllable
from Issue5_SplitAudio import split_into_syllables
from Issue4_ImplementFrequencyPreservingTimeScaling import time_stretching


def aligner_to_rap(audio_file_list, textgrid_file_list, save_fldr, bpm=100, sylLen=1, method=1):
    syl_files = []
    for text_pnt in range(len(audio_file_list)):
        [phonemes, start_times, end_times] = get_phoneme(textgrid_file_list[text_pnt])
        [syllables, min_times, max_times] = phoneme_to_syllable(phonemes, start_times, end_times)
        syl_files_t = split_into_syllables(audio_file_list[text_pnt], min_times, max_times, save_fldr)
        
        syl_files.append(syl_files_t)

    syl_files = [item for sublist in syl_files for item in sublist]

    #print(type(syl_files), type(syl_files[0]), type(audio_file))
    syl_files2 = syl_files
    [sample_rate, data] = wavfile.read(audio_file_list[0])
    finish = 0
    count = 0
    beat = 0
    DATA = []
    while finish == 0:
        if method == 1:
            subpb = 4
            subpm = subpb*bpm
            subpsec = subpm/60
            duration_sub = 1/subpsec
            duration = sylLen*duration_sub
        elif method == 2:
            subpb = 2
            subpm = subpb*bpm
            subpsec = subpm/60
            duration_sub = 1/subpsec
            duration = sylLen*duration_sub
        elif method == 3:
            subpb = 1
            subpm = subpb*bpm
            subpsec = subpm/60
            duration_sub = 1/subpsec
            duration = sylLen*duration_sub
        elif method == 4:
            subpb = 3
            subpm = subpb*bpm
            subpsec = subpm/60
            duration_sub = 1/subpsec
            duration = sylLen*duration_sub
        elif method == 5:
            if (beat==0) or (beat==3) or (beat==4) or (beat>8):
                subpb = 4
                subpm = subpb*bpm
                subpsec = subpm/60
                duration_sub = 1/subpsec
                duration = sylLen*duration_sub
            elif beat==1:
                subpb = 3
                subpm = subpb*bpm
                subpsec = subpm/60
                duration_sub = 1/subpsec
                duration = (sylLen-(sylLen/3))*duration_sub
            elif beat==2:
                subpb = 1
                subpm = subpb*bpm
                subpsec = subpm/60
                duration_sub = 1/subpsec
                duration = (sylLen/2)*duration_sub
            elif beat==5:
                subpb = 3
                subpm = subpb*bpm
                subpsec = subpm/60
                duration_sub = 1/subpsec
                duration = 1*duration_sub
            elif beat==6:
                subpb = 2
                subpm = subpb*bpm
                subpsec = subpm/60
                duration_sub = 1/subpsec
                duration = (sylLen/2)*duration_sub
            elif (beat==7) or (beat==8):
                subpb = 2
                subpm = subpb*bpm
                subpsec = subpm/60
                duration_sub = 1/subpsec
                duration = sylLen*duration_sub

        beat = beat + 1
        
        count2 = int(count + subpb)
        if count2 >= len(syl_files2):
            finish = 1
            count2 = int(len(syl_files2))

        #print(syl_files)
        for s in range(count,count2):
            # print(type(syl_files), type(syl_files[s]), syl_files[s])
            # syl_file2 = os.path.splitext(syl_files[s])[0]
            syl_file2 = syl_files[s].parent / (syl_files[s].stem + '_scaled.wav')
            print(syl_files[s],syl_file2)
            flag = time_stretching(syl_files[s], syl_file2, duration, 2)
            if flag != 1:
                print(['ERROR in scaling ' + syl_files[s]])
            else:
                syl_files2[s] = syl_file2

        # Make into rap without beat
        time_pnt = 0
        data_b = np.zeros(int(np.ceil((count2-count)*duration_sub*sample_rate)))

        for s in range(count,count2):
            [sample_rate1, data] = wavfile.read(syl_files2[s])
            if sample_rate != sample_rate1:
                print(['ERROR: sampling rate not expected ' + syl_files2[s]])

            data_b[time_pnt:int(time_pnt+len(data))] = data
            time_pnt = int(time_pnt + sample_rate*duration_sub)

        DATA = np.concatenate([DATA,data_b])
        count = count2

    file_name = save_fldr / (str(audio_file_list[0].stem) + '_Rap_bpm=' + str(bpm) + '_method=' + str(method) + \
                '_sylLen=' + str(sylLen) + '_Accapela.wav')
    wavfile.write(file_name, sample_rate, DATA)
    return file_name

if __name__ == '__main__':
    # Using textgrid file from Working_with_audio_in_time-Jerry. Change as needed.
    textgridFile = 'Working_with_audio_in_time-Jerry\\US114_F60_TG_VSDRC000.TextGrid'
    audioFile = 'Working_with_audio_in_time-Jerry\\audio_transcripts\\US114_F60_TG_VSDRC000.wav'
    saveFldr = 'Working_with_audio_in_time-Jerry\\syl_audio\\'
    aligner_to_rap(audioFile, textgridFile, saveFldr, 100, 0.5, 5)
