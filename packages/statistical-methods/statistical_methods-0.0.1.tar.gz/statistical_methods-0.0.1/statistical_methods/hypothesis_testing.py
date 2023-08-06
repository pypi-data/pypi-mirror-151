import numpy as np
import math
from pandas import NA
from scipy.stats import norm
from scipy.stats import t
from scipy.stats import chi2

from basics import *



def t_test(parameter_samples: np.ndarray, parameter_target=0, test_level=0.05, tail_number=2, tail_direction="upper", p_value_only=False):
    assert 0 <= test_level and test_level <= 1
    n = parameter_samples.size
    assert n > 1

    sample_mean = mean(parameter_samples)
    sample_variance = variance(parameter_samples)

    assert sample_variance >=0
    if sample_variance == 0:
        test_passed = False
        p_value = None
        #return "Insufficient Data"
        if p_value_only == True:
            return p_value
        elif p_value_only == False:
            return test_passed, p_value
        else:
            assert False

    test_statistic = (sample_mean - parameter_target) / (math.sqrt(sample_variance / n))

    if tail_number == 1:
        if tail_direction == "upper":
            critical_value = t.ppf(1-test_level, df=n-1)
            p_value = t.cdf(-test_statistic, df=n-1)

            if test_statistic <= critical_value:
                test_passed = False
            else:
                test_passed = True
        elif tail_direction == "lower":
            critical_value = t.ppf(test_level, df=n-1)
            p_value = t.cdf(test_statistic, df=n-1)

            if test_statistic >= critical_value:
                test_passed = False
            else:
                test_passed = True
        else:
            assert False
    elif tail_number == 2:
        critical_value_low  = t.ppf((test_level/2), df=n-1)
        critical_value_high = t.ppf(1-(test_level/2), df=n-1)
        p_value = 2 * t.cdf(-abs(test_statistic), df=n-1)

        if (test_statistic <= critical_value_high) and (test_statistic >= critical_value_low):
            test_passed = False
        else:
            test_passed = True
    else:
        assert False

    if p_value_only == True:
        return p_value
    elif p_value_only == False:
        return test_passed, p_value
    else:
        assert False



def z_test(parameter_samples: np.ndarray, parameter_target=0, test_level=0.05, tail_number=2, tail_direction="upper", p_value_only=False):
    assert 0 <= test_level and test_level <= 1
    n = parameter_samples.size
    assert n > 1

    sample_mean = mean(parameter_samples)
    sample_variance = variance(parameter_samples)
    
    assert sample_variance >= 0
    if sample_variance == 0:
        test_passed = False
        p_value = None
        #return "Insufficient Data"
        if p_value_only == True:
            return p_value
        elif p_value_only == False:
            return test_passed, p_value
        else:
            assert False

    test_statistic = (sample_mean - parameter_target) / math.sqrt(sample_variance)

    if tail_number == 1:
        if tail_direction == "upper":
            critical_value = norm.ppf(1 - test_level)
            p_value = norm.cdf(-test_statistic)

            if test_statistic <= critical_value:
                test_passed = False
            else:
                test_passed = True
        elif tail_direction == "lower":
            critical_value = norm.ppf(test_level)
            p_value = norm.cdf(test_statistic)

            if test_statistic >= critical_value:
                test_passed = False
            else:
                test_passed = True
        else:
            assert False
    elif tail_number == 2:
        critical_value_low  = norm.ppf((test_level/2))
        critical_value_high = norm.ppf(1-(test_level/2))
        p_value = 2 * norm.cdf(-abs(test_statistic))

        if (test_statistic <= critical_value_high) and (test_statistic >= critical_value_low):
            test_passed = False
        else:
            test_passed = True
    else:
        assert False

    if p_value_only == True:
        return p_value
    elif p_value_only == False:
        return test_passed, p_value
    else:
        assert False



def chi_sq_test():
    return 0



def f_test():
    return 0



def shapiro_wilk_test():
    return 0



def two_sample_t_test():
    return 0



#TODO: Check over this code
def confidence_interval(sample_data: np.ndarray, confidence_level=0.95, interval_type="mean", distribution = "normal"):
    assert 0 <= confidence_level and confidence_level <=1
    n = sample_data.size
    assert n > 1

    sample_mean = mean(sample_data)
    sample_variance = variance(sample_data)

    alpha = 1-confidence_level

    lower_level = alpha/2
    upper_level = 1 - alpha/2

    if distribution == "normal":
        lower_quantile = norm.ppf(lower_level)
        upper_quantile = norm.ppf(upper_level)
    elif distribution == "t":
        lower_quantile = t.ppf(lower_level,df=n-1)
        upper_quantile = t.ppf(upper_level,df=n-1)
    else:
        assert False

    if interval_type == "mean":
        lower_limit = sample_mean - upper_quantile*math.sqrt(sample_variance/n)
        upper_limit = sample_mean + upper_quantile*math.sqrt(sample_variance/n)
    elif interval_type == "variance":
        lower_quantile = chi2.ppf(upper_level,df=n-1)
        upper_quantile = chi2.ppf(lower_level,df=n-1)

        lower_limit = (n-1)*sample_variance/lower_quantile
        upper_limit = (n-1)*sample_variance/upper_quantile
    elif interval_type == "sd":
        #TODO: Double check that this is correct
        lower_quantile = chi2.ppf(upper_level,df=n-1)
        upper_quantile = chi2.ppf(lower_level,df=n-1)

        lower_limit = math.sqrt((n-1)*sample_variance/lower_quantile)
        upper_limit = math.sqrt((n-1)*sample_variance/upper_quantile)
    else:
        assert False

    return lower_limit, upper_limit



def anova():
    return 0



def manova():
    return 0
