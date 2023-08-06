import numpy as np
import scipy as sp

def make_ci(model, confidence):
    one = norm.ppf(confidence/100)
    two = norm.ppf((confidence+(100-confidence)/2)/100)
    model.ci_one = np.sqrt(model.intKsq)*one/np.sqrt(model.sample_size*model.band)
    model.ci_two = np.sqrt(model.intKsq)*two/np.sqrt(model.sample_size*model.band)