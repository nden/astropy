.. _legacy_interface:

Legacy Interface
----------------

.. _distortion paper: https://www.atnf.csiro.au/people/mcalabre/WCS/dcs_20040422.pdf
.. _SIP: https://irsa.ipac.caltech.edu/data/SPITZER/docs/files/spitzer/shupeADASS.pdf

It should be noted the following transformations can be applied to the coordinates:

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

    >>> from astropy.io import fits
    >>> from astropy.wcs import WCS
    >>> from astropy.utils.data import get_pkg_data_filename
    >>> fn = get_pkg_data_filename('data/j94f05bgq_flt.fits', package='astropy.wcs.tests')
    >>> f = fits.open(fn)
    >>> wcs = WCS(f[1].header)
    >>> lon, lat = wcs.all_pix2world(30, 40, 0)
    >>> print(lon, lat)
    5.528442425094046 -72.05207808966726

The applications of the other transformations in the above list are similar.

Loading WCS Information from a FITS File
----------------------------------------

This example loads a FITS file (supplied on the commandline) and uses
the WCS cards in its primary header to transform.

.. literalinclude:: examples/from_file.py
   :language: python