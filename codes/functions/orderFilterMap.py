from scipy.io import loadmat
from GetData import getData
import numpy as np


def orderFilterMaps(data_dir, subj, sess, task, acq, run, ieegMap, channelOrder):
    '''
    Retrieve the ordered correlation maps from both fMRI and iEEG

    :param data_dir:
    :param subj:
    :param sess:
    :param task:
    :param acq:
    :param run:
    :param ieegMap: The iEEG map to use (e.g. HighGamma, theta)
    :param channelOrder: Defines which channel should be included in the output and the order of which
    :return:
    '''

    if isinstance(ieegMap, str):
        ieegMap = [ieegMap]

    # set directories
    fmricorr_dir = f'{data_dir}/derivatives/fmricorr'
    ieegcorr_dir = f'{data_dir}/derivatives/corrMaps'

    # load fMRI data and electrode names
    mat = loadmat(f'{fmricorr_dir}/sub-{subj}-fmri.mat')
    fmri_elecs = mat['electrodes'].tolist()
    fmri_elecs = [f[0].tolist()[0] for f in fmri_elecs]
    fmri_data = mat['roi_corr']

    # for each map, load ieeg electrode names and data
    ieeg_elecs = list()
    ieeg_data = list()
    for map in ieegMap:
        subj_data = getData(subj, data_dir, sess, task, acq, run)
        ieeg_elecs.append(subj_data.getHGData().info.ch_names)
        ieeg_data.append(np.load(f'{data_dir}/derivatives/corrMaps/{map}/sub-{subj}_ses-{sess}_task-{task}_acq-{acq}_run-{run}_{map}_corr.npy'))

    # find the electrodes that need to be excluded (from both fMRI and iEEG)
    fmri_incl_idxs = [i in channelOrder for i in fmri_elecs]
    fmri_excl_idxs = [not elem for elem in fmri_incl_idxs]
    fmri_excl_idxs = np.where(fmri_excl_idxs)[0]
    fmri_incl_idxs = np.where(fmri_incl_idxs)[0]
    assert (len(fmri_incl_idxs) == len(channelOrder))

    ieeg_incl_idxs = list()
    ieeg_excl_idxs = list()
    for idx, map in enumerate(ieegMap):
        ieeg_incl_idxs.append([i in channelOrder for i in ieeg_elecs[idx]])
        ieeg_excl_idxs.append([not elem for elem in ieeg_incl_idxs[-1]])
        ieeg_excl_idxs[-1] = np.where(ieeg_excl_idxs[-1])[0]
        ieeg_incl_idxs[-1] = np.where(ieeg_incl_idxs[-1])[0]
        assert(len(ieeg_incl_idxs[-1]) == len(channelOrder))

    # purge matrices of the electrodes that should be excluded
    fmri_data = np.delete(fmri_data, fmri_excl_idxs, axis=0)
    fmri_data = np.delete(fmri_data, fmri_excl_idxs, axis=1)
    for idx, map in enumerate(ieegMap):
        ieeg_data[idx] = np.delete(ieeg_data[idx], ieeg_excl_idxs[idx], axis=0)
        ieeg_data[idx] = np.delete(ieeg_data[idx], ieeg_excl_idxs[idx], axis=1)

    # purge electrode lists of the electrodes that should be excluded
    def _filterElec(in_list, channels):
        out_list = list()
        for chan in in_list:     # loop to make sure the order is maintained (and thus the same as the matrices)
            if chan in channelOrder:
                out_list.append(chan)
        return out_list

    fmri_elecs = _filterElec(fmri_elecs, channelOrder)
    for idx, map in enumerate(ieegMap):
        ieeg_elecs[idx] = _filterElec(ieeg_elecs[idx], channelOrder)

    # reorder the matrices
    def _reorder_mat(input_mat, sortingList, dir):
        out = np.empty(input_mat.shape)
        out[:] = np.nan

        # for chanCount, ii in enumerate(sortingList):
        chanCount = 0
        for ii in sortingList:
            if dir == 0:
                out[:, chanCount] = input_mat[:, ii]
            else:
                out[chanCount, :] = input_mat[ii, :]
            chanCount += 1
        return out

    fMRISortingList = list()
    fmri_out = list()
    ieeg_out = list()
    for idx, map in enumerate(ieegMap):

        # determine the order of the rows (for both fMRI and iEEG separately)
        iEEGSortingList = list()
        for channel in channelOrder:

            # find the channel index for fMRI
            if idx == 0:  # only once
                try:
                    fMRISortingList.append(fmri_elecs.index(channel))
                except:
                    assert('could not find ' + channel + ' in fMRI')

            # find the channel index for fMRI
            try:
                iEEGSortingList.append(ieeg_elecs[idx].index(channel))
            except:
                assert ('could not find ' + channel + ' in iEEG')

        if idx == 0:    # only once
            fmri_out = _reorder_mat(fmri_data, fMRISortingList, 0)
            fmri_out = _reorder_mat(fmri_out, fMRISortingList, 1)
        ieeg_out.append(_reorder_mat(ieeg_data[idx], iEEGSortingList, 0))
        ieeg_out[-1] = _reorder_mat(ieeg_out[-1], iEEGSortingList, 1)

    #
    if len(ieeg_out) == 1:
        ieeg_out = ieeg_out[0]

    return channelOrder, fmri_out, ieeg_out


##
#data_dir = '/Users/m218483/Documents/ieegmovie/repo'
#subj = '22'
#sess = 'iemu'
#task = 'film' # 'rest'
#acq = 'clinical'
#run = '1'
#ieegMap = {'HighGamma', 'CAR'}
#ieegMap = 'HighGamma'

#[elec, fmri, ieeg] = orderFilterMaps(data_dir, subj, sess, task, acq, run, ieegMap, ['T03', 'T01', 'T02', 'C02', 'C01'])
