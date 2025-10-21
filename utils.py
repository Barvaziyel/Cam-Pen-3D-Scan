import os
import pickle

from PIL import Image
from scipy.linalg import svd
import numpy as np


I_THRESH = 70


def solve_svd(A, b):
    """
    return x s.t Ax=b (as close as possible using least squares minimization)
    """
    # compute svd decomposition of A
    U, s, Vh = svd(A)
    # U diag(s) Vh x = b ==> diag(s) Vh x = Uh b = c
    # (since U is orthogonal, Ut = U-1)
    c = np.dot(U.conj().T, b)
    # ==> Vh x = diag(1/s) c = w
    w = np.dot(np.diag(1/s), c)
    # ==> x = V w (= V diag(1/s) Uh b)
    x = np.dot(Vh.conj().T, w)
    return x


def floor2d_to_3d(camera_matrix, p, homogeneous=True):
    """
    This function is used to convert 2d points to 3d points, assuming the points are on Z=0 (so only X,Y need to be found).
    """
    A = camera_matrix[:2, :2]  # rotation in xy
    b = p - camera_matrix[:2, 3]  # translation in xy
    X, Y = solve_svd(A, b)
    return np.array([X, Y, 0, 1]) if homogeneous else np.array([X, Y, 0])


def plane_eq(X1, X2, X3):
    plane012 = np.cross(X1-X3, X2-X3)
    plane3 = -X3.T@(np.cross(X1,X2))
    return np.concatenate((plane012, [plane3]))


def get_frame(file_path):
    image = Image.open(file_path)
    grayscale_image = image.convert('L')
    grayscale_array = np.array(grayscale_image)
    return grayscale_array


def get_pickle(path):
    with open(path, 'rb') as f:
        pkl = pickle.load(f)
    return pkl
