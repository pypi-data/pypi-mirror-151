"""
Copyright (C) University of Adelaide, Australia - All Rights Reserved
This source code is protected under proprietary reference only license.
Please refer to the accompanying LICENSE file for further information.
"""

from numpy import *


class HS_BeamProfile:
    def __init__(self):

        self.hsgradients = None
        self.gradients = None
        self.centroids = None
        self.origin = (511.5, 511.5)
        self.intensities = None
        self.grid_spacing = 12e-6
        self.spot_spacing = None
        self.first_moments = {}
        self.second_moments = {}
        self.intensity_gradients = None
        self.P_matrix = None
        self.width_x = None
        self.width_y = None
        self.div_x = None
        self.div_y = None
        self.roc_x = None
        self.roc_y = None
        self.M2_x = None
        self.M2_y = None
        self.wavelength = None

    def convert_centroids(self):
        centroids = self.hsgradients.initial_centroids.centroids
        c_m = zeros(shape(centroids))
        c_m[:, 0] = centroids[:, 0] - self.origin[0]
        c_m[:, 1] = centroids[:, 1] - self.origin[1]
        self.centroids = c_m * self.grid_spacing

    def construct_beam_profile(self):
        # self.construct_intensity_gradients;
        self.construct_first_moments()
        self.construct_second_moments()
        # self.construct_P;
        self.width_x = 4 * sqrt(self.second_moments["x2"])
        self.width_y = 4 * sqrt(self.second_moments["y2"])
        # self.div_x = 4*sqrt(self.second_moments.u2);
        # self.div_y = 4*sqrt(self.second_moments.v2);
        self.roc_x = self.second_moments["x2"] / self.second_moments["xu"]
        self.roc_y = self.second_moments["y2"] / self.second_moments["yv"]
        # self.M2_x = (4*pi/self.wavelength)* ...
        #            sqrt(self.second_moments.x2 * ...
        #                 self.second_moments.u2 - ...
        #                 self.second_moments.xu^2);
        # self.M2_y = (4*pi/self.wavelength)* ...
        #            sqrt(self.second_moments.y2 * ...
        #                 self.second_moments.v2 - ...
        #                 self.second_moments.yv^2);

    def construct_first_moments(self):
        if (self.centroids is None) or (self.intensities is None):
            raise Exception(
                "Instance variables centroids and intensities "
                + "must be present for the moments calculation."
            )
        totI = self.intensities.sum()
        avC = dot(self.centroids.T, self.intensities) / totI
        self.first_moments["x"] = avC[0]
        self.first_moments["y"] = avC[1]

        gr = self.gradients[:, 0:2]
        avG = dot(gr.T, self.intensities) / totI
        self.first_moments["u"] = avG[0]
        self.first_moments["v"] = avG[1]

    def construct_second_moments(self):
        self.construct_x2()
        self.construct_xy()
        self.construct_xu()
        self.construct_xv()
        self.construct_y2()
        self.construct_yu()
        self.construct_yv()
        self.construct_uv()

    def construct_x2(self):
        self.second_moments["x2"] = (
            (self.centroids[:, 0] - self.first_moments["x"]) ** 2 * self.intensities
        ).sum() / self.intensities.sum()

    def construct_xy(self):
        self.second_moments["xy"] = (
            (self.centroids[:, 0] - self.first_moments["x"])
            * (self.centroids[:, 1] - self.first_moments["y"])
            * self.intensities
        ).sum() / self.intensities.sum()

    def construct_xu(self):
        self.second_moments["xu"] = (
            (self.centroids[:, 0] - self.first_moments["x"])
            * (self.gradients[:, 0] - self.first_moments["u"])
            * self.intensities
        ).sum() / self.intensities.sum()

    def construct_xv(self):
        self.second_moments["xv"] = (
            (self.centroids[:, 0] - self.first_moments["x"])
            * (self.gradients[:, 1] - self.first_moments["v"])
            * self.intensities
        ).sum() / self.intensities.sum()

    def construct_y2(self):
        self.second_moments["y2"] = (
            (self.centroids[:, 1] - self.first_moments["y"]) ** 2 * self.intensities
        ).sum() / self.intensities.sum()

    def construct_yu(self):
        self.second_moments["yu"] = (
            (self.centroids[:, 1] - self.first_moments["y"])
            * (self.gradients[:, 0] - self.first_moments["u"])
            * self.intensities
        ).sum() / self.intensities.sum()

    def construct_yv(self):
        self.second_moments["yv"] = (
            (self.centroids[:, 1] - self.first_moments["y"])
            * (self.gradients[:, 1] - self.first_moments["v"])
            * self.intensities
        ).sum() / self.intensities.sum()

    def construct_uv(self):
        self.second_moments["uv"] = (
            (self.gradients[:, 0] - self.first_moments["u"])
            * (self.gradients[:, 1] - self.first_moments["v"])
            * self.intensities
        ).sum() / self.intensities.sum()
