import pickle
import numpy as np
from utils import floor2d_to_3d


def get_light_source_coordinates(camera_matrix, pencil_bases_2d, pencil_shadow_tips_2d, pencil_height, video_directory):
    # find pencil bases and shadow tips in 3D
    Ks = np.array([floor2d_to_3d(camera_matrix, pencil_bases_2d[0, :2]),
                   floor2d_to_3d(camera_matrix, pencil_bases_2d[1, :2]),
                   floor2d_to_3d(camera_matrix, pencil_bases_2d[2, :2])])
    Tss = np.array([floor2d_to_3d(camera_matrix, pencil_shadow_tips_2d[0, :2]),
                    floor2d_to_3d(camera_matrix, pencil_shadow_tips_2d[1, :2]),
                    floor2d_to_3d(camera_matrix, pencil_shadow_tips_2d[2, :2])])
    # pencil tips are free with known pencil height
    Ts = Ks + np.array([0, 0, pencil_height, 0])

    # assuming lines on floor are 2d, we'll find their intersection as the x,y coords of the light source
    line1 = np.cross(np.concatenate((Tss[0,:2], [1])), np.concatenate((Ks[0,:2], [1])))
    line2 = np.cross(np.concatenate((Tss[1,:2], [1])), np.concatenate((Ks[1,:2], [1])))
    line3 = np.cross(np.concatenate((Tss[2,:2], [1])), np.concatenate((Ks[2,:2], [1])))
    p1 = np.cross(line1, line2) / np.cross(line1, line2)[-1]
    p2 = np.cross(line3, line2) / np.cross(line3, line2)[-1]
    p3 = np.cross(line1, line3) / np.cross(line1, line3)[-1]

    xs = [p1[0], p2[0], p3[0]]
    points = [p1, p2, p3]
    for i in range(3):
        d = Ts[0] - Tss[0]
        p = Tss[0]
        t = (xs[i] - p[0]) / d[0]
        points[i][2] = p[2] + t*d[2]

    intersection = np.mean(points, axis=0)
    print('light source:', intersection)
    pickle.dump(intersection, open(f'{video_directory}/calib_params/light.pkl', "wb"))
    return intersection
