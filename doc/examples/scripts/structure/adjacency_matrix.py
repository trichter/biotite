r"""
Construction of an adjacency matrix
===================================

In this example we create an adjacency matrix of the CA atoms in the
lysozyme crystal structure (PDB: 1AKI).
The values in the adjacency matrix ``m`` are
``m[i,j] = 1 if distance(i,j) <= threshold else 0``. 
"""

# Code source: Patrick Kunzmann
# License: BSD 3 clause

import biotite
import biotite.structure as struc
import biotite.structure.io as strucio
import biotite.database.rcsb as rcsb
import numpy as np
import matplotlib.pyplot as plt

file_name = rcsb.fetch("1aki", "mmtf", biotite.temp_dir())
array = strucio.load_structure(file_name)
# We only consider CA atoms
ca = array[array.atom_name == "CA"]
# 7 Angstrom adjacency threshold
threshold = 7
# Create adjacency map of the CA atom array
# for efficient measurement of adjacency
adjacency_map = struc.AdjacencyMap(ca, box_size=threshold)
adjacency_matrix = np.zeros(( ca.array_length(), ca.array_length()),
                            dtype=np.uint8)
for i in range(ca.array_length()):
    indices = adjacency_map.get_atoms(ca.coord[i], radius=threshold)
    adjacency_matrix[i, indices] = 1

figure = plt.figure()
ax = figure.add_subplot(111)
ax.matshow(adjacency_matrix, cmap="Greens")
plt.show()