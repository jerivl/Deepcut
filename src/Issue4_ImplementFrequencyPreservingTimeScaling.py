"""
    Modification History:
        Last modification date: December 15, 2020
        Last modification time: 11:00PM
    Description:
        Create a function that will stretch or compress audio from a wav file to a specified duration,
        while preserving the pitch of the original audio.
    Current inputs:
        target_duration (int) - duration the audio (in seconds) will be stretched or compressed to
        wav_file (str) - wav file location of original audio to be stretched or compressed
        wav_file_new (str) - wav file location where the output audio will be saved
        method (int) - 1: Overlap-Add (OLA)
                       2: Waveform-Similarity Overlap-Add (WSOLA) [PREFERRED]
                       3: Phase Vocoder (PV-TSM)
    Expected output:
        Stretched or compressed audio saved to specified file
        flag (int) - 1 if successful, 0 if no input file found, -1 if target_duration is invalid,
            -2 if invalid method
    Error(s)/warning(s) to work on:
    The PyTSMod library was used for time-stretching:
        https://github.com/KAIST-MACLab/PyTSMod
"""

import numpy as np
from scipy.io import wavfile
import pytsmod as tsm
import soundfile as sf


def time_stretching(wav_file, wav_file_new, target_duration, method=2):
    data, sample_rate = sf.read(wav_file)

    if target_duration > 0:
        if ~np.isnan(sample_rate):
            data = data.T
            current_duration = np.size(data, axis=0)/sample_rate
            N = target_duration/current_duration

            if method == 1:
                data_new = tsm.ola(data, N)
                wavfile.write(wav_file_new, sample_rate, data_new)
                return 1
            elif method == 2:
                data_new = tsm.wsola(data, N)
                wavfile.write(wav_file_new, sample_rate, data_new)
                return 1
            elif method == 3:
                data_new = tsm.phase_vocoder(data, N)
                wavfile.write(wav_file_new, sample_rate, data_new)
                return 1
            else:
                return -2
        else:
            return 0
    else:
        return -1


if __name__ == '__main__':
    time_stretching('2_taco2_waveglow.wav', '2_taco2_waveglow_long_2.wav', 6, 2)
