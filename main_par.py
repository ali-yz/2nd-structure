import os
import glob
import numpy as np
from concurrent.futures import ProcessPoolExecutor, as_completed

from p2nd.utils.parse_cif import load_structure
from p2nd.utils.dssp import model_to_dssp, dssp_to_chain_labels
from p2nd.core.features import chain_to_features

# -- CONFIGURATION
INPUT_DIR = "data/dev/mmCIF"
OUTPUT_DIR = "output"
MAX_WORKERS = 5

# -- WORKER FUNCTION
def process_cif(file_path):
    pdb_id = os.path.splitext(os.path.basename(file_path))[0]
    try:
        # load
        structure = load_structure(file_path)
        model = structure[0]
        chain = next(model.get_chains(), None)
        if chain is None:
            raise ValueError(f"No chain found in model for {pdb_id}")

        # features & labels
        features = chain_to_features(chain)
        dssp     = model_to_dssp(model, in_file=file_path)
        labels   = np.array(dssp_to_chain_labels(dssp, "A"))

        if features.shape[0] != len(labels):
            raise ValueError(f"Feature/label length mismatch for {pdb_id}: "
                             f"{features.shape[0]} vs {len(labels)}")

        # ensure output dir
        os.makedirs(OUTPUT_DIR, exist_ok=True)

        # save
        f_file = os.path.join(OUTPUT_DIR, f"{pdb_id}_features.npy")
        l_file = os.path.join(OUTPUT_DIR, f"{pdb_id}_labels.npy")
        np.save(f_file, features)
        np.save(l_file, labels)

        return pdb_id, "OK"
    except Exception as e:
        return pdb_id, f"ERROR: {e}"

# -- MAIN
if __name__ == "__main__":
    # find all .cif files
    cif_paths = glob.glob(os.path.join(INPUT_DIR, "*.cif"))
    if not cif_paths:
        raise FileNotFoundError(f"No .cif files found in {INPUT_DIR}")

    # parallel dispatch
    results = []
    with ProcessPoolExecutor(max_workers=MAX_WORKERS) as exe:
        futures = { exe.submit(process_cif, path): path for path in cif_paths }
        for fut in as_completed(futures):
            pdb_id, status = fut.result()
            print(f"{pdb_id:6} → {status}")
            results.append((pdb_id, status))

    # summary
    n_ok    = sum(1 for _,s in results if s=="OK")
    n_fail  = len(results) - n_ok
    print(f"\nProcessed {len(results)} files: {n_ok} succeeded, {n_fail} failed.")
