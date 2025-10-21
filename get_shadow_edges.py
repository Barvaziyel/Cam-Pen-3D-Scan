import itertools
import os
import pickle
from tqdm import tqdm


def check_env(ts, t, i, j):
    ii = (i - 1, i, i + 1)
    jj = (j - 1, j, j + 1)
    for k, l in itertools.product(ii, jj):
        if ts[k, l] not in (t - 1, t, t + 1):
            return False
    return True


def get_edges(ts, video_directory):
    directory_path = f'{video_directory}/scan_frames/scene2'
    filenames = [os.path.join(directory_path, p) for p in sorted(os.listdir(directory_path))]
    n_frames = len(filenames)
    rights, lefts = [-1] * n_frames, [-1] * n_frames

    for t in tqdm(range(1, n_frames)):
        set = False
        for j in range(1, ts.shape[1] - 1):
            for i in range(ts.shape[0] - 2, 0, -1):
                if ts[i, j] == t and check_env(ts, t, i, j):
                    lefts[t] = i, j
                    set = True
                    break
            if set is True:
                break
        if lefts[t] != -1:
            set = False
            for j in range(ts.shape[1] - 2, 0, -1):
                for i in range(ts.shape[0] - 2, 0, -1):
                    if ts[i, j] == t and check_env(ts, t, i, j):
                        rights[t] = i, j
                        set = True
                        break
                if set is True:
                    break

    pickle.dump(lefts, open(f'{video_directory}/scan_params/lefts.pkl', 'wb'))
    pickle.dump(rights, open(f'{video_directory}/scan_params/rights.pkl', 'wb'))
    return lefts, rights
