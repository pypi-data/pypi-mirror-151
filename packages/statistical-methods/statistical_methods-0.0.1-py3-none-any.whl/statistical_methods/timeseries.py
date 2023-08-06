import math
import numpy as np

from basics import *



def difference(series, order = 1, step = 1):
    n = series.size

    dif_number = math.floor((n-order)/step)
    assert dif_number >= 1

    if order == 1:
        dif = np.array([0]*math.floor((n-1)/step))
        
        for i in range(math.floor((n-1)/step)):
            dif[i] = series[i+step] - series[i]
    elif order > 1:
        temp_dif = np.array([0]*math.floor((n-1)/step))
        
        for i in range(math.floor((n-1)/step)):
            temp_dif[i] = series[i+step] - series[i]
        dif = difference(temp_dif, order = order-1, step = step)
    else:
        assert False

    return dif
