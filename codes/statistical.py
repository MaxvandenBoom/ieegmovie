import numpy as np
from scipy import stats

def getVec_LowerTri(cormat):
    # Fill diagonal and upper half with NaNs
    mask = np.zeros_like(cormat, dtype=bool)
    mask[np.triu_indices_from(mask)] = True
    
    cormat_half = cormat.copy()
    cormat_half[mask] = np.nan
    
    #reshape to a vector and drop the nan elements
    cormat_half = cormat_half.reshape(-1)
    corVec = cormat_half[~np.isnan(cormat_half)]
    
    return corVec

def corr(corMat1, corMat2, statistical_method: str):
    # size of corMat1 should be equal to corMat2's
    vec1 = getVec_LowerTri(corMat1)
    vec2 = getVec_LowerTri(corMat2)
    
    if "pearson" in statistical_method:
        [corrCoef, pvalue] = stats.pearsonr(vec1, vec2)
    elif "spearman" in statistical_method:
        [corrCoef, pvalue] = stats.spearmanr(vec1, vec2)
    
    return corrCoef, pvalue, vec1, vec2


if __name__ == '__main__':
    mat = np.random.rand(50,50)
    print(corr(mat, mat))
    
    