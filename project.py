import gurobipy as gp
import numpy as np


# [bus i][bus j][impedance/susceptance]
TLs = [[0, [np.imag(0.1+0.2j), np.imag(0.04j)], 0, [np.imag(0.05+0.2j), np.imag(0.04j)], [np.imag(0.08+0.3j), np.imag(0.06j)], 0],
       [[np.imag(0.1+0.2j), np.imag(0.04j)], 0, [np.imag(0.05+0.25j), np.imag(0.06j)], [np.imag(0.05+0.1j), np.imag(0.02j)], [np.imag(0.1+0.3j), np.imag(0.04j)], [np.imag(0.07+0.2j), np.imag(0.05j)]],
       [0, [np.imag(0.05+0.25j), np.imag(0.06j)], 0, 0, [np.imag(0.12+0.26j), np.imag(0.05j)], [np.imag(0.02+0.1j), np.imag(0.02j)]],
       [[np.imag(0.05+0.2j), np.imag(0.04j)], [np.imag(0.05+0.1j), np.imag(0.02j)], 0, 0, [np.imag(0.2+0.4j), np.imag(0.08j)], 0],
       [[np.imag(0.08+0.3j), np.imag(0.06j)], [np.imag(0.1+0.3j), np.imag(0.04j)], [np.imag(0.12+0.26j), np.imag(0.05j)], [np.imag(0.2+0.4j), np.imag(0.08j)], 0, [np.imag(0.1+0.3j), np.imag(0.06j)]],
       [0, [np.imag(0.07+0.2j), np.imag(0.05j)], [np.imag(0.02+0.1j), np.imag(0.02j)], 0, [np.imag(0.1+0.3j), np.imag(0.06j)], 0]]

