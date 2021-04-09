import numpy as np
import os
from scipy.io import wavfile

from Issue1_PhonemeToSyllables import get_phoneme, phoneme_to_syllable
from Issue5_SplitAudio import split_into_syllables
from Issue4_ImplementFrequencyPreservingTimeScaling import time_stretching


def aligner_to_rap(audio_file, textgrid_file, save_fldr, bpm, subpb=4, sylLen=1):
    [phonemes, start_times, end_times] = get_phoneme(textgrid_file)
    [syllables, min_times, max_times] = phoneme_to_syllable(phonemes, start_times, end_times)
    syl_files = split_into_syllables(audio_file, min_times, max_times, save_fldr)

    subpm = subpb*bpm
    subpsec = subpm/60
    if sylLen > 0 and sylLen <= 1:
        duration_sub = 1/subpsec
        duration = sylLen*duration_sub
        syl_files2 = syl_files

        for s in range(len(syl_files)):
            syl_file2 = os.path.splitext(syl_files[s])[0]
            syl_file2 = syl_file2 + '_scaled.wav'
            flag = time_stretching(syl_files[s], syl_file2, duration, 2)
            if flag != 1:
                print(['ERROR in scaling ' + syl_files[s]])
            else:
                syl_files2[s] = syl_file2

        # Make into rap without beat
        [sample_rate, data] = wavfile.read(audio_file)
        time_pnt = 0
        sample_rates = np.zeros(len(syl_files2))
        DATA = np.zeros(int(len(syl_files2)*duration_sub*sample_rate)+1)

        for s in range(len(syl_files2)):
            [sample_rate1, data] = wavfile.read(syl_files2[s])

            if sample_rate != sample_rate1:
                print(['ERROR: sampling rate not expected ' + syl_files2[s]])

            print(s)
            DATA[time_pnt:int(time_pnt+len(data))] = data
            time_pnt = int(time_pnt + sample_rate*duration_sub)

        # file_name = audio_file.split(sep='\\')
        # file_name = file_name[-1].split(sep='.')
        file_name = save_fldr + os.path.basename(audio_file) + '_Rap_bpm=' + str(bpm) + '_subpb=' + str(subpb) + \
                    '_sylLen=' + str(sylLen) + '_Accapela.wav'
        wavfile.write(file_name, sample_rate, DATA)
    else:
        print('ERROR: syllable length must be 0 < sylLen <= 1')


# if __name__ == '__main__':
#     # Using textgrid file from Working_with_audio_in_time-Jerry. Change as needed.
#     textgridFile = 'Working_with_audio_in_time-Jerry\\US114_F60_TG_VSDRC000.TextGrid'
#     audioFile = 'Working_with_audio_in_time-Jerry\\audio_transcripts\\US114_F60_TG_VSDRC000.wav'
#     saveFldr = 'Working_with_audio_in_time-Jerry\\syl_audio\\'
#     aligner_to_rap(audioFile, textgridFile, saveFldr, 100, 2, 1.5)
