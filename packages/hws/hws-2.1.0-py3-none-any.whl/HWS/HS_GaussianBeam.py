"""
Copyright (C) University of Adelaide, Australia - All Rights Reserved
This source code is protected under proprietary reference only license.
Please refer to the accompanying LICENSE file for further information.
"""

from numpy import *


class HS_GaussianBeam:
    def __init__(
        self,
        wavelength=None,
        distance_from_waist=None,
        waist_radius=None,
        max_amplitude=None,
        grid_size=None,
        grid_spacing=None,
    ):

        self.wavelength = wavelength
        self.distance_from_waist = distance_from_waist
        self.waist_radius = waist_radius
        self.max_amplitude = max_amplitude
        self.grid_size = grid_size
        self.grid_spacing = grid_spacing

        self.grid_x = None
        self.grid_y = None
        self.guoy_phase = 0
        self.curvature = None
        self.radius = None
        self.amplitude = None
        self.intensity = None
        self.rayleigh_range = None
        self.depth_of_focus = None

        # self.__dict__.update(parameters)
        self.derive_variables()

    def derive_variables(self):
        self.rayleigh_range = pi * self.waist_radius ** 2 / float(self.wavelength)
        self.depth_of_focus = 2.0 * self.rayleigh_range
        if self.distance_from_waist == 0:
            self.curvature = inf
        else:
            self.curvature = self.distance_from_waist * (
                1 + (self.rayleigh_range / float(self.distance_from_waist)) ** 2
            )
        self.radius = (
            self.waist_radius
            * (1 + (self.distance_from_waist / float(self.rayleigh_range)) ** 2) ** 0.5
        )
        self.setup_grid()
        self.construct_amplitude()

    def setup_grid(self):

        origin = self.grid_size / 2.0 - 0.5
        xr = (arange(0, self.grid_size) - origin) * self.grid_spacing
        yr = (arange(0, self.grid_size) - origin) * self.grid_spacing

        self.grid_x, self.grid_y = meshgrid(xr, yr)

    def construct_amplitude(self):
        i = 1j
        E_0 = float(self.max_amplitude)
        w_0 = float(self.waist_radius)
        w = float(self.radius)
        r = (self.grid_x ** 2 + self.grid_y ** 2) ** 0.5
        rc = float(self.curvature)
        gph = self.guoy_phase
        z = float(self.distance_from_waist)
        k = 2 * pi / self.wavelength
        self.amplitude = (
            E_0
            * (w_0 / w)
            * exp(-((r / w) ** 2) - i * k * z - i * k * (r ** 2 / (2 * rc)) + i * gph)
        )
        self.intensity = abs(self.amplitude) ** 2

    def construct_amplitude_at_waist(self):
        E_0 = float(self.max_amplitude)
        w = self.waist_radius
        r = (self.grid_x ** 2 + self.grid_y ** 2) ** 0.5
        self.amplitude = E_0 * exp(-((r / w) ** 2))
        self.intensity = abs(self.amplitude) ** 2

    def calculate_gradients(self, centroids):
        normal_v = self.calculate_normal_vectors(centroids)
        if self.distance_from_waist > 0:
            gradients = (normal_v - array([0, 0, 1]))[:, 0:2]
        else:
            gradients = (array([0, 0, 1]) - normal_v)[:, 0:2]
        return gradients

    def calculate_normal_vectors(self, centroids):
        sc = shape(centroids)[0]
        normal_vectors = zeros([sc, 3])
        centroids = centroids.astype(float)

        for k in arange(sc):
            nv = zeros(3)
            nv[0] = centroids[k, 0]
            nv[1] = centroids[k, 1]
            nv[2] = (
                self.curvature ** 2 - (centroids[k, 0] ** 2 + centroids[k, 1] ** 2)
            ) ** 0.5

            nv = nv / nv[2]
            normal_vectors[k, :] = nv

        return normal_vectors
