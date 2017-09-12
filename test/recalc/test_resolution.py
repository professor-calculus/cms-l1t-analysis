from __future__ import print_function
from nose.tools import assert_equal, assert_raises, assert_almost_equal
import numpy as np
from math import radians, sqrt
import cmsl1t.recalc.resolution as funcs
from exceptions import RuntimeError


def test_get_resolution_function():
    assert_equal(funcs.get_resolution_function("energy"), funcs.resolution_energy)
    assert_equal(funcs.get_resolution_function("phi"), funcs.resolution_phi)
    assert_equal(funcs.get_resolution_function("eta"), funcs.resolution_eta)
    assert_equal(funcs.get_resolution_function("position_1D"), funcs.resolution_position_1D)
    assert_equal(funcs.get_resolution_function("position_2D"), funcs.resolution_position_2D)
    assert_raises(RuntimeError, funcs.get_resolution_function,"gobbledygoop")


def test_resolution_energy():
    assert_equal(funcs.resolution_energy(10, 100), -0.9)
    assert_equal(funcs.resolution_energy(100, 10), 9.)
    assert_equal(funcs.resolution_energy(100, 100), 0)
    assert_equal(funcs.resolution_energy(0, 100), -1)
    assert_equal(str(funcs.resolution_energy(0, 0)).lower(), "nan")


def test_resolution_phi():
    assert_almost_equal(funcs.resolution_phi(radians(10), radians(100)), radians(-90))
    assert_almost_equal(funcs.resolution_phi(radians(100), radians(10)), radians(90))
    assert_almost_equal(funcs.resolution_phi(radians(15), radians(340)), radians(35))
    assert_almost_equal(funcs.resolution_phi(radians(340), radians(15)), radians(-35))
    assert_almost_equal(funcs.resolution_phi(radians(300), radians(333)), radians(-33))


def test_resolution_eta():
    assert_equal(funcs.resolution_eta(radians(10), radians(90)), radians(-80))
    assert_equal(funcs.resolution_eta(radians(-90), radians(10)), radians(-100))
    assert_equal(funcs.resolution_eta(radians(0), radians(-90)), radians(90))
    assert_equal(funcs.resolution_eta(radians(-90), radians(90)), radians(-180))
    assert_equal(funcs.resolution_eta(radians(0), radians(0)), 0)


def test_resolution_position_1D():
    assert_equal(funcs.resolution_position_1D(10, 11), -1)
    assert_equal(funcs.resolution_position_1D(100, -11), 111)
    assert_equal(funcs.resolution_position_1D(0, -11), 11)
    assert_equal(funcs.resolution_position_1D(0, 0), 0)


def test_resolution_position_2D():
    assert_equal(funcs.resolution_position_2D([1, 0], [0, 1]), sqrt(2))
    assert_equal(funcs.resolution_position_2D([-1, 0], [0, 1]), sqrt(2))
    assert_equal(funcs.resolution_position_2D([-1, 1], [0, 0]), sqrt(2))
    assert_equal(funcs.resolution_position_2D([1, 1], [1, 1]), 0)
    assert_equal(funcs.resolution_position_2D([1, 1], [-1, -1]), 2 * sqrt(2))
    assert_equal(funcs.resolution_position_2D([1, 1], [1, -1]), 2)

