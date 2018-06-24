"""Demo for fitting LN and LN-LN models to retinal data.

This demo uses the same data that is used in the paper `Inferring hidden structure in neural
circuits`.
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
    cell = 0
    stim_dim = stimulus.shape[0]
    hist_dim = 40       # temporal dimension for the spatiotemporal filter (400ms)

    # fit LN model (takes a few minutes)
    ln = models.LNLN(stimulus, rates[cell], (stim_dim, hist_dim), num_subunits=1)
    ln.fit()

    # plot LN model parameters
    ln.plot()

    # fit LN-LN model with 3 subunits (takes ~10 minutes)
    # (without regularization, see the `nems` package for how to add regularization)
    lnln = models.LNLN(stimulus, rates[cell], (stim_dim, hist_dim), num_subunits=3)
    lnln.fit()

    # plot LN-LN model parameters
    lnln.plot()


if __name__ == '__main__':
    main()
