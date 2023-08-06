#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    Merged to golden code at 2018.10.11 by Hoon.
"""
import os
import sys
import logging
import configparser
from logging import handlers as log_handlers
import datetime
import unicodedata
import glob
import json
import csv
import shutil
import numpy as np

try:
    # noinspection PyUnresolvedReferences
    import numpy as np
except Exception as e:
    print(" @ Warning: numpy import error in UtilsCommon - " + str(e))
try:
    # noinspection PyUnresolvedReferences
    from tqdm import tqdm
except Exception as e:
    print(" @ Warning: tqdm import error in UtilsCommon - " + str(e))


def convert_alphabet_to_number(_str):
    if isinstance(_str, int):
        return _str
    num = 0
    rev_str = _str[::-1]
    for i in range(len(rev_str)):
        print(rev_str[i])
        num += (ord(rev_str[i]) - 65) + 26 * i
    return num


def sample_signal(n_samples, corr, mu=0, sigma=1):
    assert 0 < corr < 1, "Auto-correlation must be between 0 and 1"
    # Find out the offset `c` and the std of the white noise `sigma_e`
    # that produce a signal with the desired mean and variance.
    # See https: //en.wikipedia.org/wiki/Autoregressive_model
    # under section "Example: An AR(1) process".
    c = mu * (1 - corr)
    sigma_e = np.sqrt((sigma ** 2) * (1 - corr ** 2))

    # Sample the auto - regressive process.
    signal = [c + np.random.normal(0, sigma_e)]

    for _ in range(1, n_samples):
        signal.append(c + corr * signal[-1] + np.random.normal(0, sigma_e))

    return np.array(signal)


def compute_corr_lag_1(signal):
   return np.corrcoef(signal[: -1], signal[1: ])[0][1]
