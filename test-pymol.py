import pymolPy3

# Launch pymol with GUI
pm = pymolPy3.pymolPy3()

# Load a mmCIF file
file = "data/test/mmCIF/1ash.cif"

pm(f"load {file}")

while True:
    pass
