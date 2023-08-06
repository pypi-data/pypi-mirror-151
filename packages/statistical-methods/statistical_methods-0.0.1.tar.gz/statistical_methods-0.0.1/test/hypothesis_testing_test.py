from re import S
import numpy as np
import random as rd
import unittest

import sys

sys.path.insert(0, 'C:/Users/natji/statistical_methods/statistical_methods/')

from hypothesis_testing import *

class TestHypothesisTesting(unittest.TestCase):

    def test_t_test_zero_variance(self):
        data_number = rd.randint(2, 500)
        data_value  = rd.randrange(-500, 500)
        data = np.array([data_value] * data_number)

        p = t_test(data, p_value_only=True)

        self.assertIsNone(p)


    def test_t_test_further_from_target(self):
        data_number = rd.randint(2, 500)

        data1 = np.array([rd.randrange(-500, 500) for i in range(data_number)])

        target = mean(data1)

        data2 = data1 + 1
        data3 = data1 + 10
        data4 = data1 + 100

        p1 = t_test(data1, target, p_value_only=True)
        p2 = t_test(data2, target, p_value_only=True)
        p3 = t_test(data3, target, p_value_only=True)
        p4 = t_test(data4, target, p_value_only=True)
    
        assert p1 >= p2 >= p3 >= p4


    def test_t_test_mirrored_around_zero(self):
        data_number = rd.randint(2, 500)
        data1 = np.array([rd.randrange(0, 500) for i in range(data_number)])

        data2 = -data1

        p1 = t_test(data1, 0, tail_number=1, tail_direction="upper", p_value_only=True)
        p2 = t_test(data2, 0, tail_number=1, tail_direction="lower", p_value_only=True)

        self.assertEqual(p1, p2)


    def test_t_test_tail_number_changes(self):
        data_number = rd.randint(2, 500)
        data = np.array([rd.randrange(0, 500) for i in range(data_number)])

        p1 = t_test(data,0,tail_number=2,p_value_only=True)
        p2 = t_test(data,0,tail_number=1,tail_direction="upper",p_value_only=True)

        self.assertEqual(p1, p2*2)


    #TODO: Work out how to test for this
    def test_t_test_test_passess_correctly(self):
        pass_counter = 0
        fail_counter = 0
    
        for j in range(500):
            data_number = rd.randint(2,500)
            data = np.array([])
            for i in range(data_number):
                data = np.append(data,[rd.randrange(-500,500)])
        
            (test,p) = t_test(data)

            if p < 0.05:
                assert test == True
                pass_counter += 1
            elif p >= 0.05:
                assert test == False
                fail_counter += 1
            else:
                assert False

        assert True


    def test_t_test_p_value_sum(self):
        data_number = rd.randint(2, 500)
        data = np.array([rd.randrange(0, 500) for i in range(data_number)])

        p1 = t_test(data, 0, tail_number=1, tail_direction="upper", p_value_only=True)
        p2 = t_test(data, 0, tail_number=1, tail_direction="lower", p_value_only=True)

        self.assertEqual(p1 + p2, 1)


    def test_t_test_target_moves_closer(self):
        data_number = rd.randint(2, 500)
        data = np.array([rd.randrange(0, 500) for i in range(data_number)])
    
        target = mean(data)

        p1 = t_test(data, target, p_value_only=True)
        p2 = t_test(data, target+1, p_value_only=True)
        p3 = t_test(data, target+10, p_value_only=True)
        p4 = t_test(data, target+100, p_value_only=True)

        assert p1 >= p2 >= p3 >= p4


    #TODO: Work out how to test for this
    def test_ci_testing(self):
        passed = 0
        failed = 0

        for j in range(500):
            data_number = rd.randint(2, 500)
            data_1 = np.array([rd.randrange(0, 500) for i in range(data_number)])
            data_2 = np.array([rd.randrange(0, 500) for i in range(data_number)])

            (lower, upper) = confidence_interval(data_1)

            mean_2 = mean(data_2)

            if (mean_2 <= upper) and (mean_2>=lower):
                passed += 1
            else:
                failed += 1
        assert True
        

if __name__ == '__main__':
    unittest.main()