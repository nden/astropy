.. _astropy-wcs:

***************************************
World Coordinate System (`astropy.wcs`)
***************************************

.. _wcslib: https://www.atnf.csiro.au/people/mcalabre/WCS/wcslib/index.html
.. _distortion paper: https://www.atnf.csiro.au/people/mcalabre/WCS/dcs_20040422.pdf
.. _SIP: https://irsa.ipac.caltech.edu/data/SPITZER/docs/files/spitzer/shupeADASS.pdf

Introduction
============

World Coordinate Systems (WCSs) describe the geometric transformations
between one set of coordinates and another. A common application is to
map the pixels in an image onto the celestial sphere. Another common
application is to map pixels to wavelength in a spectrum.

astropy.wcs contains utilities for managing World Coordinate System
(WCS) transformations defined in several elaborate `FITS WCS standard`_ conventions.
These transformations work both forward (from pixel to world) and backward
(from world to pixel).

For historical reasons and to support legacy software, `astropy.wcs` maintains
two separate application interfaces. The ``High-Level API`` should be used by
most applications. It abstracts out the underlying object and works transparently
with other packages which support the
`Common Python Interface for WCS <https://zenodo.org/record/1188875#.XnpOtJNKjyI>`_,
allowing for a more flexible approach to the problem and avoiding the `limitations
of the FITS WCS standard <https://ui.adsabs.harvard.edu/abs/2015A%26C....12..133T/abstract>`_.

The ``Low Level API`` is the original `astropy.wcs` API. It ties applications to
the `astropy.wcs` package and limits the transformations to the three distinct
types supported by it:

- Core WCS, as defined in the `FITS WCS standard`_, based on Mark
  Calabretta's `wcslib`_.  (Also includes ``TPV`` and ``TPD``
  distortion, but not ``SIP``).

- Simple Imaging Polynomial (`SIP`_) convention. (See :doc:`note about SIP in headers <note_sip>`.)

- table lookup distortions as defined in the FITS WCS `distortion
  paper`_.

.. _pixel_conventions:

Pixel Conventions and Definitions
---------------------------------

Both APIs assume that integer pixel values fall at the center of pixels (as assumed in
the `FITS WCS standard`_, see Section 2.1.4 of `Greisen et al., 2002,
A&A 446, 747 <https://doi.org/10.1051/0004-6361:20053818>`_).

However, there’s a difference in what is considered to be the first pixel. The
``High Level API`` follows the Python and C convention that the first pixel is
the 0-th one, i.e. the first pixel spans pixel values -0.5 to + 0.5. The
``Low Level API`` takes an additional ``origin`` argument with values of 0 or 1
indicating whether the input arrays are 0- or 1-based.
The Low-level interface assumes Cartesian order (x, y) of the input coordinates,
however the Common Interface for World Coordinate System accepts both conventions.
The order of the pixel coordinates ((x, y) vs (row, column)) in the Common API
depends on the method or property used, and this can normally be determined from
the property or method name. Properties and methods containing “pixel” assume (x, y)
ordering, while properties and methods containing “array” assume (row, column) ordering.

A Simple Example
================

One example of the use of the high-level WCS API is to use the
`~astropy.wcs.wcs.WCS.pixel_to_world` to yield the simplest WCS
with default values, converting from pixel to world coordinates::

    >>> from astropy.io import fits
    >>> from astropy.wcs import WCS
    >>> fn = get_pkg_data_filename('data/j94f05bgq_flt.fits', package='astropy.wcs.tests')
    >>> f = fits.open(fn)
    >>> w = WCS(f[1].header)
    >>> sky = w.pixel_to_world(30, 40)
    >>> print(sky)
    <SkyCoord (ICRS): (ra, dec) in deg
        (5.52844243, -72.05207809)>

Similarly, another use of the high-level API is to use the
`~astropy.wcs.wcs.WCS.world_to_pixel` to yield another simple WCS, while
converting from world to pixel coordinates::

    >>> from astropy.io import fits
    >>> from astropy.wcs import WCS
    >>> fn = get_pkg_data_filename('data/j94f05bgq_flt.fits', package='astropy.wcs.tests')
    >>> f = fits.open(fn)
    >>> w = WCS(f[1].header)
    >>> x, y = w.world_to_pixel(sky)
    >>> print(x, y)
    30.00000214674978 39.999999958214815

Using `astropy.wcs`
===================

