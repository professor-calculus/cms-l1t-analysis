# Licensed under a 3-clause BSD style license, see LICENSE.
"""
Subpackage for histogram collections
====================================
cms-l1t-analysis extends the defaultdict class to provide easier
ways to create and access sets of histograms.

**References**
.. [rootpy] https://pypi.python.org/pypi/rootpy.
"""

import six
from collections import defaultdict
import logging

from cmsl1t.io import to_root


logger = logging.getLogger(__name__)


def create_n_dim_dict(dimensions, initiaValue=0):
    if dimensions < 1:
        return initiaValue
    return defaultdict(lambda: create_n_dim_dict(dimensions - 1,
                                                 initiaValue))


# def n_dim_dict_itervalues(dictionary, dimensions):
#     if dimensions <= 1:
#         yield six.itervalues(dictionary)
#
#     # for v in six.itervalues(dictionary):
#     #     for x in n_dim_dict_itervalues(v, dimensions -1):
#     #         yield x
#     for v in six.itervalues(dictionary):
#         yield n_dim_dict_itervalues(v, dimensions -1)


def len_n_dim_dict(dictionary, dimensions):
    if dimensions <= 1:
        return len(dictionary)
    return sum(len_n_dim_dict(v, dimensions - 1)
               for v in six.itervalues(dictionary))


class BaseHistCollection(defaultdict):

    def __init__(self, dimensions, initiaValue=0):
        '''
            For each dimension create a dictionary
        '''
        defaultdict.__init__(self, lambda: create_n_dim_dict(
            dimensions - 1, initiaValue))
        self._dimensions = dimensions

    @property
    def dim(self):
        return self._dimensions

    def to_root(self, output_file):
        to_root(self, output_file)

    @staticmethod
    def from_root(input_file):
        from rootpy.io.pickler import load
        return load(input_file)

    def __len__(self):
        return len_n_dim_dict(self, self._dimensions)

    # def __iter__(self):
    #     yield n_dim_dict_itervalues(self, self._dimensions)
    #
    # def itervalues(self):
    #     yield n_dim_dict_itervalues(self, self._dimensions)
