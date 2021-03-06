#!/usr/bin/env python
# -*- coding: utf-8 -*-


import time
import math
import argparse
import numpy as np
from scipy.linalg import svd
from shieh_utils import *


VERSION = 'v4.0.0'
USAGE = '''usage: %(prog)s [options] arg1 arg2'''


def get_args():
    """TODO: Docstring for get_args.
    :returns: TODO

    """
    parser = argparse.ArgumentParser(usage=USAGE)

    parser.add_argument('--version', action='version',
                        help='Version.', version=VERSION)
    parser.add_argument('-d', action='store', type=int, default=None,
                        help='Preserved Dimention.', dest='d')
    parser.add_argument('-v', action='store', type=float, default=None,
                        help='Preserved Variance.', dest='v')
    parser.add_argument('--fn', action='store',
                        help='The name of the file.', dest='fn')
    parser.add_argument('--movies', action='store',
                        help='The name of the movies file.', dest='moviesf')
    parser.add_argument('--rating', action='store',
                        help='The name of the rating file.', dest='ratingf')
    parser.add_argument('--users', action='store',
                        help='The name of the users file.', dest='usersf')
    parser.add_argument('--forhomework', action='store_true',
                        help='Homework model.', dest='forhomework')

    return parser.parse_args()


def dim_reduction_svd(X, d=None, v=None, combineit=True):
    """TODO: Docstring for dim_reduction_svd.
    :returns: TODO

    """
    U, Sigma, Vh = svd(X)

    sum_ = 0
    idx = Sigma.shape[0]
    summation = np.sum(Sigma ** 2)
    if v:
        for i in range(Sigma.shape[0]):
            sum_ += Sigma[i] ** 2
            if sum_/summation >= v:
                idx = i
                break
    elif d:
        for i in range(d):
            sum_ += Sigma[i] ** 2
        idx = d
    else:
        return X

    print 'retained dimension: %d' % (idx + 1)

    reduced = np.dot(U[:,:idx+1], np.diag(Sigma[:idx+1]))
    reconstructed = np.dot(reduced, Vh[:idx+1,:])
    ratio = sum_/summation

    if combineit:
        return reduced, reconstructed, ratio
    else:
        return U[:,:idx], np.diag(Sigma[:idx]), Vh[:idx,:], ratio


def main():
    """TODO: Docstring for main.
    :returns: TODO

    """
    args = get_args()
    if args.forhomework:
        X, _, _, _, _ = transform_data(args.moviesf, args.ratingf, args.usersf)
    else:
        X = load_data(args.fn, 'rating').values

    print X.shape

    start = time.time()
    X_transformed, retained_variance = dim_reduction_svd(X, args.d, args.v)
    print X_transformed.shape, retained_variance
    print 'kmeans time: %f' % (time.time() - start)


if __name__ == "__main__":
    main()
