.. _astropy-wcs:

***************************************
World Coordinate System (`astropy.wcs`)
***************************************

.. _wcslib: https://www.atnf.csiro.au/people/mcalabre/WCS/wcslib/index.html
.. _distortion paper: https://www.atnf.csiro.au/people/mcalabre/WCS/dcs_20040422.pdf
.. _SIP: https://irsa.ipac.caltech.edu/data/SPITZER/docs/files/spitzer/shupeADASS.pdf

Introduction
============

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
