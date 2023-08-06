# This file is part of Build Your Own Tests
#
# Copyright 2018 Vincent Ladeuil
# Copyright 2013, 2014 Canonical Ltd.
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License version 3, as published by the
# Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranties of MERCHANTABILITY,
# SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.


from byot import (
    features,
)


class MinimalTesttools(features.Feature):

    def _probe(self):
        import testtools
        return testtools.__version__ >= (1, 8, 1)


minimal_testtools = MinimalTesttools()


class MinimalPep8(features.Feature):
    # Supporting precise is just too much work, requires at least the saucy
    # version

    def _probe(self):
        import pep8
        return pep8.__version__ >= '1.7.0'


minimal_pep8 = MinimalPep8()


class MinimalPyflakes(features.Feature):
    # Supporting precise is just too much work, requires at least the saucy
    # version

    def _probe(self):
        import pyflakes
        return pyflakes.__version__ >= '1.1.0'


minimal_pyflakes = MinimalPyflakes()
