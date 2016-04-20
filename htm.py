# testing

import numpy as np

a = np.arange(8).reshape((2,2,2))
print(a)

# 1D input array
# 1D region array

# Potential Pool
# columns_connections_locations = random.sample a "percentage of size" of array
# columns_connections_permanance = 0.0
# repeat for all columns

# Overlap Score
# for column in columns: overlap_score = sum(potential_pool[column])
# select top 2% columns with highest overlap scores

# Learning
# if input connected and 1: permanance += value
# if input connected and 0: permanance -= value


# reshape 1D region array to 3D region array
