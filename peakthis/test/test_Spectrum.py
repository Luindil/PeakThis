# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'
import unittest
import os

import numpy as np

from . import get_data_path
from ..model.Spectrum import Spectrum, BkgNotInRangeError

class SpectrumTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def array_almost_equal(self, array1, array2, places=7):
        self.assertAlmostEqual(np.sum(array1 - array2), 0, places=places)

    def array_not_almost_equal(self, array1, array2, places=7):
        self.assertNotAlmostEqual(np.sum(array1 - array2), 0, places=places)

    def test_loading_chi_files(self):
        spec = Spectrum()
        x, y = spec.data

        spec.load(get_data_path('dummy.chi')),
        new_x, new_y = spec.data

        self.assertNotEqual(len(x), len(new_x))
        self.assertNotEqual(len(y), len(new_y))

    def test_loading_invalid_file(self):
        spec = Spectrum()
        self.assertEqual(-1, spec.load(get_data_path("wrong_file_format.txt")))

    def test_saving_a_file(self):
        x = np.linspace(-5, 5, 100)
        y = x ** 2
        spec = Spectrum(x, y)
        spec.save("test.dat")

        spec2 = Spectrum()
        spec2.load("test.dat")

        spec2_x, spec2_y = spec2.data
        self.array_almost_equal(spec2_x, x)
        self.array_almost_equal(spec2_y, y)

        os.remove("test.dat")

    def test_plus_and_minus_operators(self):
        x = np.linspace(0, 10, 100)
        spectrum1 = Spectrum(x, np.sin(x))
        spectrum2 = Spectrum(x, np.sin(x))

        spectrum3 = spectrum1 + spectrum2
        self.assertTrue(np.array_equal(spectrum3._y, np.sin(x) * 2))
        self.assertTrue(np.array_equal(spectrum2._y, np.sin(x) * 1))
        self.assertTrue(np.array_equal(spectrum1._y, np.sin(x) * 1))

        spectrum3 = spectrum1 + spectrum1
        self.assertTrue(np.array_equal(spectrum3._y, np.sin(x) * 2))
        self.assertTrue(np.array_equal(spectrum1._y, np.sin(x) * 1))
        self.assertTrue(np.array_equal(spectrum1._y, np.sin(x) * 1))

        spectrum3 = spectrum2 - spectrum1
        self.assertTrue(np.array_equal(spectrum3._y, np.sin(x) * 0))
        self.assertTrue(np.array_equal(spectrum2._y, np.sin(x) * 1))
        self.assertTrue(np.array_equal(spectrum1._y, np.sin(x) * 1))

        spectrum3 = spectrum1 - spectrum1
        self.assertTrue(np.array_equal(spectrum3._y, np.sin(x) * 0))
        self.assertTrue(np.array_equal(spectrum1._y, np.sin(x) * 1))
        self.assertTrue(np.array_equal(spectrum1._y, np.sin(x) * 1))

    def test_plus_and_minus_operators_with_different_shapes(self):
        x = np.linspace(0, 10, 1000)
        x2 = np.linspace(0, 12, 1300)
        spectrum1 = Spectrum(x, np.sin(x))
        spectrum2 = Spectrum(x2, np.sin(x2))

        spectrum3 = spectrum1 + spectrum2
        self.array_almost_equal(spectrum3._x, spectrum1._x)
        self.array_almost_equal(spectrum3._y, spectrum1._y * 2, 2)

        spectrum3 = spectrum1 + spectrum1
        self.array_almost_equal(spectrum3._y, np.sin(x) * 2, 2)

        spectrum3 = spectrum1 - spectrum2
        self.array_almost_equal(spectrum3._y, np.sin(x) * 0, 2)

        spectrum3 = spectrum1 - spectrum1
        self.array_almost_equal(spectrum3._y, np.sin(x) * 0, 2)


    def test_multiply_operator(self):
        x = np.linspace(0, 10, 100)
        spectrum1 = 2 * Spectrum(x, np.sin(x))

        spectrum2 = 2 * Spectrum(x, np.sin(x))

        self.assertTrue(np.array_equal(spectrum2._y, np.sin(x) * 2))

    def test_using_background_spectrum(self):
        x = np.linspace(-5, 5, 100)
        spec_y = x ** 2
        bkg_y = x

        spec = Spectrum(x, spec_y)
        bkg = Spectrum(x, bkg_y)

        spec.set_background(bkg)
        new_x, new_y = spec.data

        self.array_almost_equal(new_x, x)
        self.array_almost_equal(new_y, spec_y - bkg_y)

    def test_using_background_spectrum_with_different_spacing(self):
        x = np.linspace(-5, 5, 100)
        spec_y = x ** 2
        x_bkg = np.linspace(-5, 5, 99)
        bkg_y = x_bkg

        spec = Spectrum(x, spec_y)
        bkg = Spectrum(x_bkg, bkg_y)

        spec.set_background(bkg)
        new_x, new_y = spec.data

        self.array_almost_equal(new_x, x)
        self.array_almost_equal(new_y, spec_y - x)

    def test_background_out_of_range_throws_error(self):
        x1 = np.linspace(0, 10)
        x2 = np.linspace(-10, -1)

        spec = Spectrum(x1, x1)
        bkg = Spectrum(x2, x2)

        spec.set_background(bkg)
        with self.assertRaises(BkgNotInRangeError):
            _, test = spec.data

    def test_setting_new_data(self):
        spec = Spectrum()
        x = np.linspace(0, 10)
        y = np.sin(x)
        spec.data = x, y

        new_x, new_y = spec.data
        self.array_almost_equal(new_x, x)
        self.array_almost_equal(new_y, y)

    def test_using_len(self):
        x = np.linspace(0,10,234)
        y = x**2
        spec = Spectrum(x, y)

        self.assertEqual(len(spec), 234)
