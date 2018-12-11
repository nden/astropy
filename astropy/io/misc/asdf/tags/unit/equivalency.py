# Licensed under a 3-clause BSD style license - see LICENSE.rst
# -*- coding: utf-8 -*-

from astropy.units.equivalencies import Equivalency
from astropy.units import equivalencies
from astropy.units.quantity import Quantity
from asdf.yamlutil import custom_tree_to_tagged_tree

from astropy.io.misc.asdf.types import AstropyAsdfType


class EquivalencyType(AstropyAsdfType):
    name = "unit/equivalency"
    types = [Equivalency]
    version = '1.0.0'

    @classmethod
    def to_tree(cls, equiv, ctx):
        node = {}
        if not isinstance(equiv, Equivalency):
            raise TypeError("'{0}' is not a valid Equivalency".format(equiv))

        eqs = []
        for i, e in enumerate(equiv.name):
            args = equiv.args[i]
            args = [custom_tree_to_tagged_tree(val, ctx) if isinstance(val, Quantity)
                    else val for val in args]
            kwargs = equiv.kwargs[i]
            kwarg_names = list(kwargs.keys())
            kwarg_values = list(kwargs.values())
            kwarg_values = [custom_tree_to_tagged_tree(val, ctx) if isinstance(val, Quantity)
                            else val for val in kwarg_values]
            eq = {'name': e, 'args': args,  'kwargs_names': kwarg_names,
                  'kwargs_values': kwarg_values}
            eqs.append(eq)

        node['equivalencies'] = eqs
        return node

    @classmethod
    def from_tree(cls, node, ctx):
        import operator
        eqs = []
        for eq in node['equivalencies']:
            equiv = getattr(equivalencies, eq['name'])
            args = eq['args']
            kwargs = dict(zip(eq['kwargs_names'], eq['kwargs_values']))
            print('equivname', eq['name'], equiv)
            eqs.append(equiv(*args, **kwargs))
        if len(eqs) > 1:
            return operator.add(*eqs)
        else:
            return eqs[0]

    @classmethod
    def assert_equal(cls, a, b):
        assert a == b
