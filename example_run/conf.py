"""
The following config params need to be set up manually or by some other script (which we do not provide).
In our example (example_run dir) you can see how we chose the params below based on manual configuration:
* points_3D: These are arbitrary 3D points chosen from example_run/calib_params/extrinsics_marked.png
* points_2D: Corresponding to points_3D, these are the pixel values of the chosen points.
* pencil_bases_2d: The 2D coordinates of the pencil bases, taken from example_run/calib_params/pencil1.png, pencil2.png, pencil3.png
* pencil_shadow_tips_2d: The 2D coordinates of the pencil shadow tips, taken from example_run/calib_params/pencil1.png, pencil2.png, pencil3.png
* pencil_height: A pre-computed height relative to a single unit in our CS (determined by the square size in the calibration checkerboard).
* video_directory: The name of the directory where the scanning videos are stored.
"""

import numpy as np

points_3D = np.array([[0, 0, 0.7, 1], [6, 0, 0.7, 1], [5, 6, 0.7, 1], [0, 2, 1.7, 1], [0, 3, 3.7, 1], [0, 7, 2.7, 1]])
points_2D = np.array([[415, 109, 1], [1073, 144, 1], [924, 794, 1], [367, 314, 1], [286, 420, 1], [298, 897, 1]])
pencil_bases_2d = np.array([[472, 211, 1], [868, 455, 1], [1500, 226, 1]])
pencil_shadow_tips_2d = np.array([[302, 664, 1], [858, 1005, 1], [1811, 677, 1]])
pencil_height = 9
video_directory = 'example_run'
