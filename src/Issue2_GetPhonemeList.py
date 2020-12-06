"""
    Modification History:
        Last modification date: October 27, 2020
        Last modification time: 9:35AM
    Description:
        Create a function that will get all the phonemes that exist in the
        file 'librispeech-lexicon.txt'. The code will take in the file 'librispeech-lexicon.txt'
        and extract each line from the file. The file is structured as [word] \t [phoneme1] ... [phonemeN].
        After reading a line from the file, the first will be take out of the line leaving the phonemes in
        the line. The line will be split into each individual words/phonemes and be placed into a numpy
        array. Only phonemes which are in the numpy array will be added that way there will be no repetition
        of phonemes into the array. The expected output is a sorted array consisting on each phoneme that is
        in the file with no duplicates.
    Current inputs:
        librispeech-lexicon.txt
    Expected output:
        List of all the phonemes in the input file with n o duplicates
    Error(s)/warning(s) to work on:
        FutureWarning: elementwise comparison failed; returning scalar instead, but in the future will
        perform elementwise comparison if word not in test_arr:
"""
from pathlib import Path
import numpy as np


def phoneme_list():
    #Path of input file. Change at your will.
    text_path = Path('C:\\Deepcut\\SD1_Intervals_assignment\\librispeech-lexicon.txt')

    # creates an empty numpy array
    phoneme_arr = np.array([])

    # Opens file to read and will be referenced as file in the loop
    with open(text_path, 'r') as file:
        # takes one line from the file. Will be referenced as line
        for line in file:
            # discards the file word file each letter
            discard, space, phoneme_line = line.partition(' ')
            # this will split the line (the one without the first word)
            # and place the individual words into the numpy array
            # the split line will be referenced as word
            for word in phoneme_line.split():
                # if word is not in the numpy array then it will added in there
                if word not in phoneme_arr:
                    phoneme_arr = np.append(phoneme_arr, word)

    # closes file
    file.close()

    # prints a sorted array with no duplicates
    print(np.sort(phoneme_arr, kind='mergesort'))


if __name__ == '__main__':
    phoneme_list()
