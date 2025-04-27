import numpy as np
import matplotlib.pyplot as plt
from Bio.PDB.vectors import calc_dihedral

# TODO: Replace with actual data loading
dev_data = None

# Extract chains from the provided dictionary
protein_structure = dev_data['1a4e']

phi_psi_angles = []

# Loop through chains
for chain in protein_structure.get_chains():
    residues = list(chain.get_residues())
    
    for i in range(1, len(residues) - 1):  # Avoid first & last residue
        try:
            # Extract relevant backbone atoms
            prev_C = residues[i - 1]['C'].get_vector()
            N = residues[i]['N'].get_vector()
            CA = residues[i]['CA'].get_vector()
            C = residues[i]['C'].get_vector()
            next_N = residues[i + 1]['N'].get_vector()
            
            # Calculate dihedral angles
            phi = np.degrees(calc_dihedral(prev_C, N, CA, C))
            psi = np.degrees(calc_dihedral(N, CA, C, next_N))
            
            phi_psi_angles.append((phi, psi))
        except KeyError:
            # Skip residues missing backbone atoms
            continue

# Convert to NumPy array for plotting
phi_psi_angles = np.array(phi_psi_angles)

# Plot Ramachandran plot
plt.figure(figsize=(6, 6))
plt.scatter(phi_psi_angles[:, 0], phi_psi_angles[:, 1], s=10, alpha=0.5)
plt.xlim(-180, 180)
plt.ylim(-180, 180)
plt.xlabel("Phi (φ) Angle (°)")
plt.ylabel("Psi (ψ) Angle (°)")
plt.title("Ramachandran Plot")
plt.grid(True)
plt.show()


import numpy as np
import matplotlib.pyplot as plt
from Bio.PDB.vectors import calc_dihedral

# Extract chains from the provided dictionary
# protein_structure = dev_data['1a4e']

phi_psi_angles = []

for protein_structure in dev_data.values():
    # Loop through chains
    for chain in protein_structure.get_chains():
        residues = list(chain.get_residues())
        
        for i in range(1, len(residues) - 1):  # Avoid first & last residue
            # only prolines
            if not (residues[i+1].get_resname() == "PRO"):
                continue
            try:
                # Extract relevant backbone atoms
                prev_C = residues[i - 1]['C'].get_vector()
                N = residues[i]['N'].get_vector()
                CA = residues[i]['CA'].get_vector()
                C = residues[i]['C'].get_vector()
                next_N = residues[i + 1]['N'].get_vector()
                
                # Calculate dihedral angles
                phi = np.degrees(calc_dihedral(prev_C, N, CA, C))
                psi = np.degrees(calc_dihedral(N, CA, C, next_N))
                
                phi_psi_angles.append((phi, psi))
            except KeyError:
                # Skip residues missing backbone atoms
                continue

# Convert to NumPy array for plotting
phi_psi_angles = np.array(phi_psi_angles)

# Plot Ramachandran plot
plt.figure(figsize=(6, 6))
plt.scatter(phi_psi_angles[:, 0], phi_psi_angles[:, 1], s=3, alpha=0.2)
plt.xlim(-180, 180)
plt.ylim(-180, 180)
plt.xlabel("Phi (φ) Angle (°)")
plt.ylabel("Psi (ψ) Angle (°)")
plt.title("Ramachandran Plot")
plt.grid(True)
plt.show()
