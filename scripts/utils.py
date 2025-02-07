"""The helper functions.
"""

import numpy as np
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import graphviz_layout
import matplotlib
import networkx as nx
import pandas as pd
import argparse
import logging
import os


class ArgumentParserWithDefaults(argparse.ArgumentParser):
    """The argument parser to support RawTextHelpFormatter and show default values.
    """

    def add_argument(self, *args, help=None, default=None, **kwargs):
        if help is not None:
            kwargs['help'] = help
        if default is not None and args[0] != '-h':
            kwargs['default'] = default
            if help is not None:
                kwargs['help'] += '\nDefault: {}'.format(default)
        super().add_argument(*args, **kwargs)


def move_results(src, dst):
    """Move the files from the source folder to the destination folder.

    Args:
        src: The source folder.
        dst: The destination folder.
    """

    if not os.path.isdir(dst):
        os.mkdir(dst)
    logging.info(f'Moving folder {src} to {dst}...')
    os.system(f'mv {src}/*.config {dst}')
    os.system(f'mv {src}/*.csv {dst}')


def get_row_col_counts(fc):
    """Return the row/columns counts of the figure.

    Args:
        fc: The figure count.

    Returns:
        rc: The row count.
        cc: The column count.
    """
    rc = int(np.sqrt(fc))
    while fc % rc != 0:
        rc -= 1
    cc = int(fc/rc)
    return (rc, cc)


def get_diameter(fn, ofn, plot=False, transparent=False):
    """Construct the network graph and return the diameter

    Args:
        fn: The nw- file path.
        ofn: The figure output path.
        plot: Plot the network or not.
        transparent: The generated figure is transparent or not.

    Returns:
        diameter: The network diameter.
    """

    # Init the matplotlib config
    font = {'family': 'Times New Roman',
            'weight': 'bold',
            'size': 14}
    matplotlib.rc('font', **font)

    data = pd.read_csv(fn)

    # Get the network information
    weighted_edges = [tuple(x)
                      for x in data[['Peer ID', 'Neighbor ID', 'Network Delay (ns)']].to_numpy()]
    weighted_edges_pruned = set()
    # Remove the repetitive edges
    for u, v, w in weighted_edges:
        u_v, w = sorted([u, v]), w
        weighted_edges_pruned.add((u_v[0], u_v[1], w))
    weighted_edges = list(weighted_edges_pruned)

    nodes = data.drop_duplicates('Peer ID')['Peer ID'].to_numpy()
    weights = data.drop_duplicates('Peer ID')['Weight'].to_numpy()

    # Construct the graph
    g = nx.Graph()
    g.add_weighted_edges_from(weighted_edges)

    diameter = nx.algorithms.distance_measures.diameter(g)
    if plot == False:
        return diameter

    lengths = {}
    for edge in weighted_edges:
        lengths[(edge[0], edge[1])] = dict(len=edge[2])

    pos = graphviz_layout(g, prog='neato')
    ec = nx.draw_networkx_edges(g, pos, alpha=0.2)
    nc = nx.draw_networkx_nodes(g, pos, nodelist=nodes, node_color=weights,
                                with_labels=False, node_size=10, cmap=plt.cm.jet)

    plt.colorbar(nc).ax.set_ylabel(
        'Weights', rotation=270, fontsize=14, labelpad=14)
    plt.axis('off')

    plt.title(f'{len(nodes)} Nodes, Diameter = {diameter}')
    plt.savefig(ofn, transparent=transparent)
    plt.close()
    return diameter
