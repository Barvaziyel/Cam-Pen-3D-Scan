# given a, b and some point p on the shadow line, we can find p's 3d location
import itertools
import pickle

import numpy as np
from tqdm import tqdm

from utils import floor2d_to_3d, plane_eq


def get_scene_3d(camera_matrix, camera_center, light_source, ts, lefts, rights, video_directory):
    def find_pixel_3d_location(x, y):
        t = int(ts[x, y])
        if t == -1 or t >= len(lefts):
            return -1, -1, -1
        a, b = lefts[t], rights[t]
        A, B = floor2d_to_3d(camera_matrix, a, homogeneous=False), floor2d_to_3d(camera_matrix, b, homogeneous=False)
        point3d = floor2d_to_3d(camera_matrix, (x, y), homogeneous=False)
        shadow_plane = plane_eq(A, B, light_source)

        # to find intersection between line and plane:
        # if plane is defined by normal N = (a,b,c) and point pp
        # and line is defined by point pl and vector d s.t. pl + t*d defines any point on it
        # then p0 = pl + t0*d lies on the plane iff p0 - pp is orthogonal to N
        # iff dot(N, pl + t0*d - pp) = 0
        # iff dot(N, pl - pp) + t0 * dot(N, d) = 0
        # iff t0 = -dot(N, pl - pp) / dot(N, d)
        # after finding t0, we can substitute in line eq to get the point.

        N, pp = shadow_plane[:3], light_source
        pl, d = camera_center, point3d - camera_center
        t0 = -np.dot(N, pl - pp) / np.dot(N, d)
        point = pl + t0 * d
        return point

    scene3d = np.ones((*ts.shape, 3)) * -1

    for i, j in tqdm(itertools.product(range(1, ts.shape[0] - 1), range(1, ts.shape[1] - 1)),
                     total=(ts.shape[0] - 2) * (ts.shape[1] - 2)):
        scene3d[i, j] = find_pixel_3d_location(i, j)

    scene3d = scene3d.reshape(-1, 3)
    x = scene3d[:, 0]
    y = scene3d[:, 1]
    z = scene3d[:, 2]
    x_mask = np.where(x!=-1)
    y_mask = np.where(y!=-1)
    z_mask = np.where(z!=-1)
    mask = np.intersect1d(np.intersect1d(x_mask, y_mask), z_mask)
    x, y, z = x[mask], y[mask], z[mask]
    scene3d = np.vstack((x, y, z)).T

    pickle.dump(scene3d, open(f'{video_directory}/scan_params/scene3d.pkl', 'wb'))
    return scene3d
