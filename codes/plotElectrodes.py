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

def sortCorrMaps(subj,corr_mat, freq, elecs):
    
    gs = gridspec.GridSpec(5, 5)
    fig=plt.figure(figsize=(20,10))

    ax2 = fig.add_subplot(gs[:-1, -1])
    Z = hierarchy.linkage(corr_mat, 'single')
    dn= hierarchy.dendrogram(Z,orientation='right')
    ax2.set_xticks([ ])
    chanorders = [elecs[l] for l in dn["leaves"]]

    ax = fig.add_subplot(gs[:-1, 1:])
    ordered_dat = corr_mat[:,dn["leaves"]]
    ordered_dat = ordered_dat[dn["leaves"],:]
    ax.imshow(ordered_dat)
    ax.tick_params("both")
    #ax.set_xticks([ ])
    ax.set_yticks(dn["leaves"])
    ax.set_yticklabels(chanorders, fontsize=0.5)

    gs.update(wspace=0.1, hspace=0)
    plt.title(subj + freq +" task sorted") 
    # plt.savefig("/home/jovyan/ieegmovie/corrMatrices/sorted/task/"+subj+"_task_"+freq+"-corrMat.png")
    plt.close(fig)
    
    return chanorders

