import numpy as np
from scipy.stats import norm

def make_ci(self, confidence):
    one = norm.ppf(confidence/100)
    two = norm.ppf((confidence+(100-confidence)/2)/100)
    self.ci_one = np.sqrt(self.intKsq)*one/np.sqrt(self.sample_size*self.band)
    self.ci_two = np.sqrt(self.intKsq)*two/np.sqrt(self.sample_size*self.band)