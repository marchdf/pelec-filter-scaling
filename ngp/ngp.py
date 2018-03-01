#!/usr/bin/env python3

# ========================================================================
#
# Imports
#
# ========================================================================
import sys
import os
import glob
import re
import argparse
import numpy as np
import pandas as pd
import matplotlib as mpl
# mpl.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns


# ========================================================================
#
# Some defaults variables
#
# ========================================================================
plt.rc('text', usetex=True)
plt.rc('font', family='serif', serif='Times')
cmap_med = ['#F15A60', '#7AC36A', '#5A9BD4', '#FAA75B',
            '#9E67AB', '#CE7058', '#D77FB4', '#737373']
cmap = ['#EE2E2F', '#008C48', '#185AA9', '#F47D23',
        '#662C91', '#A21D21', '#B43894', '#010202']
dashseq = [(None, None), [10, 5], [10, 4, 3, 4], [
    3, 3], [10, 4, 3, 4, 3, 4], [3, 3], [3, 3]]
markertype = ['s', 'd', 'o', 'p', 'h']


# ========================================================================
#
# Function definitions
#
# ========================================================================


# ========================================================================
#
# Main
#
# ========================================================================
if __name__ == '__main__':

    # ========================================================================
    # Parse arguments
    parser = argparse.ArgumentParser(
        description='A simple plot tool')
    parser.add_argument(
        '-s', '--show', help='Show the plots', action='store_true')
    args = parser.parse_args()

    # ======================================================================
    # Setup
    fname = 'data.csv'
    df = pd.read_csv(fname)

    # ======================================================================
    # Plot
    for i, ncell in enumerate(np.unique(df.ncells)):
        ndf = df[(df.ncells == ncell)].copy()

        plt.figure(0)
        p = plt.plot(ndf.stencil,
                     ndf.slowdown,
                     lw=2,
                     color=cmap[i],
                     marker=markertype[i],
                     mec=cmap[i],
                     mfc=cmap[i],
                     ms=10,
                     label=r'$cells={0:d}^3$'.format(ncell))

        plt.figure(0)
        ax = plt.gca()
        plt.xlabel(r"$n$", fontsize=22, fontweight='bold')
        plt.ylabel(r"slowdown", fontsize=22, fontweight='bold')
        plt.setp(ax.get_xmajorticklabels(), fontsize=18, fontweight='bold')
        plt.setp(ax.get_ymajorticklabels(), fontsize=18, fontweight='bold')
        legend = ax.legend(loc='best')
        # ax.set_ylim([0, 20])
        plt.tight_layout()
        plt.savefig('ngp.png', format='png')

    if args.show:
        plt.show()
