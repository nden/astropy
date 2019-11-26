# Licensed under a 3-clause BSD style license - see LICENSE.rst

import pytest

import numpy as np

from astropy import wcs

from . helper import SimModelTAB


@pytest.fixture(scope='module')
def tab_wcs_2di():
    model = SimModelTAB(nx=150, ny=200)

    # generate FITS HDU list:
    h = model.hdulist

    # create WCS object:
    w = wcs.WCS(h[0].header, h)

    return w
