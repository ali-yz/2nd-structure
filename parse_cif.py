import os
import gzip
from Bio.PDB import MMCIFParser

def decompress_files(download_dir):
    """
    Decompress all .cif.gz files in the specified directory.
    """
    for filename in os.listdir(download_dir):
        if filename.endswith(".cif.gz"):
            compressed_file = os.path.join(download_dir, filename)
            decompressed_file = os.path.join(download_dir, filename[:-3])  # Remove .gz extension
            
            # Decompress the file
            with gzip.open(compressed_file, 'rb') as gz_file, open(decompressed_file, 'wb') as out_file:
                out_file.write(gz_file.read())
            
            print(f"Decompressed: {compressed_file} -> {decompressed_file}")

def load_structures(download_dir):
    """
    Parse decompressed .cif files using BioPython and load them as structures.
    """
    parser = MMCIFParser()
    structures = {}
    
    for filename in os.listdir(download_dir):
        if filename.endswith(".cif"):  # Only process decompressed .cif files
            cif_file = os.path.join(download_dir, filename)
            try:
                # Parse the structure and store it in the dictionary
                structure_id = os.path.splitext(filename)[0]  # Use filename (without extension) as ID
                structure = parser.get_structure(structure_id, cif_file)
                structures[structure_id] = structure
                print(f"Loaded structure: {structure_id}")
            except Exception as e:
                print(f"Failed to load {filename}: {e}")
    
    return structures

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
