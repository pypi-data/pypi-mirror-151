import numpy as np
from math import *


def SE3(vec6d):
    """

    :param vec6d: 指定欧拉角指定的6维姿态
    :return: 4x4的位姿矩阵
    """
    px, py, pz, rx, ry, rz = vec6d
    rx = radians(rx)
    ry = radians(ry)
    rz = radians(rz)

    rx = np.array([
        [1, 0, 0, 0],
        [0, cos(rx), -sin(rx), 0],
        [0, sin(rx), cos(rx), 0],
        [0, 0, 0, 1]
    ])

    ry = np.array([
        [cos(ry), 0, sin(ry), 0],
        [0, 1, 0, 0],
        [-sin(ry), 0, cos(ry), 0],
        [0, 0, 0, 1]
    ])

    rz = np.array([
        [cos(rz), -sin(rz), 0, 0],
        [sin(rz), cos(rz), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])

    p = np.zeros((4, 4))
    p[0:3, 0:3] = np.eye(3)
    p[0:4, 3:4] = np.reshape([px, py, pz, 1], (4, 1))

    h = p.dot(rz.dot(ry.dot(rx)))

    return np.array(h)


if __name__ == '__main__':
    H = SE3((0, 0, 100, 0, 0, 0))
    print(H)
    pass
