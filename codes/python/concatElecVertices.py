import glob
import os
import pandas as pd
from pathlib import Path
from io import StringIO

# config
subject = 'sub-60'
fsRoot = '/Users/<user>/Documents/ieegmovie/repo/derivatives/freesurfer'
suffix = '5mm-radius.label'

# retrieve the files
fileList = sorted(glob.glob(os.path.join(fsRoot, subject, 'label', (subject + '_*_' + suffix))))

outputTxt = ''

for file in fileList:
    filename = os.path.basename(file)

    # extract the electrode name
    elecName = filename[len(subject) + 1:filename.find('_', len(subject) + 1)]

    # read the file and toss out the first two lines (pandas has difficulty with skiprows on the first two lines)
    txt = Path(file).read_text()
    txt = txt[txt.find('\n') + 1:]
    txt = txt[txt.find('\n') + 1:]

    #
    df = pd.read_csv(StringIO(txt), delim_whitespace=True, header=None)
    for row in df.iterrows():
        outputTxt += str(int(row[1][0])) + ' ' + elecName + '\n'

# write output
with open(os.path.join(fsRoot, subject, 'label', (subject + '_ALL_' + suffix)), 'w') as f:
    f.write(outputTxt)

