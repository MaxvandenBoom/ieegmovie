import numpy as np
from scipy import stats

def getVec_LowerTri(cormat):
    # Fill diagonal and upper half with NaNs
    mask = np.zeros_like(cormat, dtype=bool)
    mask[np.triu_indices_from(mask)] = True
    
    cormat_half = cormat
    nanmat = np.empty(cormat.shape)
    cormat_half[mask] = np.nan
    
    cormat_half = cormat_half.reshape(-1)
    corVec = cormat_half[~np.isnan(cormat_half)]
    
    return corVec

def corr(BOLDcorr, iEEGcorr):
    # dimesion of BOLDcorr should be equal to iEEGcorr's
    BOLDvec = getVec_LowerTri(BOLDcorr)
    iEEGvec = getVec_LowerTri(iEEGcorr)
    
    [corrCoef, pvalue] = stats.pearsonr(BOLDvec, iEEGvec)
    
    return corrCoef, pvalue, BOLDvec, iEEGvec


if __name__ == '__main__':
    mat = np.random.rand(50,50)
    print(corr(mat, mat))
    
    