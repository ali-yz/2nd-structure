# 2nd-structure

Model-Free Assignment of Protein Secondary Structure using Structural Encoding

# Installation
I used uv for python dependency management.

```
uv install
```

If you need the PyMol visualization, you need to install it separately and add it to PATH. Example on MacOS:

```
brew install pymol
```


## How Each Part Works

### PDB Download Script

Make it executable:

```
chmod +x pdb_download.sh
```

Run it with the required arguments:

```
./pdb_download.sh pdb_ids.txt pdb_urls.txt mmCIF 10
```

*   `**<input_file>**`: File containing the list of PDB IDs (\\n separated) (e.g., `pdb_ids.txt`).
*   `**<output_file>**`: File to save generated URLs (e.g., `pdb_urls.txt`).
*   `**<download_dir>**`: Directory to download files (e.g., `mmCIF`).
*   `**<parallel_downloads>**`: Number of parallel downloads (e.g., `10`).