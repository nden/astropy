import numpy as np
import astropy.units as u
from .core import Model
from .parameters import Parameter


class AngleFromVectorGratingEquation(Model):
    """
    Solve the 3D Grating Dispersion Law for the refracted angle.
    Parameters
    ----------
    groove_density : int
        Grating ruling density.
    order : int
        Spectral order.
    """

    _separable = False

    inputs = ("lam", "alpha_in", "beta_in", "z")
    """ Wavelength and 3 angle coordinates going into the grating."""

    outputs = ("alpha_out", "beta_out", "zout")
    """ Three angles coming out of the grating. """

    groove_density = Parameter(default=1, unit=1/u.m)
    """ Grating ruling density."""

    order = Parameter(default=-1)
    """ Spectral order."""

    _input_units_strict = True

    _input_units_allow_dimensionless = True


    def evaluate(self, lam, alpha_in, beta_in, z, groove_density, order):
        if alpha_in.shape != beta_in.shape != z.shape:
            raise ValueError("Expected input arrays to have the same shape")
        orig_shape = alpha_in.shape or (1,)
        xout = -np.sin(alpha_in) - groove_density * order * lam
        yout = - np.sin(beta_in)
        ##print(xout**2)
        print(yout**2)
        zout = np.sqrt(1 - xout**2 - yout**2)
        xout.shape = yout.shape = zout.shape = orig_shape
        return xout, yout, zout

    @property
    def input_units(self):
        return {"lam": u.m,
                "alpha_in": u.rad,
                "beta_in": u.rad,
                "z": u.rad
                }

class WavelengthFromVectorGratingEquation(Model):
    """
    Solve the 3D Grating Dispersion Law for the wavelength.

    Parameters
    ----------
    groove_density : int
        Grating ruling density.
    order : int
        Spectral order.
    """

    _separable = False
    fittable = False
    linear = False

    _input_units_strict = True

    _input_units_allow_dimensionless = True

    inputs = ("alpha_in", "beta_in", "alpha_out")
    """ three angle - alpha_in and beta_in going into the grating and alpha_out coming out of the grating."""
    outputs = ("lam",)
    """ Wavelength."""

    groove_density = Parameter(default=1)
    """ Grating ruling density."""
    order = Parameter(default=1)
    """ Spectral order."""

    def evaluate(self, alpha_in, beta_in, alpha_out, groove_density, order):
        # beta_in is not used in this equation but is here because it's
        # needed for the prism computation. Currently these two computations
        # need to have the same interface.
        return -(np.sin(alpha_in) + np.sin(alpha_out)) / (groove_density * order)

    @property
    def input_units(self):
        return {"alpha_in": u.rad,
                "beta_in": u.rad,
                "z": u.rad
                }
