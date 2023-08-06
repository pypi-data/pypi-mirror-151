"""
Copyright (C) University of Adelaide, Australia - All Rights Reserved
This source code is protected under proprietary reference only license.
Please refer to the accompanying LICENSE file for further information.

.. note:: This module is a collection of methods that I found sometimes useful, 
          and is always "experimental". As such most methods do not yet have proper
          docstring description.

"""

import sys
from numpy import *
import matplotlib.pyplot as plt
from scipy.interpolate import griddata

if "cv2" in sys.modules:
    import cv2


def setup_grid(limits, gspacing):
    """Set up square mesh grids for wavefront construction.

    :param limits: the minimum and maximum values of x and y coordinates
    :type limits: *dict*
    :param gspacing: the spacing between two neighboring points on the grid
    :type gspacing: positive *float*
    :Returns: *ndarrays* of x and y grids
    :rtype: *tuple*

    """

    x1, x2 = limits["x"]
    y1, y2 = limits["y"]

    xr = arange(x1, x2 + gspacing, gspacing)
    yr = arange(y1, y2 + gspacing, gspacing)

    if xr[-1] > x2:
        xr = xr[:-1]

    if yr[-1] > y2:
        yr = yr[:-1]

    return meshgrid(xr, yr)


def save_image_frame(name, iframe):
    cv2.imwrite(name, iframe)


def read_image_frame(name):
    im = cv2.imread(name, cv2.IMREAD_ANYDEPTH)
    return im.astype(int)


def find_indices_near(hsc, c_ind, radius=None):
    """Find the centroids near a centroid.

    The method finds all centroids contained in ``hsc``, an instance of
    :class:`HS_Centroids <HWS.HS_Centroids.HS_Centroids>``, that are within a
    distance from the centroid whose index is ``c_ind``.

    The distance is taken from ``radius``, and if it is not supplied, the
    method selects a value to be 1.25 times the smallest separation between
    the centroids labelled ``c_ind`` and its nearest centroid.

    Note that radius and the coordinates of the centroids in hsc must be in
    the same metric unit.

    The method returns the indices of the centroids thus found.

    """
    # Check if c_ind is valid relative to hsc
    noc = shape(hsc.centroids)[0]

    if c_ind not in arange(hsc.no_of_centroids):
        errstr = (
            "The centroid index c_ind is not consistent with "
            + "the number of centroids in hsc."
        )
        raise Exception(errstr)

    # Get the coordinates of the centre centroid.
    centre_c = hsc.centroids[c_ind]
    d = linalg.norm(hsc.centroids - centre_c, axis=1)

    # Determine the radius value to use if it is not supplied as an input.
    if radius is None:
        # Choose the second lowest value as the first lowest would be zero
        # (distance between the centre centroid and itself).
        radius = sort(d)[1] * 1.25
    elif radius < 0:
        raise Exception("radius must not be negative.")

    # Get the indices of the centroids that are within a radius from the
    # centre centroid.
    n_ind = where(d[:] < radius)

    return n_ind

    # Calculate distances between the centre centroid and the rest


def label_centroids_near_origin(hsc):
    anchors_index = argpartition(-hsc.slices_size, kth=2)[0:2]
    anchor_centroids = hsc.centroids[anchors_index]
    anchor_mean = anchor_centroids.mean(axis=0)
    origin_index = argmin(linalg.norm(hsc.centroids - anchor_mean, axis=1))
    origin_centroid = hsc.centroids[origin_index]
    nominal_sep = linalg.norm(anchor_centroids[0, :] - anchor_centroids[1, :]) / 2
    dist_fo = linalg.norm(hsc.centroids - origin_centroid, axis=1)
    cno_index = argpartition(dist_fo, kth=7)[0:7]
    cno_coord_fo = hsc.centroids[cno_index] - origin_centroid

    ri = {}
    ri["origin"] = origin_index
    anchor_from_origin = anchor_centroids - origin_centroid

    if abs(anchor_from_origin[0, 0]) > abs(anchor_from_origin[0, 1]):
        coord_to_label = 0
        anchor_types = ["left anchor", "right anchor"]
    else:
        coord_to_label = 1
        anchor_types = ["down anchor", "up anchor"]

    rc = hsc.centroids
    for ii in range(2):
        if anchor_from_origin[ii, coord_to_label] < 0:
            ri[anchor_types[0]] = anchors_index[ii]
        else:
            ri[anchor_types[1]] = anchors_index[ii]

    # Label the remaining 4 centroids near origin
    riv = ri.values()
    cc = 0
    for ii in cno_index:
        if ii not in riv:
            if cno_coord_fo[cc, 0] > 0:
                if cno_coord_fo[cc, 1] > 0:
                    ri["upper right"] = ii
                else:
                    ri["lower right"] = ii
            else:
                if cno_coord_fo[cc, 1] > 0:
                    ri["upper left"] = ii
                else:
                    ri["lower left"] = ii

        cc = cc + 1

    return ri


