"""
    Modification History:
        Date: 3/16/2021
        Time: 6:00PM
    Description:
        Will extract the phonemes from a TextGrid file and change them into
        syllables using the ARPABET dictionary. Two functions will be used
        to do this process. First function, get_phoneme, will get all of the
        phonemes and their timings from the TextGrid file into arrays. The second
        function, phoneme_to_syllables, will convert the set of phonemes into
        syllables. The syllabifier package will be used for the conversion.
        The syllable codes and syllable timings are saved.
    Current inputs:
        TextGrid File
    Current output:
        Size of the phoneme interval
        Output all of the phonemes from the phoneme intervals.
    NOTES:
        The code only works iff all TextGrid files are formatted the same as the current input
        Currently using Anaconda interpreter in base/root environment
        Packages Downloaded:
            Download the packages via cmd or anaconda cmd
            ARPABET dictionary: https://github.com/vgautam/arpabet-syllabifier/blob/master/tests/tmp.ipynb
            Textgrid Tool: https://github.com/kylebgorman/textgrid
                CMD download: pip install TextGrid
"""
from pathlib import Path
import textgrid
from syllabifier import syllabifyARPA
import numpy as np


def get_phoneme(filename):
    textgrid_file = textgrid.TextGrid.fromFile(Path(filename))

    """ 
        Currently looking at the phones tier (items[2] in the file)
        Find the number of intervals that are in this tier and change
        the data type to a string and split the string till you get the
        size then to an interger.
    """
    info_from_file = textgrid_file[1]
    size_info = str(info_from_file).split(", ", 1)[1].split(" ", 1)[0]
    size_of_interval = int(size_info)

    '''
        Store all of the phonemes into a large strings
        Store all of the timings of both xmin and xmax into SEPERATE
        arrays.
    '''
    # Print all of the phonemes found in the file
    phonemes_str = ''
    interval_min = np.zeros(size_of_interval)
    interval_max = np.zeros(size_of_interval)
    sil_phones = ['sp', 'spn', 'sil', '']
    count = 0
    for x in range(0, size_of_interval):
        phone = textgrid_file[1][x].mark
        # Filter Silence codes
        if phone not in sil_phones:
            # p_len = len(phone)  # length of string
            # if p_len > 2:  # for syllabifier, phones must have max length of 2
            #     phone = phone[0:2]
            # add to larger string
            phonemes_str = phonemes_str + ' ' + phone
            interval_min[count] = textgrid_file[1][x].minTime
            interval_max[count] = textgrid_file[1][x].maxTime
            count = count + 1

    interval_min = interval_min[0:count]
    interval_max = interval_max[0:count]
    print(phonemes_str)
    return phonemes_str, interval_min, interval_max

# This function is to convert the phonemes to syllables
def phoneme_to_syllable(phoneme, xmin, xmax):
    syllables = syllabifyARPA(phoneme)
    num_syl = len(syllables)
    interval_min = np.zeros(num_syl)
    interval_max = np.zeros(num_syl)
    count = 0
    for s in range(num_syl):
        syllable = syllables[s]
        phonemes = syllable.split()
        num_ph = len(phonemes)
        i1 = np.zeros(num_ph)
        i2 = np.zeros(num_ph)
        for p in range(num_ph):
            i1[p] = xmin[p+count]
            i2[p] = xmax[p+count]

        count = count + num_ph
        interval_min[s] = min(i1)
        interval_max[s] = max(i2)

    print(syllables)
    return syllables, interval_min, interval_max

if __name__ == '__main__':
    #Using textgrid file from Working_with_audio_in_time-Jerry. Change as needed.
    [phonemes, start_times, end_times] = get_phoneme('Working_with_audio_in_time-Jerry\\US114_F60_TG_VSDRC000.TextGrid')
    [syllables, min_times, max_times] = phoneme_to_syllable(phonemes, start_times, end_times)

