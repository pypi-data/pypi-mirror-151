from MathExp import *
import numpy as np

H = SE3([10, 20, 15, 10, 20, 30])

print(f'H\r\n{H}')
print(f'H\r\n{np.linalg.inv(H)}')
print(f'H\r\n{H.T}')
print(f'H.T\r\n{np.linalg.inv(H) - H.T}')

H1 = SE3([1, 0, 0, 0, 0, 0])
H2 = H1.dot(H)

print(f'H2\r\n{H2}')
pass
