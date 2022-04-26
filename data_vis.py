# data_vis.py
from argparse import ArgumentError
import sys
import umap
import plotly
import numpy as np
import pandas as pd
from sklearn.manifold import TSNE
from matplotlib import pyplot as plt
from sklearn.decomposition import PCA


def UMAP_vis():


    return


def tSNE_vis():


    return


def PCA_vis():
    # cumulative and individual variances from principle components
    # project to 2d anyway with 2 principle components


    return

def main(key):

    if key == "umap":
        UMAP_vis()

    elif key == "tsne":
        tSNE_vis()

    elif key == "pca":
        PCA_vis()

    else: 
        raise ArgumentError("Incorrect function specification.")

    return


if __name__ == "__main__":

    if len(sys.argv) == 1:
        pass

    elif len(sys.argv) == 2:
        main(sys.argv[-1])

    else:
        raise ArgumentError("Incorrect command line arguments")

    