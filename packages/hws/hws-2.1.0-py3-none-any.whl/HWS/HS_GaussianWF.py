"""
Copyright (C) University of Adelaide, Australia - All Rights Reserved
This source code is protected under proprietary reference only license.
Please refer to the accompanying LICENSE file for further information.
"""

from numpy import *


class HS_GaussianWF:
    def __init__(self):
        amplitude = None
        width = None
        gradients = None
        wf = None
        wf_full = None
        centroids = None
        centre = array([511.5, 511.5]) * 12e-6

    def synthesize_gradients(self):
        ctr = zeros(shape(self.centroids))
        ctr[:, 0] = self.centroids[:, 0] - self.centre[0]
        ctr[:, 1] = self.centroids[:, 1] - self.centre[1]

        self.construct_wf()

        self.gradients = zeros(shape(ctr))
        self.gradients[:, 0] = self.wf * (2 / self.width ** 2) * ctr[:, 0]
        self.gradients[:, 1] = self.wf * (2 / self.width ** 2) * ctr[:, 1]

    def construct_wf(self):
        ctr = zeros(shape(self.centroids))
        ctr[:, 0] = self.centroids[:, 0] - self.centre[0]
        ctr[:, 1] = self.centroids[:, 1] - self.centre[1]

        self.wf = self.amplitude * exp(
            -(ctr[:, 0] ** 2 + ctr[:, 1] ** 2) / self.width ** 2
        )
