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

    fname = 'summary.txt'
    df = pd.read_csv(fname)
    df['ratio'] = 100 * df.llcmiss / (df.loads + df.stores)

    plt.figure(0)
    p = plt.plot(df.npts,
                 df.llcmiss / df.llcmiss[0],
                 lw=2,
                 color=cmap[0],
                 marker=markertype[0],
                 mec=cmap[0],
                 mfc=cmap[0],
                 ms=10)

    plt.figure(1)
    p = plt.plot(df.npts,
                 df.ratio,
                 lw=2,
                 color=cmap[0],
                 marker=markertype[0],
                 mec=cmap[0],
                 mfc=cmap[0],
                 ms=10)

    plt.figure(0)
    ax = plt.gca()
    plt.xlabel(r"$n$", fontsize=22, fontweight='bold')
    plt.ylabel(
        r"LLC misses",
        fontsize=22,
        fontweight='bold')
    plt.setp(ax.get_xmajorticklabels(), fontsize=18, fontweight='bold')
    plt.setp(ax.get_ymajorticklabels(), fontsize=18, fontweight='bold')
    plt.tight_layout()
    plt.savefig('llcmiss.png', format='png')

    plt.figure(1)
    ax = plt.gca()
    plt.xlabel(r"$n$", fontsize=22, fontweight='bold')
    plt.ylabel(
        r"$~[\%]$",
        fontsize=22,
        fontweight='bold')
    plt.setp(ax.get_xmajorticklabels(), fontsize=18, fontweight='bold')
    plt.setp(ax.get_ymajorticklabels(), fontsize=18, fontweight='bold')
    plt.tight_layout()
    plt.savefig('misses_ratio.png', format='png')

    if args.show:
        plt.show()
