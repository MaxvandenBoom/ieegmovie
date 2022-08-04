#import functions
import mne
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import os
import neuropythy as ny
import nibabel as nib
from matplotlib import gridspec
from scipy.cluster import hierarchy


def sortCorrMaps(subj,corr_mat, freq):
    gs = gridspec.GridSpec(5, 5)
    fig=plt.figure(figsize=(20,10))

    ax2 = fig.add_subplot(gs[:-1, -1])
    Z = hierarchy.linkage(corr_mat, 'single')
    dn= hierarchy.dendrogram(Z,orientation='right')
    ax2.set_xticks([ ])

    ax = fig.add_subplot(gs[:-1, 1:])
    ax.imshow(corr_mat[:,dn["leaves"]])
    ax.set_axis_off()

    fig.align_ylabels()
    gs.update(wspace=0.1, hspace=0)
    plt.title(subj + freq +" task sorted") 
    plt.savefig("/home/jovyan/ieegmovie/corrMatrices/sorted/task/"+subj+"_task_"+freq+"-corrMat.png")
    plt.close(fig)