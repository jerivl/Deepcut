"""
    Modification History:
        Last modification date: December 15, 2020
        Last modification time: 9:35AM
    Description:
        Create a function that will stretch or compress audio from a wav file to a specified duration.
        The change in pitch that occurs will be ignored.
    Current inputs:
        target_duration (int) - duration the audio will be stretched or compressed to
        wav_file (str) - wav file location of original audio to be stretched or compressed
        wav_file_new (str) - wav file location where the output audio will be saved
    Expected output:
        Stretched or compressed audio saved to specified file
        flag (int) - 1 if successful, 0 if no input file found, -1 if target_duration is invalid
    Error(s)/warning(s) to work on:
"""

import numpy as np
from scipy.io import wavfile


def naive_time_stretching(wav_file, wav_file_new, target_duration):
    sample_rate, data = wavfile.read(wav_file)

    if target_duration > 0:
        if ~np.isnan(sample_rate):
            current_duration = np.size(data, axis=0)/sample_rate
            N = current_duration/target_duration
            wavfile.write(wav_file_new, int(N*sample_rate), data)
            return 1
        else:
            return 0
    else:
        return -1


if __name__ == '__main__':
    naive_time_stretching('2_taco2_waveglow.wav', '2_taco2_waveglow_new.wav', 3)
