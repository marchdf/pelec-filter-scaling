#!/usr/bin/env python3
#
# This file creates a grids file with the same number of cells per
# level. These grids are nested and centered in the middle of the
# domain.
#

# ========================================================================
#
# Imports
#
# ========================================================================
import numpy as np


# ========================================================================
#
# Main
#
# ========================================================================
if __name__ == '__main__':

    # ========================================================================
    # Setup

    # n^3 = number of cells on each level
    n = 512  # 1 level
    # n = 448  # 2 level
    # n = 416  # 3 level and max_grid_size = 32

    # number of levels beyond the base level
    nlvls = 1

    # max grid size on each level
    max_grid_size = 64

    # Grid refinement ratio
    ratio = 2

    # output file name
    oname = 'grids_file_{0:d}_{1:d}'.format(n, nlvls)

    # ========================================================================
    # Write output file
    with open(oname, 'w') as of:
        of.write(str(nlvls) + '\n')

        for k, nlvls in enumerate(range(nlvls)):
            resolution = n * ratio**k
            center = int(resolution / 2)
            extent = int(resolution / (ratio**(k + 2)))
            xs = np.arange(center - extent,
                           center + extent,
                           int(max_grid_size / ratio))
            xe = xs + int(max_grid_size / 2) - 1

            XS = np.meshgrid(xs, xs, xs)
            XE = np.meshgrid(xe, xe, xe)

            of.write('{0:d}\n'.format(len(XS[0].flatten())))

            for xs, ys, zs, xe, ye, ze in zip(XS[0].flatten(),
                                              XS[1].flatten(),
                                              XS[2].flatten(),
                                              XE[0].flatten(),
                                              XE[1].flatten(),
                                              XE[2].flatten()):
                of.write("(({0:d},{1:d},{2:d})({3:d},{4:d},{5:d}))\n".format(
                    xs, ys, zs, xe, ye, ze))

        # need a blank line at the end of the grids file
        of.write('\n')
