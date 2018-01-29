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

    npts, nprocs = list(map(int, re.findall(r'\d+', fname)))
    runtime = 0
    filtertime = 0
    with open(fname, 'r') as f:
        for line in f:
            if 'Run time w/o init =' in line:
                runtime = float(line.split()[-1])
            elif 'Filter::apply_filter()' in line:
                if nprocs == 1:
                    filtertime = float(line.split()[2])
                else:
                    filtertime = float(line.split()[3])
            elif '[Level 0 step 1] Advanced' in line:
                ndofs = float(line.split()[5])

    return npts, nprocs, runtime, filtertime, ndofs


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
    df = pd.DataFrame(lst, columns=['npts',
                                    'nprocs',
                                    'runtime',
                                    'filtertime',
                                    'ndofs'])
    df['ratio'] = df['filtertime'] / df['runtime'] * 100
    df['runtime'] /= df['ndofs']
    df['filtertime'] /= df['ndofs']
    print(df)

    # ========================================================================
    # Plot
    with sns.axes_style("white"):

        p = sns.FacetGrid(hue='npts',
                          data=df)
        p = p.map(plt.scatter, 'nprocs', 'runtime')
        p = p.map(plt.plot, 'nprocs', 'runtime').add_legend()
        p.ax.set_xscale('log')
        p.ax.set_ylim([0, 1e-3])
        p.ax.set(xlabel=r'\# procs', ylabel=r'total $t$/dofs')

        p = sns.FacetGrid(hue='npts',
                          data=df)
        p = p.map(plt.scatter, 'nprocs', 'filtertime')
        p = p.map(plt.plot, 'nprocs', 'filtertime').add_legend()
        p.ax.set_xscale('log')
        p.ax.set_ylim([0, 1e-4])
        p.ax.set(xlabel=r'\# procs', ylabel=r'filter $t$/dofs')

        p = sns.FacetGrid(hue='nprocs',
                          data=df)
        p = p.map(plt.scatter, 'npts', 'ratio')
        p = p.map(plt.plot, 'npts', 'ratio').add_legend()
        p.ax.set(xlabel=r'\# pts', ylabel=r'filter $t$ / total $t$')

    plt.figure(1)
    plt.savefig('runtimes.png', format='png', dpi=300)
    plt.figure(2)
    plt.savefig('filtertimes.png', format='png', dpi=300)
    plt.figure(3)
    plt.savefig('ratios.png', format='png', dpi=300)

    if args.show:
        plt.show()
