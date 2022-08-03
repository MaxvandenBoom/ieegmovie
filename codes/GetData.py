#import functions
import mne
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import os
from mne_bids import BIDSPath, read_raw_bids, print_dir_tree, make_report
from mne_bids.path import get_bids_path_from_fname
from ecog_preproc_utils import transformData

## get subjects
def getSubjects(path):
    subjects=[]
    for subject in os.listdir(path):
        if "sub-" in subject:
            subjects.append(subject)

    return subjects 

#get data 
class getData:
    def __init__(self, subj, path, sess, task, acq, run):
        self.subj= subj
        self.path= path
        self.sess= "iemu"
        self.task= "rest"
        self.acq= "clinical"
        self.run= "1"
    
    def getDataDir(self):
        data_dir = f'{self.path}/{self.subj}/ses-{self.sess}/ieeg/'
        return data_dir
    
    def getRawPath(self):
        raw_path = f'{self.path}/{self.subj}_ses-{self.sess}_task-{self.task}_acq-{self.acq}_run-{self.run}_ieeg.vhdr'
        return raw_path
        
    def getBidsPath(self):
        subj=self.subj
        bids_path = BIDSPath (subject=subj.strip("sub-"), session = self.sess, task = self.task, \
                 acquisition = self.acq, run = self.run, root = self.path, datatype ='ieeg')
        return bids_path
    
    def load_BIDS(self):
        """
        Load MNE raw object and drop bad channels

        Inputs:
        ----------------
        bids_path

        Outputs:
        ----------------
        cts : center frequencies for the filtering
        sds : bandwidths for the filtering
        """
        subj=self.subj
        bids_path = self.getBidsPath()
        
         # Read data and extract parameters from BIDS files
        raw = read_raw_bids(bids_path, verbose=True)

        raw.load_data()
        raw.set_meas_date(None)

        # drop bad channels
        raw.drop_channels(raw.info['bads'])
        # select only ecog channels
        raw.pick_types(ecog=True)

        return raw
    
    
    def saveHGData(self):
        data_dir = self.getDataDir()
        raw = self.load_BIDS()
        bids_path= self.getBidsPath()
        hgdat = transformData(raw, data_dir, band='high_gamma', notch=True, CAR=True,
                          car_chans='average', log_transform=True, do_zscore=True,
                          hg_fs=100, notch_freqs=np.arange(50, 251, 50), 
                          overwrite=False, ch_types='eeg', save=False)
        save_path= f'{self.path}/derivatives/HighGamma'
        fname= os.path.join(save_path, f'{bids_path.basename}_HG_raw.fif')
        hgdat.save(fname, overwrite=True)
    
    def saveCARData(self):
        data_dir = self.getDataDir()
        raw = self.load_BIDS()
        bids_path= self.getBidsPath()

        # Apply Notch filter
        raw.notch_filter(freqs=np.arange(50, 251, 50))

        # Common average reference
        raw_ref_car = raw.copy()
        raw_ref_car.set_eeg_reference(ref_channels = 'average')

        # save the data
        save_path= f'{self.path}/derivatives/CAR'
        fname= os.path.join(save_path, f'{bids_path.basename}_CAR_raw.fif')
        raw_ref_car.save(fname, overwrite=True)

        
    def getHGData(self):
        data_dir = self.path + "/derivatives/HighGamma"
        bids_path=self.getBidsPath()
        fname = os.path.join(data_dir, f'{bids_path.basename}_HG_raw.fif')
        hg = mne.io.read_raw(fname)  
        return hg
            
    def getCARData(self):
        data_dir = self.path + "/derivatives/CAR"
        bids_path=self.getBidsPath()
        fname = os.path.join(data_dir, f'{bids_path.basename}_CAR_raw.fif')
        car = mne.io.read_raw(fname) 
        return car