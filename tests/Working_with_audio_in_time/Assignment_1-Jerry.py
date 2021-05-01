'''
Partial solution to assignment 1. The folder stucture and files used are given.
The concatenated audio (all.wav) as well as US114_F60_TG_VSDRC000.TextGrid are included as an example.
Note that I am using a Mac to write this. Adjust accordingly.
'''

from pathlib import Path
from intervaltree import IntervalTree
from textgrid import TextGrid
import pathlib
import matplotlib.pyplot as plt
import scipy.io.wavfile as wav
import numpy as np
import os

# I like to define my filepaths at the top of the program. Keeps it easy to adjust
# I'm spacing out most of these lines for readability

# Use the version for your OS
mfa_path = Path('montreal-forced-aligner/bin/mfa_align')

# i.e. input path. Just the directory containing our audio & transcripts
corpus_path = Path('audio_transcripts/')

# Defines the different words that exist in the transcripts and their phonemes
dictionary_path = Path('librispeech-lexicon.txt')

output_path = Path('alligned/')

# Edit 2: I forgot to specify English as the acoustic_model_path argument.
# Should work for all versions of MFA. Bit unintuitive
cmd = '%s %s %s English %s --verbose' % (mfa_path, corpus_path, dictionary_path, output_path)

print('Your working directory is: %s' % pathlib.Path().resolve())
print('This block will run force allignment with the command:\n%s' % cmd)
# If it breaks here:
# Run "cd your_working_directory" followed by the listed command in your command prompt.
os.system(cmd)

# Get list of paths because Pathlib's glob is a generator
corpus_audio = [path for path in corpus_path.glob('*.wav')]
output_path = Path('all.wav')

pad_time = 3 # seconds
all_padded = [] # list that stores padded audio data before concatenation
for file in corpus_audio:
    sample_rate, data = wav.read(file)

    # The concatenated data (even zeros) should be the same data type
    padding = np.zeros(pad_time * sample_rate).astype(data.dtype)

    # Note that np.concatenate takes a tuple or a list as the first argument.
    # The following is missing parentheses: np.concatenate(data, padding, axis=0)
    padded = np.concatenate((data, padding), axis=0)

    # Concatenate data and padding and add to end of list
    all_padded.append(padded)


# ###############################################
# # Concatenate all_padded and write as all.wav
# ###############################################
# concat = np.
# wav.write(output_path, rate, concat) # ***


# trees = []
# for file in corpus_path.glob('*.TextGrid'):
#     tree = IntervalTree()
#     ###############################################
#     # Determine how to index through textgrid intervals
#     # Add each interval to tree (use tree.addi)
#     ###############################################
#     intervals = # Read .textgrid file
#     for interval in intervals:
#         tree.addi()


# # Time axis will be given by
# t = np.linspace(0, len(concat)/rate, num = len(concat))
# ##################
# # Plot t vs data
# ##################



# ###############################################
# # Shift each interval tree based on order and lengths of padded data
# # Take union of all shifted trees
# # Only plot the points that exist in the Union_Tree - X (setminus)
# # Equivalently use an if statement
# ###############################################
