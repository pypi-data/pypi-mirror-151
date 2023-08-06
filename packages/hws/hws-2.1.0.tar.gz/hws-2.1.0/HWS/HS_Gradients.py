"""
Copyright (C) University of Adelaide, Australia - All Rights Reserved
This source code is protected under proprietary reference only license.
Please refer to the accompanying LICENSE file for further information.
"""
from numpy import *
import scipy.ndimage
import matplotlib.pyplot as plt
from copy import deepcopy


class HS_Gradients:
    """A class to construct the gradients from the two sets of centroids.

    ``HS_Gradients`` is a class reponsible for construction and accees of the
    gradients. The gradient fields are constructed by calculating the displacements
    between two sets of centroids, and then scaling the result with the other
    parameters like ``pixel_size``, ``lever_arm`` and ``magnification``.

    **Instantiation**

    The class accepts three input parameters for the instantiation. ``hsc_i``, and
    ``hsc_f`` are initial (or reference) and final (or live) instances of
    :class:`HS_Centroids <HWS.HS_Centroids.HS_Centroids>`.

    ``lever_arm`` is the camera lever arm length, i.e., the distance between the
    CCD and the Hartmann plate in front of it.

    **Instance Variables**

    - ``pixel_size``: the width of a pixel (in meters), assuming each pixel is a square
      shape

      :Type: positive *float*
      :Required by: :func:`~HS_Gradients.construct_gradients`

    - ``lever_arm``: the distance (in meters) between the CCD and the Hartmann plate

      :Type: positive *float*
      :Required by: :func:`~HS_Gradients.construct_gradients`

    - ``magnification``: the magnification factor required to scale the gradients

      (may need more detailed description)

      :Type: *float*
      :Required by: :func:`~HS_Gradients.construct_gradients`

    - ``origin``: the origin of the coordinates used for the locations of the gradient
      vectors

      The choice of origin affects the wavefront construction, and is normally set at
      the centre of the image.

      :Type: *ndarray* of two elements
      :Required by: :func:`~HS_Gradients.construct_gradients`

    - ``initial_centroids``: an instance of :class:`HS_Centroids <HWS.HS_Centroids.HS_Centroids>` that contains the initial (or reference) centroids

      :Type: instance of :class:`HS_Centroids <HWS.HS_Centroids.HS_Centroids>`
      :Required by: :func:`~HS_Gradients.construct_gradients`

    - ``final_centroids``: an instance of :class:`HS_Centroids <HWS.HS_Centroids.HS_Centroids>` that contains the initial (or reference) centroids

      :Type: instance of :class:`HS_Centroids <HWS.HS_Centroids.HS_Centroids>`
      :Required by: :func:`~HS_Gradients.construct_gradients`

    - ``gradients``: An array of the gradients constructed from the initial and the
      final centroids

      Its shape is N by 4 (N = the number of centroids). The first two elements in
      each row are x and y values of the gradients (in radian, i.e., dimensionless
      units). The thrid and fourth elements are the coordinates of the corresponding
      reference centroid (meter units).

      :Type: *ndarray*
      :Required by: :func:`~HS_Gradients.calculate_rms`, :func:`~HS_Gradients.plot`
      :Updated by: :func:`~HS_Gradients.construct_gradients`

    - ``rms``: the root-mean-squqre values of the gradient magnitude values

      :Type: *ndarray* of N elements, where N is the number of centroids
      :Updated by: :func:`~HS_Gradients.calculate_rms`

    .. note:: The following two instance variables are not used but exist just
       to remind a user which units are used to express the centroids and gradients.

    - ``centroidUnits``
    - ``gradientUnits``

    """

    def __init__(self, hsc_i=None, hsc_f=None, lever_arm=0.01):
        self.pixel_size = 12e-6
        self.lever_arm = lever_arm
        self.magnification = 1.0
        self.origin = array([511.5, 511.5])
        self.initial_centroids = None
        self.final_centroids = None
        self.initial_centroids_input = hsc_i
        self.final_centroids_input = hsc_f
        self.gradients = None
        self.magnitudes = None
        self.rms = None
        self.centroidUnits = "( x [pixels], y [pixels] )"
        self.gradientUnits = "( dx/dL [rad], dy/dL [rad], x [meters], y [meters] )"

        if (hsc_i is not None) and (hsc_f is not None):
            self.remove_invalid_centroids()
        else:
            # just in case a user assigns one of the instances...
            self.initial_centroids = hsc_i
            self.final_centroids = hsc_f

    def construct_gradients(self):
        """Construct gradients from ``initial_centroids`` and ``final_centroids``.

        :Requires: ``pixel_size``, ``lever_arm``, ``magnification``, ``origin``,
                   ``initial_centroids``, ``final_centroids``
        :Updates: ``gradients``

        """
        self.lever_arm = float(self.lever_arm)
        self.magnigication = float(self.magnification)
        self.origin = self.origin.astype(float)

        x_i = self.initial_centroids.centroids[:, 0] - self.origin[0]
        y_i = self.initial_centroids.centroids[:, 1] - self.origin[1]

        x_i = x_i * (self.pixel_size * self.magnification)
        y_i = y_i * (self.pixel_size * self.magnification)

        displacements = (
            self.final_centroids.centroids - self.initial_centroids.centroids
        )

        mod_factor = self.pixel_size / (self.lever_arm * self.magnification)
        self.gradients = hstack((displacements * mod_factor, array([x_i, y_i]).T))
        # self.gradients = displacements
        self.magnitudes = sqrt(self.gradients[:, 0] ** 2 + self.gradients[:, 1] ** 2)

    def remove_invalid_centroids(self):
        """Removes the rows containing None from input centroids.

        (Experimental)
        """
        c_i = self.initial_centroids_input.centroids
        c_f = self.final_centroids_input.centroids
        indices_to_remove = unique(argwhere(equal(c_f, None))[:, 0])

        self.initial_centroids = deepcopy(self.initial_centroids_input)
        self.final_centroids = deepcopy(self.final_centroids_input)

        self.initial_centroids.hsimage = self.initial_centroids_input.hsimage
        self.final_centroids.hsimage = self.final_centroids_input.hsimage

        c_i_r = delete(c_i, indices_to_remove, axis=0)
        c_f_r = delete(c_f, indices_to_remove, axis=0)

        self.initial_centroids.centroids = c_i_r.astype(float)
        self.final_centroids.centroids = c_f_r.astype(float)

        self.initial_centroids.no_of_centroids = shape(
            self.initial_centroids.centroids
        )[0]

        self.final_centroids.no_of_centroids = shape(self.final_centroids.centroids)[0]

        if self.initial_centroids.intensities is not None:
            self.initial_centroids.intensities = delete(
                self.initial_centroids.intensities, indices_to_remove, axis=0
            )

        if self.final_centroids.intensities is not None:
            self.final_centroids.intensities = delete(
                self.final_centroids.intensities, indices_to_remove, axis=0
            )

    def calculate_rms(self):
        """Calculate root-mean-square of gradient magnitudes.

        :Requires: ``gradients``
        :Updates: ``rms``
        :Returns: the calcualted rms value
        :rtype: *float*

        """
        noc = float(shape(self.gradients)[0])
        self.rms = (((self.gradients[:, 0:2]) ** 2).sum() / noc) ** 0.5
        return self.rms

    def plot(self):
        """Plot the gradients using quiver plot method of matplotlib module

        :Requires: ``gradients``
        """
        plt.quiver(
            self.gradients[:, 2],
            self.gradients[:, 3],
            self.gradients[:, 0],
            self.gradients[:, 1],
        )
        plt.gca().set_aspect("equal", adjustable="box")
        plt.draw()
        # plt.show(block=False)
        plt.show()


# Won Kim 26/11/2018 3:19:31 PM
