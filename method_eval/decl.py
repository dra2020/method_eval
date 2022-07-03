#!/usr/bin/env python3
#
# WARRINGTON'S FPTP DECLINATION
#

import numpy as np


def decl_degrees(vals):
    """
    Convert decl fractions to degrees.
    """

    return decl_fraction(vals) * 90.0


def decl_fraction(vals):
    """
    Compute the declination of an election.

    Warrington's FPTP implementation
    Return result expressed as a fraction of 90 degrees
    """

    Rwin = sorted(filter(lambda x: x <= 0.5, vals))
    Dwin = sorted(filter(lambda x: x > 0.5, vals))
    # Undefined if each party does not win at least one seat
    if len(Rwin) < 1 or len(Dwin) < 1:
        return False
    theta = np.arctan((1 - 2 * np.mean(Rwin)) * len(vals) / len(Rwin))
    gamma = np.arctan((2 * np.mean(Dwin) - 1) * len(vals) / len(Dwin))
    # Convert to range [-1,1]
    # A little extra precision just in case.
    return 2.0 * (gamma - theta) / 3.1415926535
