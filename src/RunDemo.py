import logging
import threading
import time

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

# importing pyglet module
import pyglet
from PlayVideo import play_video


def test(x,y):
    z = x + y


if __name__ == "__main__":
    x = threading.Thread(target=play_video, args=("facetest.mp4",))
    y = threading.Thread(target=test, args=(1,2))

    logging.info("Main    : before running thread")

    x.start()
    y.start()
