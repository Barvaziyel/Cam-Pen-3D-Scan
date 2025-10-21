from utils import get_pickle
import matplotlib.pyplot as plt
import numpy as np


def plot_3d_scene(scene_pickle_filepath):
    points = get_pickle(scene_pickle_filepath).reshape(-1, 3)

    # Create a figure and a 3D axis
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Extract x, y, and z coordinates
    x = points[:, 0]
    y = points[:, 1]
    z = points[:, 2]

    x_mask = np.where((x!=-1) & (x<100) & (x>=-100))
    y_mask = np.where((y!=-1) & (y<100) & (y>=-100))
    z_mask = np.where((z!=-1) & (z<100) & (z>=-100))

    mask = np.intersect1d(np.intersect1d(x_mask, y_mask), z_mask)

    x, y, z = x[mask], y[mask], z[mask]

    # Plot the points
    ax.scatter(x, y, z)
    # Set labels for the axes (optional)
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')

    # Show the 3D plot
    plt.show()


if __name__ == '__main__':
    plot_3d_scene('scan_params/scene3d.pkl')