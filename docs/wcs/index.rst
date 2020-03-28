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
The following example shows how to load an imaging WCS from an extension HDU.
The steps can be generalized to the case of a FITS file of any dimensions::

    >>> from astropy.wcs import WCS
    >>> from astropy.io import fits
    >>> hdu = fits.open('/Users/username/some_data_file.fits')
    >>> hdu.info()
    Filename: /Users/username/some_data_file.fits
    No.    Name      Ver    Type      Cards   Dimensions   Format
      0  PRIMARY       1 PrimaryHDU     156   (25, 76, 3644)   float64
    >>> hdr = hdu[0].header
    >>> wcs = WCS(hdr)
    >>> wcs
    WCS Keywords
    Number of WCS axes: 3
    CTYPE : 'RA---TAN'  'DEC--TAN'  'AWAV'
    CRVAL : 81.86752514  -12.69730074  5.399999999999999e-07
    CRPIX : 10.0  32.0  1.0
    PC1_1 PC1_2 PC1_3  : 1.0  0.0  0.0
    PC2_1 PC2_2 PC2_3  : 0.0  1.0  0.0
    PC3_1 PC3_2 PC3_3  : 0.0  0.0  1.0
    CDELT : 0.0002777777778  0.0002777777778  4.391981187874499e-11
    NAXIS : 25  76  3644

It is a good habit to check how many extensions are there, in case the FITS file is
of the multi-extension type.

It should be noted the following transformations can be applied:

    1. From pixels to world coordinates:

        - `~astropy.wcs.wcs.WCS.all_pix2world`: Perform all three
            transformations in series (core WCS, SIP and table lookup
            distortions) from pixel to world coordinates.  Use this one
            if you're not sure which to use.

        - `~astropy.wcs.wcs.WCS.wcs_pix2world`: Perform just the core
           WCS transformation from pixel to world coordinates.

    2. From world to pixel coordinates:

        - `~astropy.wcs.wcs.WCS.all_world2pix`: Perform all three
           transformations (core WCS, SIP and table lookup
           distortions) from world to pixel coordinates, using an
           iterative method if necessary.

        - `~astropy.wcs.wcs.WCS.wcs_world2pix`: Perform just the core
           WCS transformation from world to pixel coordinates.

    3. Performing `SIP`_ transformations only:

        - `~astropy.wcs.wcs.WCS.sip_pix2foc`: Convert from pixel to
           focal plane coordinates using the `SIP`_ polynomial
           coefficients.

        - `~astropy.wcs.wcs.WCS.sip_foc2pix`: Convert from focal
           plane to pixel coordinates using the `SIP`_ polynomial
           coefficients.

    4. Performing `distortion paper`_ transformations only:

        - `~astropy.wcs.wcs.WCS.p4_pix2foc`: Convert from pixel to
           focal plane coordinates using the table lookup distortion
           method described in the FITS WCS `distortion paper`_.

        - `~astropy.wcs.wcs.WCS.det2im`: Convert from detector
           coordinates to image coordinates.  Commonly used for narrow
           column correction.

For example, to convert pixel coordinates from a two dimensional image
to world coordinates::

    >>> from astropy.wcs import WCS
    >>> wcs = WCS('image.fits')  # doctest: +IGNORE_WARNINGS
    >>> lon, lat = wcs.all_pix2world(30, 40, 0)
    >>> print(lon, lat)
    31.0 41.0

The applications of the other transformations in the above list are similar.

Load from a file
----------------

Using `astropy.wcs`
===================

High level interface
--------------------

Low level interface
-------------------

Using the core wcslib transforms
--------------------------------

Examples creating a WCS programmatically
----------------------------------------

Supported projections
---------------------

WCS tools
---------

Relax constants
---------------

Other information
=================

.. toctree::
   :maxdepth: 1

   relax
   history
   wcsapi

.. note that if this section gets too long, it should be moved to a separate
   doc page - see the top of performance.inc.rst for the instructions on how to do
   that
.. include:: performance.inc.rst

See Also
========

- `wcslib`_

Reference/API
=============

.. automodapi:: astropy.wcs
   :inherited-members:

.. automodapi:: astropy.wcs.utils

Acknowledgments and Licenses
============================

`wcslib`_ is licenced under the `GNU Lesser General Public License
<http://www.gnu.org/licenses/lgpl.html>`_.
