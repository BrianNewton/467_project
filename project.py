import gurobipy as gp
from gurobipy import GRB
import numpy as np
import scipy as sp


class Bus:
    def __init__(self, type, V_pu, angle, Pg_pu, Qg_pu, Pl_pu, Ql_pu):
        self.type = type
        self.V_pu = V_pu
        self.angle = angle
        self.Pg_pu = Pg_pu
        self.Qg_pu = Qg_pu
        self.Pl_pu = Pl_pu
        self.Ql_pu = Ql_pu
    
    def set_gen(self, C0, C1, C2, Pg_max, Pg_min, Qg_max, Qg_min):
        self.C0 = C0
        self.C1 = C1
        self.C2 = C2
        self.Pg_max = Pg_max
        self.Pg_min = Pg_min
        self.Qg_max = Qg_max
        self.Qg_min = Qg_min

# [bus i][bus j][impedance/susceptance]
TLs = [[[0,0],              [0.1+0.2j, 0.04j],      [0,0],                  [0.05+0.2j, 0.04j], [0.08+0.3j, 0.06j],     [0,0]],
       [[0.1+0.2j, 0.04j],  [0,0],                  [0.05+0.25j, 0.06j],    [0.05+0.1j, 0.02j], [0.1+0.3j, 0.04j],      [0.07+0.2j, 0.05j]],
       [[0,0],              [0.05+0.25j, 0.06j],    [0,0],                  [0,0],              [0.12+0.26j, 0.05j],    [0.02+0.1j, 0.02j]],
       [[0.05+0.2j, 0.04j], [0.05+0.1j, 0.02j],     [0,0],                  [0,0],              [0.2+0.4j, 0.08j],      [0,0]],
       [[0.08+0.3j, 0.06j], [0.1+0.3j, 0.04j],      [0.12+0.26j, 0.05j],    [0.2+0.4j, 0.08j],  [0,0],                  [0.1+0.3j, 0.06j]],
       [[0,0],              [0.07+0.2j, 0.05j],     [0.02+0.1j, 0.02j],     [0,0],              [0.1+0.3j, 0.06j],      [0,0]]]

Y_bus = [[0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0]]


# Building Y_bus, B matrix and G matrix
for i in range(0, 6):
    for j in range(0, 6):
        print(i)
        Y_bus[i][i] = Y_bus[i][i] + TLs[i][j][0] + TLs[i][j][1]/2
        Y_bus[i][j] = -1*TLs[i][j][0]

B_matrix = np.imag(Y_bus)
G_matrix = np.real(Y_bus)


B_prime = (-1)*np.delete(B_matrix, 2, 1)
B_prime = np.delete(B_prime, 2, 0)

B_prime_prime = np.delete(B_prime, 0, 1)
B_prime_prime = np.delete(B_prime_prime, 0, 0)
B_prime_prime = np.delete(B_prime_prime, 0, 1)
B_prime_prime = np.delete(B_prime_prime, 0, 0)

# Setting bus data
buses = []

#bus 1
buses.append(Bus("PV", 1.05, None, 0.9, None, 0, 0))
buses[0].set_gen(300, 8, 0.0015, 150, 50, 150, -150)

#bus 2
buses.append(Bus("Slack", 1.05, 0, None, None, 0, 0))
buses[1].set_gen(450, 8, 0.0005, 200, 50, 150, -150)

#bus 3
buses.append(Bus("PV", 1.05, None, 0.6, None, 0, 0))
buses[2].set_gen(700, 7.5, 0.001, 100, 30, 150, -150)

#bus 4
buses.append(Bus("PQ", None, None, 0, 0, 0.9, 0.6))

#bus 5
buses.append(Bus("PQ", None, None, 0, 0, 1, 0.7))

#bus 6
buses.append(Bus("PQ", None, None, 0, 0, 0.9, 0.6))

#1
p1 = gp.Model("DC Load Flow without generation limits")
P = p1.addMVar(shape=5, name="P 1x5 vector")
Delta = p1.addMVar(shape=5, name="Delta 1x5 vector")

B_prime_inv = np.linalg.inv(B_prime)

obj = 300 + 450 + 700 + 8*P[0] + 8*P[1] + 7.5*P[2] + 0.0015*P[0]**2 + 0.0005*P[1]**2 + 0.001*P[2]**2
p1.setObjective(obj, GRB.MINIMIZE)

p1.addConstr(B_prime_inv @ P == Delta)

p1.optimize()

print('Optimization Complete. Objective function value: %.2f' % p1.objVal)
for v in p1.getVars():
    print('%s: %g' % (v.varName, v.x))

#2


#3


#4


#5


#6


#7


#8