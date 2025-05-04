import os
import numpy as np
from p2nd.utils.parse_cif import load_structure
from p2nd.utils.dssp import model_to_dssp, dssp_to_chain_labels
from p2nd.core.features import chain_to_features

file_prefix = "data/dev/mmCIF/"
pdb_id = "1mi1"
file_path = os.path.join(file_prefix, f"{pdb_id}.cif")

output_dir = "output/"

if not os.path.exists(file_path):
    raise FileNotFoundError(f"File {file_path} does not exist.")

structure = load_structure(file_path)
model = structure[0]
chain = next(model.get_chains(), None)
features = chain_to_features(chain)
dssp = model_to_dssp(model, in_file=file_path)
labels = dssp_to_chain_labels(dssp, "A")

print(f"Features shape: {features.shape}")
print(f"Labels shape: {len(labels)}")

labels = np.array(labels)

# Check if the length of features and labels match
if features.shape[0] != len(labels):
    raise ValueError("The number of features and labels do not match.")

# write the features and labels to files
features_file = os.path.join(output_dir, f"{pdb_id}_features.npy")
labels_file = os.path.join(output_dir, f"{pdb_id}_labels.npy")

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

np.save(features_file, features)
print(f"Features saved to {features_file}")
np.save(labels_file, labels)
print(f"Labels saved to {labels_file}")

print()
