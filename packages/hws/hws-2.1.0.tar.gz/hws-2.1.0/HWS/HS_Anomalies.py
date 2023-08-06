"""
Copyright (C) University of Adelaide, Australia - All Rights Reserved
This source code is protected under proprietary reference only license.
Please refer to the accompanying LICENSE file for further information.
"""

from numpy import *
from HWS.HS_Centroids import *
from HWS.HS_Gradients import *
from HWS.HS_WFP import *


class HS_Anomalies:
    """A class to analyse the gradients for anomalies.

    (Experimental)

    This class can be used to detect the anomalous gradient vectors that
    may appear due to undesired and unexpected small size bumps (whose
    dimensions being comparable to the spot spacing) of high magnitude in a
    transverse wavefront aberration.

    The class is instantiated with an instance of
    :class:`HS_Gradients <HWS.HS_Gradients.HS_Gradients>`, and analyses
    the gradients by calculating the average of the radial components of the
    gradient vectors on nearest neighbor centroids for each centroid.

    The analysis is performed on "difference gradients", the gradients from
    reference and live centroids minus the gradients from LSQ polynomial
    calculation.

    If an averaged radial component on a centroid deviates from the overall
    average by a threshold factor times the standard deviation of all radial
    magnitudes, we assume that there is an anomalous aberration near that
    centroid.

    After identifying such "anomalous" centroids, the class analyses if such
    centroids are next to each other, and if so groups them. The number of
    groups obtained as such are the number of anomalies that may be present in
    the transverse aberration. The centroid with the highest radial magnitude in
    a group is considered to be the "centre" of that group.

    The class then estimates the position of each anomaly by performing a "centre
    of mass calculation" about the centre of each group, treating the averaged
    radial gradient magnitudes of neighbouring centroids like a mass. The
    estimate is by no means supposed to be quantitatively accurate but may still
    be useful analysing a large set of data for anomalies.

    """

    def __init__(self, hsg=None, std_threshold=5, separation=40):
        # separation is a nominal separation between neighboring spots in
        # an image (i.e., spot spacing). It is used to find the nearest
        # neighbor centroids and does not need to be too accurate.
        #
        # If the value is too small, one cannot find any neighboring
        # centroids. If too big, more centroids than just the nearest
        # neighbours will be included (which sometimes one may wish to do).
        self.separation = separation
        self.hsg = hsg
        self.gradients = None
        self.difference_gradients = None
        self.reference_centroids = None
        self.gradient_magnitudes = None
        self.wfp_whole = None
        self.wfp_diff = None
        self.wf_numerical_diff = None
        self.radial_magnitudes = None
        self.radial_ratios = None
        self.radial_mean = None
        self.radial_std = None
        self.std_threshold = std_threshold
        self.indices = None
        self.groups = {}
        self.centroids = None
        self.magnitudes = None
        self.ratios = None

        self.initialise_groups()

        if (self.hsg is not None) and self.hsg.__class__.__name__ == "HS_Gradients":
            self.reference_centroids = self.hsg.initial_centroids.centroids
            self.gradients = self.hsg.gradients[:, 0:2]
            self.gradient_magnitudes = self.hsg.magnitudes
            self.analyse_gradients()

    def initialise_groups(self):
        self.groups["indices"] = []
        self.groups["radial_magnitudes"] = []
        self.groups["max_indices"] = []

    def analyse_gradients(self):
        self.construct_difference_gradients()
        self.compute_radial_gradients()
        if size(self.indices) != 0:
            self.determine_anomalous_groups()

    def construct_difference_gradients(self):
        hsg = self.hsg

        self.wfp_whole = HS_WFP(hsg)
        self.wfp_whole.compute_poly_coeffs()
        gr_BTA = self.wfp_whole.calculate_gradients()

        self.difference_gradients = self.gradients - gr_BTA

        hsc_ref = self.hsg.initial_centroids
        mod_factor = hsg.pixel_size / (hsg.lever_arm * hsg.magnification)

        hsc_live = HS_Centroids()
        hsc_live.centroids = hsc_ref.centroids + self.difference_gradients / mod_factor
        hsc_live.no_of_centroids = hsc_ref.no_of_centroids
        hsc_live.average_centroids()

        hsg_diff = HS_Gradients(hsc_ref, hsc_live)
        hsg_diff.construct_gradients()

        self.wfp_diff = HS_WFP(hsg_diff)
        self.wfp_diff.compute_poly_coeffs()

    def compute_radial_gradients(self):
        refc = self.reference_centroids.copy()
        sep = self.separation
        gr_r = []
        noc = shape(refc)[0]
        # For each coord in pos_arr, find the reference centroids that are within a
        # radius given by separation.
        for cidx in range(noc):
            # Move the centroid sufficiently far away so that it is not
            # picked by where clause below (which then will pick only the
            # neighboring centroids but not the centroid itself.
            refc[cidx, :] = refc[cidx, :] + array([sep * 10, sep * 10])
            tc = self.reference_centroids[cidx, :]
            nn_ind = where(sqrt(((refc - tc) ** 2).sum(axis=1)) < sep)
            refc[cidx, :] = self.reference_centroids[cidx, :]
            v_dis = refc[nn_ind, :] - refc[cidx, :]
            v_mag = sqrt((v_dis ** 2).sum(axis=1))
            vn_dis = v_dis / v_mag

            gr = self.difference_gradients[nn_ind, 0:2]
            gr_r.append((vn_dis * gr).mean())

        gr_r = array(gr_r)
        self.radial_magnitudes = gr_r
        self.radial_mean = gr_r.mean()
        self.radial_std = gr_r.std()

        gr_r_c = self.radial_magnitudes - self.radial_mean
        gr_r_ratio = gr_r_c / self.radial_std

        self.ratios = gr_r_ratio
        self.indices = where(abs(gr_r_ratio) > self.std_threshold)[0]

    def determine_anomalous_groups(self):
        actr = self.reference_centroids[self.indices].copy()
        groups_list = None

        # group the centroid indices
        for aind in self.indices:
            tc = self.reference_centroids[aind]
            nn_aind = where(sqrt(((actr - tc) ** 2).sum(axis=1)) < self.separation)[0]
            nn_set = set(self.indices[nn_aind])

            if groups_list is None:
                groups_list = []
                groups_list.append(nn_set)
            else:
                updated = False
                ii = 0
                for grs in groups_list:
                    if len(grs.intersection(nn_set)) != 0:
                        groups_list[ii] = grs.union(nn_set)
                        updated = True
                        break

                    ii = ii + 1

                if updated == False:
                    groups_list.append(nn_set)

        self.initialise_groups()
        for grs in groups_list:
            grs = array(list(grs))
            maxind = grs[abs(self.radial_magnitudes[grs]).argmax()]
            self.groups["max_indices"].append(maxind)
            self.groups["indices"].append(grs)
            self.groups["radial_magnitudes"].append(self.radial_magnitudes[grs])

        self.estimate_positions()
        self.estimate_positions_alt()

    def estimate_positions(self):
        """Estimate the positions of the anomalies.

        The position of each anomaly is estimated by performing the
        weighted average of the centroids, using the averaged radial
        gradient magnitudes as weights, about the centroid with the highest
        radial gradient magnitude.

        """
        self.groups["positions"] = []

        refc = self.reference_centroids
        sep = self.separation
        rm = self.radial_magnitudes

        for cidx in self.groups["max_indices"]:
            tc = self.reference_centroids[cidx]
            nn_ind = where(sqrt(((refc - tc) ** 2).sum(axis=1)) < 1.5 * sep)[0]
            pos_x = (rm[nn_ind] * refc[nn_ind, 0]).sum() / rm[nn_ind].sum()
            pos_y = (rm[nn_ind] * refc[nn_ind, 1]).sum() / rm[nn_ind].sum()

            self.groups["positions"].append([pos_x, pos_y])

        self.groups["positions"] = array(self.groups["positions"])

    def estimate_positions_alt(self):
        """Estimate the positions of the anomalies using slightly different method.

        The method is similar to :func:`~HS_Anomalies.estimate_positions`
        except that the positions are estimated by performing two weighted
        averaging successively. The first averaging is over the radial
        gradient magnitudes over the centroids that form a cluster for each
        anomalies. The second averaging is then carried out about the
        position from the first averaging as the centre for the second averaging.

        """

        self.groups["positions_alt"] = []
        self.groups["positions_from_indices"] = []

        refc = self.reference_centroids
        sep = self.separation
        rm = self.radial_magnitudes

        for g in self.groups["indices"]:
            grm = self.radial_magnitudes[g]
            ipos_x = (grm * self.reference_centroids[g, 0]).sum() / grm.sum()
            ipos_y = (grm * self.reference_centroids[g, 1]).sum() / grm.sum()

            tc = array([ipos_x, ipos_y])
            nn_ind = where(sqrt(((refc - tc) ** 2).sum(axis=1)) < 2 * sep)[0]
            pos_x = (rm[nn_ind] * refc[nn_ind, 0]).sum() / rm[nn_ind].sum()
            pos_y = (rm[nn_ind] * refc[nn_ind, 1]).sum() / rm[nn_ind].sum()

            self.groups["positions_from_indices"].append(tc)
            self.groups["positions_alt"].append([pos_x, pos_y])

        self.groups["positions_alt"] = array(self.groups["positions_alt"])


# Won Kim 5/11/2018 3:37:03 PM
