# p2nd.core.features.py

import numpy as np


def chain_to_ca_array(chain):
    """
    Convert a chain to a numpy array of C-alpha coordinates. Pass where there is no C-alpha atom.

    :param chain: A Bio.PDB Chain object
    :return: A numpy array of C-alpha coordinates.
    """
    ca_coords = []
    for residue in chain:
        if residue.has_id('CA'):
            ca_coords.append(residue['CA'].get_coord())
        else:
            pass
    return np.array(ca_coords)

def ca_array_to_distances_features(ca_array: np.array):
    """
    Convert a C-alpha array to a 3d tensor of distance between C-alpha atoms.

    There are 6 features for each residue:
    1. d(ca[i-2], ca[i])
    2. d(ca[i], ca[i+2])
    3. d(ca[i-1], ca[i+1])
    4. d(ca[i-1], ca[i+2])
    5. d(ca[i-2], ca[i+2])
    6. d(ca[i-2], ca[i+1])

    The non applicable fields for two ends of chain are set to 0.


    :param ca_array: A numpy array of C-alpha coordinates.

    :return: A 3d tensor of distances.
    """

    n_residues = ca_array.shape[0]
    n_features = 6
    distances = np.zeros((n_residues, n_features))

    for i in range(n_residues):
        if i - 2 >= 0:
            distances[i, 0] = np.linalg.norm(ca_array[i] - ca_array[i - 2])
        if i + 2 < n_residues:
            distances[i, 1] = np.linalg.norm(ca_array[i] - ca_array[i + 2])
        if i - 1 >= 0 and i + 1 < n_residues:
            distances[i, 2] = np.linalg.norm(ca_array[i - 1] - ca_array[i + 1])
        if i - 1 >= 0 and i + 2 < n_residues:
            distances[i, 3] = np.linalg.norm(ca_array[i - 1] - ca_array[i + 2])
        if i - 2 >= 0 and i + 2 < n_residues:
            distances[i, 4] = np.linalg.norm(ca_array[i - 2] - ca_array[i + 2])
        if i - 2 >= 0 and i + 1 < n_residues:
            distances[i, 5] = np.linalg.norm(ca_array[i - 2] - ca_array[i + 1])

    return distances

def ca_array_to_angle_features(ca_array: np.array):
    """
    Convert a C-alpha array to a 3d tensor of angles between C-alpha atoms.

    There are 6 features for each residue:
    1. angle(ca[i-2], ca[i], ca[i+2])
    2. angle(ca[i-1], ca[i], ca[i+1])
    3. angle(ca[i-1], ca[i], ca[i-2])
    4. angle(ca[i], ca[i-1], ca[i-2])
    5. angle(ca[i], ca[i+1], ca[i+2])
    6. angle(ca[i+1], ca[i], ca[i+2])

    The non applicable fields for two ends of chain are set to 0.

    :param ca_array: A numpy array of C-alpha coordinates.

    :return: A 3d tensor of angles in radians.
    """
    n_residues = ca_array.shape[0]
    n_features = 6
    angles = np.zeros((n_residues, n_features))

    for i in range(n_residues):
        if i - 2 >= 0 and i + 2 < n_residues:
            angles[i, 0] = np.arccos(np.clip(np.dot(ca_array[i - 2] - ca_array[i], ca_array[i + 2] - ca_array[i]) /
                                              (np.linalg.norm(ca_array[i - 2] - ca_array[i]) *
                                               np.linalg.norm(ca_array[i + 2] - ca_array[i])), -1.0, 1.0))
        if i - 1 >= 0 and i + 1 < n_residues:
            angles[i, 1] = np.arccos(np.clip(np.dot(ca_array[i - 1] - ca_array[i], ca_array[i + 1] - ca_array[i]) /
                                              (np.linalg.norm(ca_array[i - 1] - ca_array[i]) *
                                               np.linalg.norm(ca_array[i + 1] - ca_array[i])), -1.0, 1.0))
        if i - 2 >= 0 and i + 1 < n_residues:
            angles[i, 2] = np.arccos(np.clip(np.dot(ca_array[i - 2] - ca_array[i], ca_array[i + 1] - ca_array[i]) /
                                              (np.linalg.norm(ca_array[i - 2] - ca_array[i]) *
                                               np.linalg.norm(ca_array[i + 1] - ca_array[i])), -1.0, 1.0))
        if i >= 2:
            angles[i, 3] = np.arccos(np.clip(np.dot(ca_array[i] - ca_array[i - 1], ca_array[i - 2] - ca_array[i]) /
                                              (np.linalg.norm(ca_array[i] - ca_array[i - 1]) *
                                               np.linalg.norm(ca_array[i - 2] - ca_array[i])), -1.0, 1.0))
        if i + 2 < n_residues:
            angles[i, 4] = np.arccos(np.clip(np.dot(ca_array[i] - ca_array[i + 1], ca_array[i + 2] - ca_array[i]) /
                                              (np.linalg.norm(ca_array[i] - ca_array[i + 1]) *
                                               np.linalg.norm(ca_array[i + 2] - ca_array[i])), -1.0, 1.0))
        if i + 1 < n_residues and i + 2 < n_residues:
            angles[i, 5] = np.arccos(np.clip(np.dot(ca_array[i + 1] - ca_array[i], ca_array[i + 2] - ca_array[i]) /
                                              (np.linalg.norm(ca_array[i + 1] - ca_array[i]) *
                                               np.linalg.norm(ca_array[i + 2] - ca_array[i])), -1.0, 1.0))
    return angles

