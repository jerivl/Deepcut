"""
    Modification History:
        Date: 2/4/2021
        Time: 10:58AM
    Description:
        Will extract the phonemes from a TextGrid file and change them into
        syllables using the ARPABET dictionary. Two functions will be used
        to do this process. First function, get_phoneme, will get all of the
        phonemes and their timings from the TextGrid file into arrays the
        textgrid package will be used for part. The second function,
        phoneme_to_syllables, will convert the set of phonemes into syllables.
        The syllabifier package will be used for the convertion. Adding a new
        interval into the TextGrid file will be done by a different textgrid tool.
    Current inputs:
        US114_F60_TG_VSDRC000.TextGrid
    Current output:
        Information of the TextGrid file to understand the structure of the tool.
        Size of the phoneme invertal
        Output all off the phonemes from the phoneme intervals.
    Work on:
        Getting all of the phonemes and timings from the TextGrid file into arrays.
        Convertion to string or doubles will mostly likely be needed.
    NOTES:
        The code only works iff all TextGrid files are formatted the same as the current input
        Currently using Anaconda interpreter in base/root environment
        Packages Downloaded:
            Download the packages via cmd or anaconda cmd
            ARPABET dictionary: https://github.com/vgautam/arpabet-syllabifier/blob/master/tests/tmp.ipynb
            Textgrid Tool: https://github.com/kylebgorman/textgrid
                CMD download: pip install TextGrid
            Textgrid tool for future use(?) to create new intervals for syllables:
                https://github.com/hbuschme/TextGridTools/tree/5e58d13923f5e513c56667f157e6a5091e40f00d
"""
from pathlib import Path
import textgrid
# from syllabifier import syllabifyARPA
import numpy as np


def get_phoneme():
    #Using textgrid file from Working_with_audio_in_time-Jerry. Change as needed.
    textgrid_file = textgrid.TextGrid.fromFile(Path('C:\\Deepcut\\Working_with_audio_in_time-Jerry'
                                                    '\\Working_with_audio_in_time-Jerry\\US114_F60_TG_VSDRC000.TextGrid'))
    """
        Printing data from the textgrid
        This is to see how the textgrid package works and can be used
        later to change the phonemes to syllables
        While the textgrid file starts everything at 1 the package
        will start it at 0. Use (x - 1) to get the right tier/interval/item
        Delete later
    """
    print(textgrid_file)             # prints the general info of the textgrid
    print(textgrid_file[0])          # prints the info of the first tier
    print(textgrid_file[1])          # prints info of the second tier
    print(textgrid_file[1][0])       # prints info (xmin, xmax, text) of first interval in the second tier
    print(textgrid_file[1][0].mark)  # mark is used to get the text of the interval

    """ 
        Currently looking at the phones tier (items[2] in the file)
        Find the number of intervals that are in this tier and change
        the data type to a string and split the string till you get the
        size then to an interger.
        Long way
            info = textgrid_file[1]
            myinfo = str(info)
            print(myinfo.split(", ", 1)[1])
            myinfo2 = myinfo.split(", ", 1)[1]
            print(myinfo2)
            myinfo3 = myinfo2.split(" ", 1)[0]
            print(myinfo3)
            size_of_interval = int(myinfo3)
            print(size_of_interval)
    """
    # Easier/quicker way to get the size of the intervals
    info_from_file = textgrid_file[1]
    size_info = str(info_from_file).split(", ", 1)[1].split(" ", 1)[0]
    print("Size in string: ", size_info)    # Delete later
    size_of_interval = int(size_info)

    '''
        Store all of the phonemes into an array (preferably numpy)
        Store all of the timings of both xmin and xmax into SEPERATE
        arrays. Use textgrid_file[1][x].xmin/xmax to at least print
        the value(s) before placing into the array, if needed.
        If needed print all of the phonemes and timings before placing
        them into the array to see what is going where.
        ***Create the numpy arrays OUTSIDE the loop. If they are created
        inside the loop then they will only exist inside the loop.***
    '''
    # Print all of the phonemes found in the file
    for x in range(0, size_of_interval):
        print("\"", textgrid_file[1][x].mark, "\"")
        # Insert lines of code to place all information
        # in their respective arrays

# This function is to convert the phonemes to syllables
# def phoneme_to_syllable(phoneme):


if __name__ == '__main__':
    get_phoneme()
