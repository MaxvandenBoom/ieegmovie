import mne
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import os
from mne_bids import BIDSPath, read_raw_bids, print_dir_tree, make_report
from mne_bids.path import get_bids_path_from_fname
from ecog_preproc_utils import transformData

def load_BIDS(bids_path):
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
    raw = read_raw_bids(bids_path, verbose=True)
     # Read data and extract parameters from BIDS files
    raw = read_raw_bids(bids_path, verbose=True)
    
    raw.load_data()
    raw.set_meas_date(None)
    
    # drop bad channels
    raw.drop_channels(raw.info['bads'])
    # select only ecog channels
    raw.pick_types(ecog=True)
    
    return raw

def extract_CAR(bids_path, output_path):
    
    raw = load_BIDS(bids_path)
    
    # Apply Notch filter
    raw.notch_filter(freqs=np.arange(50, 251, 50))
    
    # Common average reference
    raw_ref_car = raw.copy()
    raw_ref_car.set_eeg_reference(ref_channels = 'average')
    
    # High-pass filtering to remove slow drift
    raw_ref_car.filter(l_freq = 0.1, h_freq = None)
    
    # save the data
    fname = os.path.join(output_path, f'CAR/{bids_path.basename}_CAR_raw.fif')
    raw_ref_car.save(fname, overwrite=True)

    return raw_ref_car


def extract_oscillation(bids_path, data_dir, output_dir, oscillation):
    raw = load_BIDS(bids_path)
    
    dat = transformData(raw, data_dir, band=oscillation, notch=True, CAR=True,
                        car_chans='average', log_transform=True, do_zscore=True,
                      hg_fs=100, notch_freqs=np.arange(50, 251, 50), 
                      overwrite=False, ch_types='eeg', save=False)
    
    fname = os.path.join(output_dir,
                         f'{oscillation}/{bids_path.basename}_{oscillation}_raw.fif')
    dat.save(fname, overwrite=True)



