"""
    Modification History:
        Last modification date: March 26, 2021
        Last modification time: 3:30PM
    Description:
        Create a function that will split a wav file into the specified start and end times
    Current inputs:
        wav_file (str) - wav file location of original audio to be split
        xmin (double array) - array of start times
        xmax (double array) - array of end times
        save_fldr (str) - folder where split audio will be saved
    Expected output:
        saveFile (str list) - list of filenames where the split audio was saved
"""

import numpy as np
from scipy.io import wavfile
from os.path import basename
from Issue1_PhonemeToSyllables import get_phoneme, phoneme_to_syllable


def split_into_syllables(wav_file, xmin, xmax, save_fldr):
    #file_name = wav_file.split(sep='/')
    #file_name = file_name[-1].split(sep='.')
    file_name = basename(wav_file)

    [sample_rate, data] = wavfile.read(wav_file)
    length = data.shape[0]/sample_rate
    num_syl = len(xmin)
    save_files = ["" for i in range(num_syl)]
    for s in range(num_syl):
        save_file = save_fldr + file_name + '_' + str(s) + '.wav'
        sample_min = int(xmin[s]*sample_rate)
        sample_max = int(xmax[s]*sample_rate)
        syl_data = data[sample_min:sample_max]

        wavfile.write(save_file, sample_rate, syl_data)
        save_files[s] = save_file

    return save_files


if __name__ == '__main__':
    # Using textgrid file from Working_with_audio_in_time-Jerry. Change as needed.
    [phonemes, start_times, end_times] = get_phoneme('Working_with_audio_in_time-Jerry\\US114_F60_TG_VSDRC000.TextGrid')
    [syllables, min_times, max_times] = phoneme_to_syllable(phonemes, start_times, end_times)
    saveFiles = split_into_syllables('Working_with_audio_in_time-Jerry\\audio_transcripts\\US114_F60_TG_VSDRC000.wav',
                         min_times, max_times, 'Working_with_audio_in_time-Jerry\\syl_audio\\')