def interpolate_centroids_intensities(hsc):
    # WK: If the interpolated image look odd, it could be due to invalid
    # centroids that is more likely to occur if one lowers the otsu
    # threshold to get more centroids. It is recommended to check the
    # centroids and to filter centroids before using this method.

    x_max, x_min = (
        round((hsc.centroids[:, 0]).max()),
        round((hsc.centroids[:, 0]).min()),
    )

    y_max, y_min = (
        round((hsc.centroids[:, 1]).max()),
        round((hsc.centroids[:, 1]).min()),
    )

    limits = {}

    limits["x"] = array([x_min, x_max])
    limits["y"] = array((y_min, y_max))

    xg, yg = setup_grid(limits, 1)
    xc, yc = (xg[0, :], yg[:, 0])

    im_intp = griddata(hsc.centroids, hsc.intensities, (xg, yg), method="cubic")

    return im_intp


def read_and_average_image_frames(prefix, first=1, nof=1):
    pass


def generate_spot_pattern(
    centroids, size=(1024, 1024), pixel_size=12e-6, spot_radius=30e-6
):

    ss = spot_radius / pixel_size
    ssb = ss * 2
    image = zeros(size)

    for ctr in centroids:
        pos_is_valid = (
            ctr[0] > 0 + 20
            and ctr[0] < size[0] - 20
            and ctr[1] > 0 + 20
            and ctr[1] < size[1] - 20
        )

        if pos_is_valid:
            xmin = array([0, ctr[0] - ssb]).max().astype(int)
            xmax = array([size[0], ctr[0] + ssb + 1]).min().astype(int)
            xr = arange(xmin, xmax)

            ymin = array([0, ctr[1] - ssb]).max().astype(int)
            ymax = array([size[1], ctr[1] + ssb + 1]).min().astype(int)
            yr = arange(ymin, ymax)

            xg, yg = meshgrid(xr, yr)
            image[yg, xg] = exp(
                -(
                    (
                        ((xg - ctr[0]) / (2.0 * ss)) ** 2
                        + ((yg - ctr[1]) / (2.0 * ss)) ** 2
                    )
                    ** (10 / 2.0)
                )
            )

    return image


def generate_hex_grid_old():
    hole_spacing = 470e-6
    angle = 0
    n = 35
    (X, Y) = meshgrid(arange(n + 1), arange(n + 1))
    X = X * hole_spacing
    Y = Y * hole_spacing
    n = shape(X)[0]
    X = X * (3.0 ** 0.5 / 2)
    Y = Y + tile(array([0, 0.5 * hole_spacing]), [n, n / 2])
    X_s = (X / 12e-6) + 30
    Y_s = (Y / 12e-6) + 15
    X_r = zeros([n, n])
    Y_r = zeros([n, n])

    for ii in arange(n):
        for jj in arange(n):
            X_r[ii, jj] = cos(angle) * X_s[ii, jj] - sin(angle) * Y_s[ii, jj]
            Y_r[ii, jj] = sin(angle) * X_s[ii, jj] + cos(angle) * Y_s[ii, jj]

    pos = array([X_r.flatten(), Y_r.flatten()]).T
    ind = lexsort((pos[:, 1], pos[:, 0]))
    return pos[ind]


def generate_hex_grid(
    length=[1024, 1024], separation=37, orientation=0, padding=[30, 30]
):
    sp_s = separation
    sp_l = sqrt(3) * separation

    if orientation == 0:
        xspacing = sp_s
        yspacing = sp_l
    else:
        xspacing = sp_l
        yspacing = sp_s

    # outer x and y coordinates
    xr_o = arange(start=padding[0], stop=length[0] - padding[0], step=xspacing)
    yr_o = arange(start=padding[1], stop=length[1] - padding[1], step=yspacing)

    # inner x and y coordinates
    xr_i = arange(
        start=padding[0] + xspacing / 2.0,
        stop=length[0] - padding[0] - xspacing / 2.0,
        step=xspacing,
    )
    yr_i = arange(
        start=padding[1] + yspacing / 2.0,
        stop=length[1] - padding[1] - yspacing / 2.0,
        step=yspacing,
    )

    xg_o, yg_o = meshgrid(xr_o, yr_o)
    xg_i, yg_i = meshgrid(xr_i, yr_i)

    c_o = array(matrix([xg_o.ravel(), yg_o.ravel()]).T)
    c_i = array(matrix([xg_i.ravel(), yg_i.ravel()]).T)

    ctr = concatenate((c_o, c_i), axis=0)
    idx = lexsort((ctr[:, 1], ctr[:, 0]))
    return ctr[idx]


def generate_and_plot_centroids():
    ctr = generate_hex_grid()
    plt.scatter(ctr[:, 0], ctr[:, 1], marker="+")
    plt.gca().set_aspect("equal")
    plt.xlim(0, 1024)
    plt.ylim(0, 1024)

    for n in arange(shape(ctr)[0]):
        plt.text(ctr[n, 0] + 5, ctr[n, 1] + 5, str(n + 1), fontsize=8)

    plt.draw()

    return ctr
