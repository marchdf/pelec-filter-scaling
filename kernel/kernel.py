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
def parse_profiler(fname):

    npts, ltype = list(map(int, re.findall(r'\d+', fname)))
    runtime = 0
    filtertime = 0
    with open(fname, 'r') as f:
        for line in f:
            if 'Run time w/o init =' in line:
                runtime = float(line.split()[-1])
            elif 'Filter::apply_filter()' in line:
                filtertime = float(line.split()[2])

    return npts, ltype, runtime, filtertime


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

    # ========================================================================
    # Setup
    sfx = '.out'
    fnames = sorted(glob.glob('*' + sfx))

    # ========================================================================
    # Parse profiling data
    lst = []
    for fname in fnames:
        lst.append(parse_profiler(fname))
    df = pd.DataFrame(lst, columns=['npts', 'ltype', 'runtime', 'filtertime'])
    df['ratio'] = df['filtertime'] / df['runtime'] * 100
    df['delta'] = df['npts'] - 1

    # ========================================================================
    # Plot
    names = [r'1: $n_c,k,j,i,n,m,l$',
             r'2: $n_c,n,k,m,j,l,i$',
             r'3: $n_c,k,n,j,m,i,l$',
             r'4: $n,m,l,n_c,k,j,i$',
             r'5: $n_c,n,m,l,k,j,i$']
    plt.figure(0)
    for k, ltype in enumerate(np.unique(df.ltype)):

        subdf = df[df.ltype == ltype]

        p = plt.plot(subdf.npts,
                     subdf.ratio,
                     lw=2,
                     color=cmap[k],
                     marker=markertype[k],
                     mec=cmap[k],
                     mfc=cmap[k],
                     ms=10,
                     label=names[k])

    plt.figure(0)
    ax = plt.gca()
    plt.xlabel(r"$n$", fontsize=22, fontweight='bold')
    plt.ylabel(r"time $~[\%]$", fontsize=22, fontweight='bold')
    plt.setp(ax.get_xmajorticklabels(), fontsize=18, fontweight='bold')
    plt.setp(ax.get_ymajorticklabels(), fontsize=18, fontweight='bold')
    legend = ax.legend(loc='best', prop={'size': 12})
    ax.set_ylim([0, 60])
    plt.tight_layout()
    plt.savefig('filtertimes.png', format='png', dpi=300)

    if args.show:
        plt.show()
