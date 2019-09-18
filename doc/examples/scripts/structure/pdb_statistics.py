"""
Annual releases of PDB structures
=================================

This script creates a plot showing the number of annually released PDB
structures since 1990, very similar to the
`official statistics <https://www.rcsb.org/stats/growth/overall>`_.
"""

# Code source: Patrick Kunzmann
# License: BSD 3 clause

import numpy as np
import matplotlib.pyplot as plt
import biotite
import biotite.database.rcsb as rcsb 
import datetime


years = np.arange(1990, datetime.date.today().year + 1)
xray_count = np.zeros(len(years), dtype=int)
nmr_count = np.zeros(len(years), dtype=int)
em_count = np.zeros(len(years), dtype=int)
tot_count = np.zeros(len(years), dtype=int)
# For each year fetch the list of released PDB IDs
# and count the number
for i, year in enumerate(years):
    # A query that comprises one year
    date_query = rcsb.DateQuery(
        datetime.date(year,  1,  1),
        datetime.date(year, 12, 31),
        event="release"
    )
    xray_query = rcsb.MethodQuery("X-RAY")
    nmr_query = rcsb.MethodQuery("SOLUTION_NMR")
    em_query = rcsb.MethodQuery("ELECTRON MICROSCOPY")
    # Get the amount of structures, that were released in that year
    # AND were elucidated with the respective method
    xray_count[i], nmr_count[i], em_count[i] = [
        len(rcsb.search(rcsb.CompositeQuery("and", (date_query, q))))
        for q in [xray_query, nmr_query, em_query]
    ]
    # Get the total amount of structures released in that year
    tot_count[i] = len(rcsb.search(date_query))

fig, ax = plt.subplots(figsize=(8.0, 5.0))
ax.set_title("PDB release statistics")
ax.set_xlim(years[0]-1, years[-1]+1)
ax.set_xticks(years)
ax.set_xticklabels([str(y) for y in years], rotation=45)
ax.set_xlabel("Year")
ax.set_ylabel("Released structures per year")
ax.bar(
    years, xray_count,
    color=biotite.colors["darkorange"], label="X-RAY"
)
ax.bar(
    years, nmr_count, bottom=xray_count,
    color=biotite.colors["orange"], label="Solution NMR"
)
ax.bar(
    years, em_count, bottom=xray_count + nmr_count,
    color=biotite.colors["brightorange"], label="Electron Microscopy"
)
ax.bar(
    years, tot_count - xray_count - nmr_count - em_count,
    bottom=xray_count + nmr_count + em_count,
    color="gray", label="Miscellaneous"
)
ax.legend(loc="upper left")
fig.tight_layout()

plt.show()