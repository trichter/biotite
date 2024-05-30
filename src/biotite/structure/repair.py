# This source code is part of the Biotite package and is distributed
# under the 3-Clause BSD License. Please see 'LICENSE.rst' for further
# information.

"""
This module contains functionalities for repairing malformed structures.
"""

__name__ = "biotite.structure"
__author__ = "Patrick Kunzmann"
__all__ = ["renumber_atom_ids", "renumber_res_ids",
           "create_continuous_res_ids"]

import warnings
import numpy as np
from .residues import get_residue_starts
from .chains import get_chain_starts


def renumber_atom_ids(array, start=None):
    """
    Renumber the atom IDs of the given array.

    DEPRECATED.

    Parameters
    ----------
    array : AtomArray or AtomArrayStack
        The array to be checked.
    start : int, optional
        The starting index for renumbering.
        The first ID in the array is taken by default.

    Returns
    -------
    array : AtomArray or AtomArrayStack
        The renumbered array.
    """
    warnings.warn(
      "'renumber_atom_ids()' is deprecated",
        DeprecationWarning
    )
    if "atom_id" not in array.get_annotation_categories():
        raise ValueError("The atom array must have the 'atom_id' annotation")
    if start is None:
        start = array.atom_id[0]
    array = array.copy()
    array.atom_id = np.arange(start, array.shape[-1]+1)
    return array


def renumber_res_ids(array, start=None):
    """
    Renumber the residue IDs of the given array, so that are continuous.

    DEPRECATED: Use :func:`create_continuous_res_ids()`instead.

    Parameters
    ----------
    array : AtomArray or AtomArrayStack
        The array to be checked.
    start : int, optional
        The starting index for renumbering.
        The first ID in the array is taken by default.

    Returns
    -------
    array : AtomArray or AtomArrayStack
        The renumbered array.
    """
    warnings.warn(
      "'renumber_res_ids()' is deprecated, use 'create_continuous_res_ids()'",
        DeprecationWarning
    )
    if start is None:
        start = array.res_id[0]
    diff = np.diff(array.res_id)
    diff[diff != 0] = 1
    new_res_ids =  np.concatenate(([start], diff)).cumsum()
    array = array.copy()
    array.res_id = new_res_ids
    return array


def create_continuous_res_ids(atoms, restart_each_chain=True):
    """
    Create an array of continuous residue IDs for a given structure.

    This means that residue IDs are incremented by 1 for each residue.

    Parameters
    ----------
    atoms : AtomArray or AtomArrayStack
        The atoms for which the continuous residue IDs should be created.
    restart_each_chain : bool, optional
        If true, the residue IDs are reset to 1 for each chain.

    Returns
    -------
    res_ids : ndarray, dtype=int
        The continuous residue IDs.

    Examples
    --------

    >>> # Remove a residue to make the residue IDs discontinuous
    >>> atom_array = atom_array[atom_array.res_id != 5]
    >>> res_ids, _ = get_residues(atom_array)
    >>> print(res_ids)
    [ 1  2  3  4  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20]
    >>> atom_array.res_id = create_continuous_res_ids(atom_array)
    >>> res_ids, _ = get_residues(atom_array)
    >>> print(res_ids)
    [ 1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19]

    """
    res_ids_diff = np.zeros(atoms.array_length(), dtype=int)
    res_starts = get_residue_starts(atoms)
    res_ids_diff[res_starts] = 1
    res_ids = np.cumsum(res_ids_diff)

    if restart_each_chain:
        chain_starts = get_chain_starts(atoms)
        for start in chain_starts:
            res_ids[start:] -= res_ids[start] - 1

    return res_ids
