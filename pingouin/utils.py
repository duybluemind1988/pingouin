# Author: Raphael Vallat <raphaelvallat9@gmail.com>
# Date: April 2018
# GNU license
import numpy as np
from scipy import stats
from six import string_types
import pandas as pd


__all__ = ["_check_eftype", "_check_data", "_extract_effects"]

# SUB-FUNCTIONS
def _check_eftype(eftype):
    """Check validity of eftype"""
    return True if eftype in ['hedges', 'cohen', 'r', 'eta-square',
                              'odds-ratio', 'AUC'] else False


def _check_data(dv=None, group=None, data=None, x=None, y=None):
    """Extract data from dataframe or numpy arrays"""

    # OPTION A: a pandas DataFrame and column names are specified
    # -----------------------------------------------------------
    if all(v is not None for v in [dv, group, data]):
        for input in [dv, group]:
            if not isinstance(input, string_types):
                err = "Could not interpret input '{}'".format(input)
                raise ValueError(err)
        # Check that data is a pandas dataframe
        if not isinstance(data, pd.DataFrame):
            err = "data must be a pandas dataframe"
            raise ValueError(err)
        # Extract group information
        group_keys = data[group].unique()
        if len(group_keys) != 2:
            err = "group must have exactly two unique values."
            raise ValueError(err)
        # Extract data
        x = data[data[group] == group_keys[0]][dv]
        y = data[data[group] == group_keys[1]][dv]

    # OPTION B: x and y vectors are specified
    # ---------------------------------------
    else:
        if all(v is not None for v in [x, y]):
            for input in [x, y]:
                if not isinstance(input, (list, np.ndarray)):
                    err = "x and y must be np.ndarray"
                    raise ValueError(err)
    nx, ny = len(x), len(y)
    dof = nx + ny - 2
    return x, y, nx, ny, dof


def _extract_effects(dv=None, between=None, within=None, effects='all', data=None):
    """Extract data from dataframe or numpy arrays"""

    # Check input arguments
    if not isinstance(data, pd.DataFrame):
        raise ValueError('Data must be a pandas dataframe')
    if any(v is None for v in [dv, data]):
        raise ValueError('DV and data must be specified')
    if effects not in ['within', 'between', 'interaction', 'all']:
        raise ValueError('Effects must be: within, between, interaction or all')
    if effects == 'within' and not isinstance(within, string_types):
        raise ValueError('within must be specified when effects=within')
    elif effects == 'between' and not isinstance(between, string_types):
        raise ValueError('between must be specified when effects=between')
    elif effects == 'interaction':
        for input in [within, between]:
            if not isinstance(input, string_types):
                raise ValueError('within and between must be specified when \
                effects=interaction')

    # Extract number of pairwise comparisons
    if effects == 'within':
        col = within
    elif effects == 'between':
        col = between
    # Extract data
    labels = data[col].unique()
    npairs = len(labels)
    datadic = {}
    nobs = np.array([], dtype=int)

    print('Labels:', labels)
    for l in labels:
        datadic[l] = data[data[col] == l][dv]
        nobs = np.append(nobs, len(datadic[l]))

    dt_array = pd.DataFrame.from_dict(datadic)
    return dt_array, nobs