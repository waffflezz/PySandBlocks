import numpy as np


def obj_to_vf(filename):
    vertex, faces = [], []
    with open(filename) as f:
        for line in f:
            if line.startswith('v '):
                vertex.append(np.array([float(i) for i in line.split()[1:]]))
            elif line.startswith('f'):
                faces_ = line.split()[1:]
                faces.append(
                    [int(face_.split('/')[0]) - 1 for face_ in faces_])
    return vertex, faces
