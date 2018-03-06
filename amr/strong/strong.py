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

    npts, nlvls, nprocs = list(map(int, re.findall(r'\d+', fname)))
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

    return npts, nlvls, nprocs, runtime, filtertime


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
                                    'nlvls',
                                    'nprocs',
                                    'runtime',
                                    'filtertime'])
    df['ratio'] = df['filtertime'] / df['runtime'] * 100
    df['delta'] = df['npts'] - 1
    df['theory'] = df['nprocs']**(-1.0)

    min_procs = df.nprocs.min()

    # ========================================================================
    # Plot
    for nlvls in np.unique(df.nlvls):
        plt.close('all')
        ndf = df[(df.nlvls == nlvls)].copy()
        total_basetimes = ndf.groupby('npts')['runtime'].first()
        filter_basetimes = ndf.groupby('npts')['filtertime'].first()
        for k, npts in enumerate(np.unique(ndf.npts)):
            subdf = ndf[(ndf.npts == npts)].copy()
            subdf['total_speedup'] = total_basetimes.iloc[k] / subdf['runtime']
            subdf['filter_speedup'] = filter_basetimes.iloc[k] / \
                subdf['filtertime']

            plt.figure(0)
            p = plt.semilogx(subdf.nprocs,
                             subdf.ratio,
                             lw=2,
                             color=cmap[k],
                             marker=markertype[k],
                             mec=cmap[k],
                             mfc=cmap[k],
                             ms=10,
                             label=r'$n={0:d}$'.format(npts))

            plt.figure(1)
            p = plt.plot(subdf.nprocs,
                         subdf.total_speedup,
                         lw=2,
                         color=cmap[k],
                         marker=markertype[k],
                         mec=cmap[k],
                         mfc=cmap[k],
                         ms=10,
                         label=r'$n={0:d}$'.format(npts))

            if npts != 0:
                plt.figure(2)
                p = plt.plot(subdf.nprocs,
                             subdf.filter_speedup,
                             lw=2,
                             color=cmap[k],
                             marker=markertype[k],
                             mec=cmap[k],
                             mfc=cmap[k],
                             ms=10,
                             label=r'$n={0:d}$'.format(npts))

        plt.figure(1)
        p = plt.plot(subdf.nprocs,
                     subdf.nprocs / min_procs,
                     lw=2,
                     color=cmap[-1],
                     label="perfect scaling")

        plt.figure(2)
        p = plt.plot(subdf.nprocs,
                     subdf.nprocs / min_procs,
                     lw=2,
                     color=cmap[-1],
                     label="perfect scaling")

        plt.figure(0)
        ax = plt.gca()
        plt.xlabel(r"\# procs", fontsize=22, fontweight='bold')
        plt.ylabel(r"time $~[\%]$", fontsize=22, fontweight='bold')
        plt.setp(ax.get_xmajorticklabels(), fontsize=18, fontweight='bold')
        plt.setp(ax.get_ymajorticklabels(), fontsize=18, fontweight='bold')
        legend = ax.legend(loc='best', prop={'size': 12})
        # ax.set_ylim([0, 20])
        plt.tight_layout()
        plt.savefig('ratios_{0:d}.png'.format(nlvls),
                    format='png',
                    dpi=300)

        plt.figure(1)
        ax = plt.gca()
        plt.xlabel(r"cores", fontsize=22, fontweight='bold')
        plt.ylabel(r"speedup", fontsize=22, fontweight='bold')
        plt.setp(ax.get_xmajorticklabels(), fontsize=18, fontweight='bold')
        plt.setp(ax.get_ymajorticklabels(), fontsize=18, fontweight='bold')
        legend = ax.legend(loc='best', prop={'size': 12})
        # ax.set_ylim([0, 20])
        plt.tight_layout()
        plt.savefig('total_speedup_{0:d}.png'.format(nlvls),
                    format='png',
                    dpi=300)

        plt.figure(2)
        ax = plt.gca()
        plt.xlabel(r"cores", fontsize=22, fontweight='bold')
        plt.ylabel(r"speedup", fontsize=22, fontweight='bold')
        plt.setp(ax.get_xmajorticklabels(), fontsize=18, fontweight='bold')
        plt.setp(ax.get_ymajorticklabels(), fontsize=18, fontweight='bold')
        legend = ax.legend(loc='best', prop={'size': 12})
        # ax.set_ylim([0, 20])
        plt.tight_layout()
        plt.savefig('filter_speedup_{0:d}.png'.format(nlvls),
                    format='png',
                    dpi=300)

    if args.show:
        plt.show()
