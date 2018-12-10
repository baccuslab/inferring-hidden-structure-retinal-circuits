"""
Generates Figure 3 from `Inferring hidden structure in neural circuits`,
Maheswaranathan et. al. 2018.
"""

import h5py
import numpy as np
from nems import models


def main():
    """Fits an LN and an LN-LN model to the same cell."""

    # load data (white noise stimulus and ganglion cell responses, sampled at 100Hz)
    with h5py.File('rgc_whitenoise.h5', 'r') as f:
        stimulus = np.array(f['stimulus'])
        rates = np.array(f['firing_rates'])

    # pick a cell to fit
    cell = 7
    stim_dim = stimulus.shape[0]
    hist_dim = 40       # temporal dimension for the spatiotemporal filter (400ms)

    # set up LN-LN model with 4 subunits
    lnln = models.LNLN(stimulus, rates[cell], (stim_dim, hist_dim), final_nonlinearity='softrect', num_subunits=4)

    # add regularization
    penalty_sparse = 1.25
    penalty_nucnorm = 1.7
    lnln.add_regularizer('W', 'sparse', gamma=penalty_sparse)
    lnln.add_regularizer('W', 'nucnorm', gamma=penalty_nucnorm)

    lnln.fit(disp=5, max_iter=8, num_alt=5)

    # plot LN-LN model parameters
    lnln.plot()

    return lnln


if __name__ == '__main__':
    lnln = main()