def ca_array_to_dihedral_features(ca_array: np.array):
    """
    Convert a C-alpha array to a 3d tensor of dihedral angles between C-alpha atoms.

    There are 6 features for each residue:
    1. dihedral(ca[i-2], ca[i-1], ca[i], ca[i+1])
    2. dihedral(ca[i-1], ca[i], ca[i+1], ca[i+2])

    The non applicable fields for two ends of chain are set to 0.

    :param ca_array: A numpy array of C-alpha coordinates.

    :return: A 3d tensor of angles in radians.
    """
    n_residues = ca_array.shape[0]
    n_features = 2
    dihedrals = np.zeros((n_residues, n_features))

    for i in range(n_residues):
        if i - 2 >= 0 and i + 1 < n_residues:
            b1 = ca_array[i - 2] - ca_array[i - 1]
            b2 = ca_array[i] - ca_array[i - 1]
            b3 = ca_array[i + 1] - ca_array[i]
            normal1 = np.cross(b1, b2)
            normal2 = np.cross(b2, b3)
            dihedrals[i, 0] = np.arctan2(np.linalg.norm(np.cross(normal1, normal2)), np.dot(normal1, normal2))
        if i - 1 >= 0 and i + 2 < n_residues:
            b1 = ca_array[i - 1] - ca_array[i]
            b2 = ca_array[i + 1] - ca_array[i]
            b3 = ca_array[i + 2] - ca_array[i + 1]
            normal1 = np.cross(b1, b2)
            normal2 = np.cross(b2, b3)
            dihedrals[i, 1] = np.arctan2(np.linalg.norm(np.cross(normal1, normal2)), np.dot(normal1, normal2))

    return dihedrals

def ca_array_to_proximity_features(ca_array: np.array):
    """
    Number and average distance and average residue distance of neighbors within a cutoff of 4.5A, 8A, 12A.

    Features:
    1. Number of neighbors within 4.5A
    2. Number of neighbors within 8A
    3. Number of neighbors within 12A
    4. Average distance of neighbors within 4.5A
    5. Average distance of neighbors within 8A
    6. Average distance of neighbors within 12A
    7. Average residue distance of neighbors within 4.5A
    8. Average residue distance of neighbors within 8A
    9. Average residue distance of neighbors within 12A

    :param ca_array: A numpy array of C-alpha coordinates.
    :return: A 3d tensor of distances.
    """
    n_residues = ca_array.shape[0]
    n_features = 9
    proximity = np.zeros((n_residues, n_features))

    cutoff = [4.5, 8.0, 12.0]

    for i in range(n_residues):
        for j in range(n_residues):
            if i != j:
                dist = np.linalg.norm(ca_array[i] - ca_array[j])
                for k in range(len(cutoff)):
                    if dist < cutoff[k]:
                        proximity[i, k] += 1
                        proximity[i, k + 3] += dist
                        proximity[i, k + 6] += np.abs(i - j)

    for i in range(n_residues):
        for k in range(len(cutoff)):
            if proximity[i, k] > 0:
                proximity[i, k + 3] /= proximity[i, k]
                proximity[i, k + 6] /= proximity[i, k]

    return proximity

def chain_to_features(chain):
    """
    Convert a chain to a 3d tensor of features.

    :param chain: A Bio.PDB Chain object
    :return: A 3d tensor of features.
    """
    ca_array = chain_to_ca_array(chain)
    distances = ca_array_to_distances_features(ca_array)
    angles = ca_array_to_angle_features(ca_array)
    dihedrals = ca_array_to_dihedral_features(ca_array)
    proximity = ca_array_to_proximity_features(ca_array)

    features = np.concatenate((distances, angles, dihedrals, proximity), axis=1)
    return features
