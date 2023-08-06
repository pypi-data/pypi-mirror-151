import numpy as np
import math 



def mean(sample_data: np.ndarray) -> float:
    n = sample_data.size
    assert n > 0

    sample_sum = 0
    for i in range(n):
        sample_sum += sample_data[i]

    sample_mean = sample_sum / n

    return sample_mean



def variance(sample_data: np.ndarray, use_biased_estimate=False) -> float:
    assert use_biased_estimate == True or use_biased_estimate == False
    n = sample_data.size
    assert n > 0

    if n == 1:
        use_biased_estimate = True

    sample_sum = 0
    sample_mean = mean(sample_data)

    for i in range(n):
        sample_sum += (sample_data[i] - sample_mean) ** 2

    if use_biased_estimate == True:
        sample_variance = sample_sum / n
    elif use_biased_estimate == False:
        sample_variance = sample_sum / (n-1)
    else:
        assert False
    
    return sample_variance



def standard_deviation(sample_data: np.ndarray, use_biased_estimate=False) -> float:
    assert use_biased_estimate == True or use_biased_estimate == False
    n = sample_data.size
    assert n > 0

    sample_variance = variance(sample_data, use_biased_estimate)
    sd = math.sqrt(sample_variance)

    return sd



def covariance(sample_x: np.ndarray, sample_y: np.ndarray, use_biased_estimate=False) -> float:
    assert use_biased_estimate == True or use_biased_estimate == False
    assert sample_x.size == sample_y.size
    n = sample_x.size
    assert n > 0 

    if n == 1:
        use_biased_estimate = True

    sample_sum = 0
    mean_x = mean(sample_x)
    mean_y = mean(sample_y)

    for i in range(n):
        sample_sum += sample_x[i] * sample_y[i]
    sample_sum = sample_sum - (mean_x * mean_y)

    if use_biased_estimate == True:
        sample_covariance = sample_sum / n
    elif use_biased_estimate == False:
        sample_covariance = sample_sum / (n-1)
    else:
        assert False
    
    return sample_covariance



def correlation(sample_x: np.ndarray, sample_y: np.ndarray, use_biased_estimate=False) -> float:
    assert use_biased_estimate == True or use_biased_estimate == False
    assert sample_x.size == sample_y.size
    n = sample_x.size
    assert n > 0 

    sd_x = standard_deviation(sample_x)
    sd_y = standard_deviation(sample_y)
    sample_cov = covariance(sample_x, sample_y, use_biased_estimate)

    sample_corr = sample_cov / (sd_x * sd_y)

    return sample_corr



#TODO: Needs testing
def skewness(sample_data: np.ndarray, use_biased_estimate=False) -> float:
    assert use_biased_estimate == True or use_biased_estimate == False
    n = sample_data.size
    assert n > 0 

    sample_mean = mean(sample_data)
    var = variance(sample_data, use_biased_estimate)

    third_moment_sum = 0

    for i in range(n):
        third_moment_sum += (sample_data[i] - sample_mean) ** 3

    third_moment = third_moment_sum / n

    skewness = third_moment / (var ** (3 / 2))

    return skewness



#TODO: change according to kurtosis defns
#TODO: what to do with biased estimates?
def kurtosis(sample_data: np.ndarray, use_excess_kurtosis=False) -> float:
    n = sample_data.size
    assert n > 0

    sample_mean = mean(sample_data)
    var = variance(sample_data, use_biased_estimate=True) 

    sample_sum = 0

    for i in range(n):
        sample_sum += (sample_data[i] - sample_mean) ** 4
    
    sample_sum = sample_sum / n

    if use_excess_kurtosis == True:
        sample_kurtosis = sample_sum / ((var) ** 2) - 3
    elif use_excess_kurtosis == False:
        sample_kurtosis = sample_sum / ((var) ** 2)
    else:
        assert False

    return sample_kurtosis



#TODO: Double check over moment code
#TODO: Centralised and standardized moments are not fully correct?
def moment(sample_data: np.ndarray, moment_power=1, use_standardized_estimate=False, use_centralized_estimate=False) -> float:
    n = sample_data.size
    assert n > 0
    assert moment_power >= 0 

    if (use_standardized_estimate == False) and (use_centralized_estimate == False):
        sample_sum = 0
        for i in range(n):
            sample_sum += (sample_data[i]) ** moment_power
        sample_moment = sample_sum / n
    elif use_standardized_estimate == True:
        sample_mean = mean(sample_data)
        sample_sd   = standard_deviation(sample_data)

        sample_sum = 0
        for i in range(n):
            sample_sum += ((sample_data[i] - sample_mean) / (sample_sd)) ** moment_power
        sample_moment = sample_sum / n
    elif (use_centralized_estimate == True) and (use_standardized_estimate == False):
        sample_mean = mean(sample_data)

        sample_sum = 0
        for i in range(n):
            sample_sum += (sample_data[i] - sample_mean) ** moment_power
        sample_moment = sample_sum / n
    else:
        assert False
    
    return sample_moment



def mse(modelled: np.ndarray, observed: np.ndarray) -> float:
    assert modelled.size == observed.size
    n = modelled.size
    assert n > 0 
    se_sum = 0

    for i in range(n):
        se_sum += (modelled[i] - observed[i]) ** 2

    mean_square_error = se_sum / n

    return mean_square_error



def rmse(modelled: np.ndarray, observed: np.ndarray) -> float:
    assert modelled.size == observed.size
    n = modelled.size
    assert n > 0

    mean_square_error = mse(modelled, observed)
    root_mean_square_error = math.sqrt(mean_square_error)

    return root_mean_square_error



def mean_error(modelled: np.ndarray, observed: np.ndarray) -> float:
    assert modelled.size == observed.size 
    n = modelled.size
    assert n > 0
    me_sum = 0 

    for i in range(n):
        me_sum += (modelled[i] - observed[i])
    
    me = me_sum/n

    return me



def data_range(sample_data: np.ndarray) -> float:
    upper = max(sample_data)
    lower = min(sample_data)
    sample_range = upper - lower
    return sample_range



#TODO: Look over, not the best method of calculating with small amounts of data
def percentile(sample_data: np.ndarray, percentage: float) -> float:
    assert 0 <= percentage and percentage <= 1
    sample_data.sort()
    n = sample_data.size

    if percentage == 0.5:
        return median(sample_data)
    elif percentage == 0:
        place = 0
    else:
        place = math.ceil(percentage * n) - 1

    percentile_out = sample_data[place]

    return percentile_out



def median(sample_data: np.ndarray) -> float:
    sample_data.sort()
    
    n = sample_data.size

    if (n % 2 == 0):
        upper_med = sample_data[n // 2]
        lower_med = sample_data[(n // 2) - 1]
        med = (upper_med + lower_med) / 2
    elif (n % 2 == 1):
        med = sample_data[n // 2]
    else:
        assert False

    return med



def iqr(sample_data: np.ndarray) -> float:
    upper_quartile = percentile(sample_data, 0.75)
    lower_quartile = percentile(sample_data, 0.25)

    i_q_r = upper_quartile - lower_quartile

    return i_q_r



def mode(sample_data: np.ndarray) -> np.ndarray:
    unique_data = set(sample_data)

    most_common_value = []
    mode_count = 0

    for value in unique_data:
        value_count = (sample_data == value).sum()

        if value_count > mode_count:
            most_common_value = [value]
            mode_count = value_count
        elif value_count == mode_count:
            most_common_value.append(value)

    return np.array(most_common_value)
