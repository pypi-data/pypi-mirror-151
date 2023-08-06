import numpy as np

from statistical_methods.basics import *



#TODO: Check that the denominator value here is correct, is it biased is it not?
def semivariance(sample_data: np.ndarray, maximum_value = 0) -> float:
    use_data = sample_data[sample_data < maximum_value]
    n = use_data.size
    assert n > 0

    semivar = variance(use_data)

    return semivar



def simple_return() -> float:
    return 0



def compound_return() -> float:
    return 0