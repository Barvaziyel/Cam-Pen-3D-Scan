import itertools
import os
import numpy as np
from tqdm import tqdm
from utils import get_frame, I_THRESH
import pickle


def abs_diff(a, b):
    return np.abs(a.astype(int) - b.astype(int)).astype(np.uint8)


def get_ts(video_directory):
    directory_path = f'{video_directory}/scan_frames/scene2'
    filenames = [os.path.join(directory_path, p) for p in sorted(os.listdir(directory_path))]
    n_frames = len(filenames)

    frame = get_frame(filenames[0])
    im_shape = frame.shape
    ts = np.ones(im_shape) * -1
    imax = np.copy(frame)

    for t, filename in tqdm(enumerate(filenames, start=1), total=n_frames - 1):
        frame = get_frame(filename)
        diff = abs_diff(imax, frame)
        for i, j in itertools.product(range(im_shape[0]), range(im_shape[1])):
            if ts[i, j] == -1 and diff[i, j] > I_THRESH:
                ts[i, j] = t

    pickle.dump(ts, open(f"{video_directory}/scan_params/ts.pkl", "wb"))
    return ts
