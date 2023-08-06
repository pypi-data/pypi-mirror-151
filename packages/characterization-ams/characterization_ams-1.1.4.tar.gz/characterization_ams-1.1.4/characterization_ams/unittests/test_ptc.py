__author__ = "Denver Lloyd"
__copyright__ = "Copyright 2021, AMS Characterization"


import numpy as np
import pandas as pd
import sys
import os
import inspect
import pytest
import pdb
# currentdir = \
#     os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
# parentdir = os.path.dirname(currentdir)
# sys.path.insert(0, parentdir)
import characterization_ams.unittests.datasets as datasets
from characterization_ams.unittests import image_generator
from characterization_ams.stats_engine import stats
from characterization_ams.standard_tests import ptc
import pathlib
# load synthetic dataset
data = pd.read_csv(pathlib.Path(datasets.__file__).parents[0]/'test_emva.csv')


# generate dsnu and prnu images
ped_start = 168
peds = np.linspace(168, 3800, 30)
power = np.linspace(0, 10, 30)
rows = 100
cols = 100
pedestal = 168
n_images = 1000
images = []
temp = pd.DataFrame()
raw = pd.DataFrame()
for (idx, pp) in enumerate(peds):
    n_images = 1000
    rfpn = 105
    cfpn = 101
    ctn = 15
    rtn = 12
    ptn = 20 + np.sqrt(pp)
    pfpn = 95 + 0.08 * (pp - ped_start)

    tot_t = np.sqrt(ctn**2 + rtn**2 + ptn**2)
    tot_f = np.sqrt(rfpn**2 + pfpn**2 + cfpn**2)

    # fpn
    imgs = image_generator.gen_images(cfpn=cfpn,
                                      rfpn=rfpn,
                                      pfpn=pfpn,
                                      rtn=rtn,
                                      ptn=ptn,
                                      ctn=ctn,
                                      rows=rows,
                                      cols=cols,
                                      pedestal=pp,
                                      n_images=n_images)
    temp['Power'] = pd.Series(power[idx])
    temp['imagidx'] = idx
    raw = pd.concat([raw, temp]).reset_index(drop=True)
    images.append(np.array(imgs))


def test_ptc():
    """
    """

    data, hist, summ = ptc.ptc(images,
                               df=raw,
                               exp_col='Power')
    summ = ptc.ut.rename(summ, revert=True)
    data = ptc.ut.rename(data, revert=True)
    hist = ptc.ut.rename(hist, revert=True)

    system_gain = summ.system_gain[0]

    assert round(system_gain, 1) == 1.6
