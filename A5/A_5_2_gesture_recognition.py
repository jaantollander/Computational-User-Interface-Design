import os
from typing import Dict, List

import numpy as np
from numpy.linalg import norm

import matplotlib.pyplot as plt
import seaborn as sns


def parse(filepath) -> Dict[str, List[float]]:
    """Parses a leap motion data from csv file into a dictionary."""
    d = dict()
    with open(filepath, mode='r') as f:
        for line in f:
            v = line.strip('\n').split(',')
            d[v[0]] = list(map(float, v[1:]))
    return d


def angle(v1, v2):
    return np.arccos(np.dot(v1, v2) / (norm(v1) * norm(v2)))


def to_col(v1):
    return v1.reshape((len(v1), 1))


def feature_vector(data):
    # Position of the finger tips
    F = np.array(data["FingertipsPositions"]).reshape((5, 3))

    # Set missing values (vector F[i] is zero vector) to nan.
    for i in range(len(F)):
        if norm(F[i]) == 0:
            F[i, :] = np.nan

    # Palm center
    C = np.array(data["PalmPosition"])

    # Orientation unit vectors
    n = np.array(data["HandDirection"])
    h = np.array(data["PalmNormal"])

    # Index of the middle finger
    middle = 2

    # Scale factor
    S = norm(F[middle]-C)

    # Projection of F to n
    F_pi = to_col(np.dot(F, n.T)) * n

    # Fingertips angle
    A = np.array(list(angle(F_pi_i-C, h) for F_pi_i in F_pi))

    # Fingertips distance
    D = norm(F-C, axis=1) / S

    # Fingertips elevation
    E = np.sign(np.dot((F-F_pi), n)) * norm(F-F_pi, axis=1) / S

    return np.hstack((A, D, E))


def features_and_labels(gesture_path="gesture_set"):
    features = []
    labels = []
    label_convert = {"G4": 4, "G5": 5}
    for dirpath, _, filenames in os.walk(gesture_path):
        for filename in filenames:
            _, _, label = dirpath.split('/')
            data = parse(os.path.join(dirpath, filename))
            features.append(feature_vector(data))
            labels.append(label_convert[str(label)])
    return np.array(features), np.array(labels)


def distplot(features, labels):
    feature_names = [f'A_{i}' for i in range(5)] + \
                    [f'D_{i}' for i in range(4)] + \
                    [f'E_{i}' for i in range(5)]
    sns.set()
    for i, name in enumerate(feature_names):
        plt.figure()
        plt.title(f"${name}$")
        sns.distplot([f[i] for (f, l) in zip(features, labels) if l == 4],
                     label="Feature 4", kde=False, bins=20)
        sns.distplot([f[i] for (f, l) in zip(features, labels) if l == 5],
                     label="Feature 5", kde=False, bins=20)
        plt.legend()
        plt.show()


features, labels = features_and_labels()
# TODO: scale A to interval [0.5, 1]
# TODO: scale E to interval [0.5, 1]
features[np.isnan(features)] = 0.0  # Set missing values to 0
distplot(features, labels)


# participant = "P1"
# label = "G4"
# filename = "1_leap_motion.csv"
# filepath = os.path.join("gesture_set", participant, label, filename)
# data = parse(filepath)
# A, D, E = feature_vector(data)
