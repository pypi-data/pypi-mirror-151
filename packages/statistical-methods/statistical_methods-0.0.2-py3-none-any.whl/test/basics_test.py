import numpy as np
import random as rd
import unittest

from statistical_methods.basics import *

class TestBasics(unittest.TestCase):

    def test_mean_two_repeated_values(self):
        data_number = rd.randint(1, 500)
        data = np.array([0, 1] * data_number)
        samp_mean = mean(data)
        self.assertEqual(samp_mean, 0.5)

    def test_mean_one_repeated_value(self):
        data_value = rd.randrange(-500, 500)
        data_number = rd.randint(1, 500)
        data = np.array([data_value] * data_number)
        samp_mean = mean(data)
        self.assertEqual(samp_mean, data_value)

    def test_mean_predetermined_data(self):
        data = np.array([5, 9, 7, 8.5, 4, 3, 2.1, 1.112, 5.8, 10, 0, 0.5, 5.5])
        samp_mean = mean(data)
        self.assertAlmostEqual(samp_mean, 4.73169230769)

    def test_mean_negative_data_negative_mean(self):
        data_number = rd.randint(1, 500)
        data = np.array([rd.randrange(-500, 500) for i in range(data_number)])
        data_neg = -data
        samp_mean = mean(data)
        mean_neg = mean(data_neg)
        self.assertEqual(samp_mean, -mean_neg)

    def test_mean_single_data_point(self):
        data_value = rd.randrange(-500, 500)
        data = np.array([data_value])
        samp_mean = mean(data)
        self.assertEqual(samp_mean, data_value)

    def test_variance_one_repeated_value(self):
        data_value = rd.randrange(-500, 500)
        data_number = rd.randint(1, 500)
        data = np.array([data_value] * data_number)
        var = variance(data)
        self.assertEqual(var, 0)

    def test_variance_repeating_two_values_more_decreases_variance(self):
        data_number = rd.randint(1, 500)
        data = np.array([rd.randrange(-500, 500) for i in range(data_number)])
        data_extended = data
        data_extended = np.append(data_extended,data)
        var = variance(data)
        var_extended = variance(data_extended)
        self.assertGreaterEqual(var, var_extended)

    def test_variance_single_data_point(self):
        data = np.array([rd.randrange(-500, 500)])
        var = variance(data)
        self.assertEqual(var, 0)

    def test_variance_predetermined_data(self):
        #TODO: Write predetermined data
        data = np.array([1, 1, 1])
        var = variance(data)
        self.assertEqual(var, 0)

    def test_variance_biased_estimate_differ(self):
        data_number = rd.randint(2,500)
        data = np.array([rd.randrange(-500, 500) for i in range(data_number)])

        var_1 = variance(data, use_biased_estimate=False)
        var_2 = variance(data, use_biased_estimate=True)

        self.assertGreaterEqual(var_1, var_2)

    def test_covariance(self):
        assert True

    def test_correlation(self):
        assert True

    def test_skewness(self):
        assert True

    def test_kurtosis(self):
        assert True

    def test_moment_first_moment_mean(self):
        data_number = rd.randint(2, 500)
        data = np.array([rd.randrange(-500, 500) for i in range(data_number)])
        samp_moment = moment(data)
        samp_mean = mean(data)
        self.assertEqual(samp_moment, samp_mean)

    def test_moment_first_central_moment_zero(self):
        data_number = rd.randint(2, 500)
        data = np.array([rd.randrange(-500, 500) for i in range(data_number)])
        samp_moment = moment(data, use_centralized_estimate= True)
        self.assertAlmostEqual(samp_moment, 0)

    def test_moment_second_centralised_moment_variance(self):
        data_number = rd.randint(2, 500)
        data = np.array([rd.randrange(-500, 500) for i in range(data_number)])
        samp_moment = moment(data, 2, use_centralized_estimate=True)
        var = variance(data, use_biased_estimate=True)
        self.assertEqual(samp_moment, var)

    def test_moment_zero_one(self):
        data_number = rd.randint(2, 500)
        data = np.array([rd.randrange(-500, 500) for i in range(data_number)])
        samp_moment = moment(data, 0)
        self.assertEqual(samp_moment, 1)

    def test_mse(self):
        assert True

    def test_rmse(self):
        assert True

    def test_mean_error(self):
        assert True

    def test_data_range(self):
        assert True

    def test_percentile(self):
        assert True

    def test_median(self):
        assert True

    def test_iqr(self):
        assert True

    def test_mode(self):
        assert True

    def test_correlation_correct_output_range(self):
        data_number = rd.randint(1, 500)

        data = np.array([rd.randrange(-500, 500) for i in range(data_number)])
        data2= np.array([rd.randrange(-500, 500) for j in range(data_number)])

        corr = correlation(data, data2)

        self.assertLessEqual(corr, 1)
        self.assertGreaterEqual(corr, -1)

    def test_correlation_identical_data(self):
        data_number = rd.randint(2, 500)

        data = np.array([rd.randrange(-500, 500) for i in range(data_number)])

        corr = correlation(data, data)

        self.assertAlmostEqual(corr, 1, places=1)

    def test_correlation_negative_data(self):
        data_number = rd.randint(2, 500)

        data = np.array([rd.randrange(-500, 500) for i in range(data_number)])

        corr = correlation(data, -data)

        self.assertAlmostEqual(corr, -1, places=1)

    def test_kurtosis_upper_bound(self):
        data_number = rd.randint(2, 500)

        data = np.array([rd.randrange(-500, 500) for i in range(data_number)])

        k = kurtosis(data)
        s = skewness(data)

        assert k >= ((s) ** 2) + 1

if __name__ == '__main__':
    unittest.main()