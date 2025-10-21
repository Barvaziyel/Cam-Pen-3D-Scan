import numpy as np

from ext_calib import calibrate_camera
from get_shadow_edges import get_edges
from get_ts import get_ts
from lamp import get_light_source_coordinates
from triangulation import get_scene_3d
from example_run.conf import *


if __name__ == '__main__':
    # calibrate camera - find camera matrix & center
    camera_matrix, camera_center = calibrate_camera(points_3D, points_2D, video_directory)

    # find light source coordinates - using pencil
    light_source = get_light_source_coordinates(camera_matrix, pencil_bases_2d, pencil_shadow_tips_2d, pencil_height, video_directory)

    # get shadow time for each pixel
    ts = get_ts(video_directory)

    # get shadow edges for each frame
    lefts, rights = get_edges(ts, video_directory)

    # get scene in 3d
    scene3d = get_scene_3d(camera_matrix, camera_center, light_source, ts, lefts, rights, video_directory)

    print('done! use plot_scene3d.py to plot your generated scene.')
