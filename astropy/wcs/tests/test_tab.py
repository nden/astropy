# Licensed under a 3-clause BSD style license - see LICENSE.rst

import pytest

import numpy as np

from astropy import wcs

from . helper import SimModelTAB


def test_2d_spacial_tab_roundtrip():
    nx = 150
    ny = 200
    model = SimModelTAB(nx=nx, ny=ny)

    # generate FITS HDU list:
    h = model.hdulist

    # create WCS object:
    w = wcs.WCS(h[0].header, h)

    # generate random test coordinates:
    xy = 0.51 + [nx + 0.99, ny + 0.99] * np.random.random((100, 2))
    rd = w.wcs_pix2world(xy, 1)
    xy_roundtripped = w.wcs_world2pix(rd, 1)
    m = np.logical_and(*(np.isfinite(xy_roundtripped).T))
    assert np.allclose(xy[m], xy_roundtripped[m], rtol=0, atol=1e-7)


def test_2d_spacial_tab_vs_model():
    nx = 150
    ny = 200
    model = SimModelTAB(nx=nx, ny=ny)

    # generate FITS HDU list:
    h = model.hdulist

    # create WCS object:
    w = wcs.WCS(h[0].header, h)

    # generate random test coordinates:
    xy = 0.51 + [nx + 0.99, ny + 0.99] * np.random.random((100, 2))
    rd = w.wcs_pix2world(xy, 1)
    rd_model = model.fwd_eval(xy)
    assert np.allclose(rd, rd_model, rtol=0, atol=1e-7)