Shared Python Interface for World Coordinate Systems
----------------------------------------------------

.. toctree::
   :maxdepth: 1

   wcsapi.rst

Legacy Interface
----------------

.. _legacy_interface:

Using the Core wcslib Transforms
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Some examples of the use of the core wcslib transforms is given below with
the `~astropy.wcs.wcs.WCS.wcs_pix2world` and `~astropy.wcs.wcs.WCS.wcs_world2pix`
for the pixel-to-world and world-to-pixel transformations.

Once the WCS object has been created, one can use the following method to convert
from pixel to world coordinates::

    >>> from astropy.wcs import WCS
    >>> w = WCS('image.fits')  # doctest: +IGNORE_WARNINGS
    >>> wx, wy = w.wcs_pix2world(30., 40., 1)
    >>> print(wx, wy)
    30.0 40.0

This converts the pixel coordinates (30., 40.) to the native world coordinate system
of the transformation. Note the third argument, set to 1, is to indicate whether
the pixel coordinates should be treated as starting from (1, 1) (as FITS files do)
or from (0, 0). Converting from world to pixel coordinates is similar::

    >>> from astropy.wcs import WCS
    >>> w = WCS('image.fits')  # doctest: +IGNORE_WARNINGS
    >>> px, py = w.wcs_world2pix(30., 40., 1)
    >>> print(px, py)
    30.0 40.0

Examples creating a WCS programmatically
----------------------------------------

.. toctree::
   :maxdepth: 2

   example_create_imaging
   example_cube_wcs

.. _wcslint:

Supported projections
---------------------

As `astropy.wcs` is based on `wcslib`_, it supports the standard
projections defined in the `FITS WCS standard`_.  These projection
codes are specified in the second part of the ``CTYPEn`` keywords
(accessible through `Wcsprm.ctype <astropy.wcs.Wcsprm.ctype>`), for
example, ``RA---TAN-SIP``.  The supported projection codes are:

- ``AZP``: zenithal/azimuthal perspective
- ``SZP``: slant zenithal perspective
- ``TAN``: gnomonic
- ``STG``: stereographic
- ``SIN``: orthographic/synthesis
- ``ARC``: zenithal/azimuthal equidistant
- ``ZPN``: zenithal/azimuthal polynomial
- ``ZEA``: zenithal/azimuthal equal area
- ``AIR``: Airy's projection
- ``CYP``: cylindrical perspective
- ``CEA``: cylindrical equal area
- ``CAR``: plate carrée
- ``MER``: Mercator's projection
- ``COP``: conic perspective
- ``COE``: conic equal area
- ``COD``: conic equidistant
- ``COO``: conic orthomorphic
- ``SFL``: Sanson-Flamsteed ("global sinusoid")
- ``PAR``: parabolic
- ``MOL``: Mollweide's projection
- ``AIT``: Hammer-Aitoff
- ``BON``: Bonne's projection
- ``PCO``: polyconic
- ``TSC``: tangential spherical cube
- ``CSC``: COBE quadrilateralized spherical cube
- ``QSC``: quadrilateralized spherical cube
- ``HPX``: HEALPix
- ``XPH``: HEALPix polar, aka "butterfly"

And, if built with wcslib 5.0 or later, the following polynomial
distortions are supported:

- ``TPV``: Polynomial distortion
- ``TUV``: Polynomial distortion

.. note::

    Though wcslib 5.4 and later handles ``SIP`` polynomial distortion,
    for backward compatibility, ``SIP`` is handled by astropy itself
    and methods exist to handle it specially.

WCS Tools
---------

.. toctree::
   :maxdepth: 1

   wcstools.rst

Relax Constants
---------------

.. toctree::
   :maxdepth: 1

   relax

Other Information
=================

.. toctree::
   :maxdepth: 1

   history
   validation

.. note that if this section gets too long, it should be moved to a separate
   doc page - see the top of performance.inc.rst for the instructions on how to do
   that
.. include:: performance.inc.rst

See Also
========

- `wcslib`_

.. _wcs-reference-api:

Reference/API
=============

.. automodapi:: astropy.wcs
   :inherited-members:

.. automodapi:: astropy.wcs.utils

.. automodapi:: astropy.wcs.wcsapi

Acknowledgments and Licenses
============================

`wcslib`_ is licenced under the `GNU Lesser General Public License
<http://www.gnu.org/licenses/lgpl.html>`_.
