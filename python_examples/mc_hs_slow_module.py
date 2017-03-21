#!/usr/bin/env python3
# mc_hs_slow_module.py

#------------------------------------------------------------------------------------------------#
# This software was written in 2016/17                                                           #
# by Michael P. Allen <m.p.allen@warwick.ac.uk>/<m.p.allen@bristol.ac.uk>                        #
# and Dominic J. Tildesley <dominic.tildesley@epfl.ch> ("the authors"),                          #
# to accompany the book "Computer Simulation of Liquids", second edition, 2017 ("the text"),     #
# published by Oxford University Press ("the publishers").                                       #
#                                                                                                #
# LICENCE                                                                                        #
# Creative Commons CC0 Public Domain Dedication.                                                 #
# To the extent possible under law, the authors have dedicated all copyright and related         #
# and neighboring rights to this software to the PUBLIC domain worldwide.                        #
# This software is distributed without any warranty.                                             #
# You should have received a copy of the CC0 Public Domain Dedication along with this software.  #
# If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.                               #
#                                                                                                #
# DISCLAIMER                                                                                     #
# The authors and publishers make no warranties about the software, and disclaim liability       #
# for all uses of the software, to the fullest extent permitted by applicable law.               #
# The authors and publishers do not recommend use of this software for any purpose.              #
# It is made freely available, solely to clarify points made in the text. When using or citing   #
# the software, you should not imply endorsement by the authors or publishers.                   #
#------------------------------------------------------------------------------------------------#

"""Energy and move routines for MC simulation, LJ potential. Slow version using Python loop."""

def introduction():
    """Prints out introductory statements at start of run."""

    print('Hard sphere potential')
    print('Diameter, sigma = 1')
    print('Energy, kT = 1')
    print('Slow version built around Python loops')

def conclusion():
    """Prints out concluding statements at end of run."""

    print('Program ends')

def overlap ( box, r ):
    """Takes in box and coordinate array, and signals any overlap."""

    # Actual calculation is performed by function overlap_1

    n, d = r.shape
    assert d==3, 'Dimension error for r in overlap'

    for i in range(n-1):
        if overlap_1 ( r[i,:], box, r[i+1:,:] ):
            return True # Immediate return on detection of overlap

    return False

def overlap_1 ( ri, box, r ):
    """Takes in coordinates of an atom and signals any overlap.

    Values of box and partner coordinate array are supplied.
    """

    import numpy as np

    # In general, r will be a subset of the complete set of simulation coordinates
    # and none of its rows should be identical to ri

    # It is assumed that positions are in units where box = 1

    nj, d = r.shape
    assert d==3, 'Dimension error for r in overlap_1'
    assert ri.size==3, 'Dimension error for ri in overlap_1'

    inv_box_sq = 1.0 / box ** 2

    for rj in r:
        rij = ri - rj            # Separation vector
        rij = rij - np.rint(rij) # Periodic boundary conditions in box=1 units
        rij_sq = np.sum(rij**2)  # Squared separation

        if rij_sq < inv_box_sq: # Check within cutoff
            return True # Immediate return on detection of overlap

    return False

def n_overlap ( box, r ):
    """Takes in box and coordinate array, and counts overlaps."""

    # This routine is used in the calculation of pressure
    # Actual calculation is performed by function n_overlap_1

    n, d = r.shape
    assert d==3, 'Dimension error for r in n_overlap'

    n_ovr = 0 # Initialize

    for i in range(n-1):
        n_ovr = n_ovr + n_overlap_1 ( r[i,:], box, r[i+1:,:] )

    return n_ovr

def n_overlap_1 ( ri, box, r ):
    """Takes in coordinates of an atom and counts overlaps.

    Values of box and partner coordinate array are supplied.
    """

    import numpy as np

    # In general, r will be a subset of the complete set of simulation coordinates
    # and none of its rows should be identical to ri

    # It is assumed that positions are in units where box = 1

    nj, d = r.shape
    assert d==3, 'Dimension error for r in overlap_1'
    assert ri.size==3, 'Dimension error for ri in overlap_1'

    inv_box_sq = 1.0 / box ** 2

    n_ovr = 0 # Initialize

    for rj in r:
        rij = ri - rj            # Separation vector
        rij = rij - np.rint(rij) # Periodic boundary conditions in box=1 units
        rij_sq = np.sum(rij**2)  # Squared separation

        if rij_sq < inv_box_sq: # Check within cutoff
            n_ovr = n_ovr + 1

    return n_ovr