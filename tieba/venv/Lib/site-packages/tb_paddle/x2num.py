from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import numpy as np


def check_nan(array):
    tmp = np.sum(array)
    if np.isnan(tmp) or np.isinf(tmp):
        print('Warning: NaN or Inf found in input tensor.')
    return array


def make_np(x):
    if isinstance(x, list):
        return check_nan(np.array(x))
    if isinstance(x, np.ndarray):
        return check_nan(x)
    if np.isscalar(x):
        return check_nan(np.array([x]))
    raise NotImplementedError('Got {}, but expected numpy array or torch tensor.'.format(type(x)))
