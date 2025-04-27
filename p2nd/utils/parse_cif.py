import os
import gzip
from Bio.PDB import MMCIFParser
from Bio.PDB.Structure import Structure
import warnings
from Bio.PDB.PDBExceptions import PDBConstructionWarning
warnings.simplefilter('ignore', PDBConstructionWarning)


def decompress_files(download_dir) -> None:
    """
    Decompress all .cif.gz files in the specified directory.

    Parameters:
    download_dir (str): Directory where the .cif.gz files are downloaded.

    Returns:
    None
    """
    for filename in os.listdir(download_dir):
        if filename.endswith(".cif.gz"):
            compressed_file = os.path.join(download_dir, filename)
            decompressed_file = os.path.join(download_dir, filename[:-3])  # Remove .gz extension
            
            try:
                # Decompress the file
                with gzip.open(compressed_file, 'rb') as gz_file, open(decompressed_file, 'wb') as out_file:
                    out_file.write(gz_file.read())
            
                print(f"Decompressed: {compressed_file} -> {decompressed_file}")
            except Exception as e:
                print(f"Failed to decompress {compressed_file}: {e}")

def load_structures(cif_data_dir: str) -> dict[str, Structure]:
    """
    Parse decompressed .cif files using BioPython and load them as structures.
    
    Parameters:
    cif_data_dir (str): Directory containing decompressed .cif files.

    Returns:
    dict: Dictionary containing parsed structures, with structure ID as
          key and Structure object as value.
    """
    parser = MMCIFParser()
    structures = {}
    
    for filename in os.listdir(cif_data_dir):
        if filename.endswith(".cif"):  # Only process decompressed .cif files
            cif_file = os.path.join(cif_data_dir, filename)
            try:
                # Parse the structure and store it in the dictionary
                structure_id = os.path.splitext(filename)[0]  # Use filename (without extension) as ID
                structure = parser.get_structure(structure_id, cif_file)
                structures[structure_id] = structure
                print(f"Loaded structure: {structure_id}")
            except Exception as e:
                print(f"Failed to load {filename}: {e}")
    
    return structures

def load_structure(cif_file: str) -> Structure:
    """
    Load a single structure from a .cif file.

    Parameters:
    cif_file (str): Path to the .cif file.

    Returns:
    Structure: Parsed structure object.
    """
    parser = MMCIFParser()
    structure_id = os.path.splitext(os.path.basename(cif_file))[0]  # Use filename (without extension) as ID
    try:
        structure = parser.get_structure(structure_id, cif_file)
        print(f"Loaded structure: {structure_id}")
        return structure
    except Exception as e:
        print(f"Failed to load {cif_file}: {e}")
        return None

if __name__ == "__main__":
    # Directory where the .cif.gz files are downloaded
    download_dir = "data/test/mmCIF"  # Replace with your directory name if different

    # Step 1: Decompress .cif.gz files
    decompress_files(download_dir)

    # Step 2: Load structures from decompressed .cif files
    structures = load_structures(download_dir)
    
    print(f"Loaded {len(structures)} structures.")
    # Access individual structures (example)
    for structure_id, structure in structures.items():
        print(f"Structure ID: {structure_id}, Model Count: {len(structure)}")
