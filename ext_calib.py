import numpy as np
import pickle
from scipy.linalg import svd
from utils import solve_svd

def calibrate_camera(points_3D, points_2D, video_directory):
    A = np.array([
        [
            [0,0,0,0, -z*X, -z*Y, -z*Z, -z*W, y*X, y*Y, y*Z],
            [z*X, z*Y, z*Z, z*W, 0,0,0,0, -x*X, -x*Y, -x*Z],
        ] for (X, Y, Z, W), (x, y, z) in zip(points_3D, points_2D)]).reshape(-1, 11)[:-1]
    b = np.array(([[-y*W, x*W] for (X, Y, Z, W), (x, y, z) in zip(points_3D, points_2D)])).reshape(12)[:-1]

    P = np.concatenate((solve_svd(A, b), [1])).reshape(3, 4)

    U, s, Vh = svd(P)
    C = np.around(Vh[-1, :-1] / Vh[-1, -1], 3)

    pickle.dump(P, open(f"{video_directory}/calib_params/P_matrix.pkl", "wb"))
    print('camera center:', C)
    pickle.dump(C, open(f"{video_directory}/calib_params/camera_center.pkl", "wb"))
    return P, C