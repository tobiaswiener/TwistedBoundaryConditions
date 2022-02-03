import numpy as np
from scipy import linalg



a = np.random.random((1000,1000))
i = 0
while True:
    linalg.eigh(a)
    i +=1
    print(f"\r{i}")