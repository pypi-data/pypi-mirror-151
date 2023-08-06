"""
Copyright (C) University of Adelaide, Australia - All Rights Reserved
This source code is protected under proprietary reference only license.
Please refer to the accompanying LICENSE file for further information.
"""

from copy import deepcopy
from numpy import *
from numpy.linalg import norm
from scipy import arctan
from HWS.HS_Centroids import *
from HWS.HS_Gradients import *
from HWS.HS_WFP import *


class HS_OFF2ON:
    """A Class to determine the angle of the input beam and the tilt of the
    camera to transform off-axis gradients to on-axis gradients, and
    calculates on-axis wavefront aberration.

    **Instance Variables**

    - ``magnification``: the magnification factor of the beam received by
      the camera. The default value is 1.

    - ``unitization_length``: the unitization length that is to be used for
      all properties that are instances of HS_WFP class.
      :func:`~HS_OFF2ON.enable_unitization` method sets the
      unitization_length of all such properties.

    - ``hsc_cref_off``: an instance of
      :class:`HS_Centroids <HWS.HS_Centroids.HS_Centroids>` that holds the
      reference centroids obtained from a collimated (non-divergent) beam.

    - ``hsc_sref_off``: an instance of
      :class:`HS_Centroids <HWS.HS_Centroids.HS_Centroids>` that holds the
      centroids from the reflection off a cold spherical mirror.

    - ``hsc_live_off``: an instance of
      :class:`HS_Centroids <HWS.HS_Centroids.HS_Centroids>` that holds the
      centroids from the reflection off a heated spherical mirror.

    - ``hsg_sref_off``: an instance of
      :class:`HS_Gradients <HWS.HS_Gradients.HS_Gradients>` that holds the
      gradients between ``cref`` and ``sref`` centroids.

    - ``hsg_live_off``: an instance of
      :class:`HS_Gradients <HWS.HS_Gradients.HS_Gradients>` that holds the
      gradients between ``live`` and ``cref`` centroids.

    - ``hsg_live_sref_off``: an instance of
      :class:`HS_Gradients <HWS.HS_Gradients.HS_Gradients>` that holds the
      gradients between ``live`` and ``sref`` centroids.

    - ``incidence_angle``: the angle of incidence between the input and the
      reflected beam. When ``sref`` centroids are obtained from a cold
      spherical mirror, this value can be calculated using the method
      :func:`~HS_OFF2ON.calculate_incidence_angle`. This value must either
      be calculated from off-axis data or set by a user before calculating
      on-axis gradients.

    - ``tilt_angle``: the angle of camera tilt. When ``sref`` centroids are
      obtained from a cold spherical mirror, this value can be calculated
      using the method :func:`~HS_OFF2ON.calculate_incidence_angle`. This value
      must be either calculated from off-axis data or set by a user before
      calculating on-axis gradients.

    - ``normal_vectors_sref_off``: an array of vectors normal to the
      surface of the cold mirror (POV off-axis camera).

    - ``normal_vectors_sref_on``: an array of vectors normal to the
      surface of the cold mirror (POV on-axis).

    - ``normal_vectors_live_off``: an array of vectors normal to the
      surface of the hot mirror (POV off-axis camera).

    - ``normal_vectors_live_on``: an array of vectors normal to the
      surface of the hot mirror (POV on-axis).

    - ``hswfp_sref_off``: an instance of :class:`HS_WFP <HWS.HS_WFP.HS_WFP>`
      used to calculate the polynomial and Seidel coefficients from the off-axis
      gradients between ``sref`` and ``cref``.

    - ``hswfp_live_off``: an instance of :class:`HS_WFP <HWS.HS_WFP.HS_WFP>`
      used to calculate the polynomial and Seidel coefficients from the off-axis
      gradients between ``live`` and ``cref``.

    - ``hswfp_live_sref_off``: an instance of :class:`HS_WFP <HWS.HS_WFP.HS_WFP>`
      used to calculate the polynomial and Seidel coefficients from the off-axis
      gradients between ``live`` and ``sref``.

    - ``hswfp_sref_on``: an instance of :class:`HS_WFP <HWS.HS_WFP.HS_WFP>`
      used to calculate the polynomial and Seidel coefficients from the on-axis
      gradients between ``sref`` and ``cref``.

    - ``hswfp_live_on``: an instance of :class:`HS_WFP <HWS.HS_WFP.HS_WFP>`
      used to calculate the polynomial and Seidel coefficients from the on-axis
      gradients between ``live`` and ``cref``.

    - ``hswfP_live_sref_on``: an instance of :class:`HS_WFP <HWS.HS_WFP.HS_WFP>`
      used to calculate the polynomial and Seidel coefficients from the on-axis
      gradients between ``live`` and ``sref``.

    """

    def __init__(self, hsc_cref_off=None, hsc_sref_off=None, hsc_live_off=None):
        self.magnification = 1.0
        self.unitization_length = None
        self.incidence_angle = None
        self.tilt_angle = None
        self.hsc_cref_off = hsc_cref_off
        self.hsc_sref_off = hsc_sref_off
        self.hsc_live_off = hsc_live_off
        self.hsg_sref_off = None
        self.hsg_live_off = None
        self.hsg_live_sref_off = None
        self.hsc_cref_on = None
        self.hsc_sref_on = None
        self.hsc_live_on = None
        self.hswfp_sref_off = HS_WFP()
        self.hswfp_live_off = HS_WFP()
        self.hswfp_live_sref_off = HS_WFP()
        self.hswfp_sref_on = HS_WFP()
        self.hswfp_live_on = HS_WFP()
        self.hswfp_live_sref_on = HS_WFP()
        self.normal_vectors_sref_off = None
        self.normal_vectors_sref_on = None
        self.normal_vectors_live_off = None
        self.normal_vectors_live_on = None

    def enable_unitization(self):
        """Enable the option to unitize the length scales for the WF coefficient
        calculations.

        This method turns on the option to use unitization for all
        properties that are instances of :class:`HS_WFP <HWS.HS_WFP.HS_WFP>`,
        and sets their ``unitization_length`` instance variables.

        A user can control unitization of each instances separately as
        well. This method is just for convenience when a user wants to
        enable unitization with the same unitization length all at once.

        :Requires: ``unitization_length``
        :Updates: ``to_unitize`` and ``unitization_length`` of ``hswfp_sref_off``,
                  ``hswfp_live_off``, ``hswfp_live_sref_off``, ``hswfp_sref_on``,
                  ``hswfp_live_on``, and ``hswfp_sref_live_on``

        """
        self.hswfp_sref_off.to_unitize = True
        self.hswfp_live_off.to_unitize = True
        self.hswfp_live_sref_off.to_unitize = True
        self.hswfp_live_sref_on.to_unitize = True
        self.hswfp_sref_on.to_unitize = True
        self.hswfp_live_on.to_unitize = True

        self.hswfp_sref_off.unitization_length = self.unitization_length
        self.hswfp_live_off.unitization_length = self.unitization_length
        self.hswfp_live_sref_off.unitization_length = self.unitization_length
        self.hswfp_sref_on.unitization_length = self.unitization_length
        self.hswfp_live_on.unitization_length = self.unitization_length
        self.hswfp_live_sref_on.unitization_length = self.unitization_length

    def compute_off(self):
        """Compute off-axis gradients and the polynomial coefficients.

        :Uses: :func:`~HS_WFP.compute_sref_off`,
               :func:`~HS_WFP.compute_live_off`

        """
        self.compute_sref_off()
        self.compute_live_off()

    def compute_incidence_angle(self):
        """Compute the angle of incidence of the beam upon a spherical mirror.

        Uses the seidel coefficients obtained from ``sref`` data to compute
        the angle of incidence of the input rays as they hit the mirror. ``seidel_coeffs``
        of ``hswfp_sref_off`` must be present before calling this method.

        :Requires: ``seidel_coeffs`` of ``hswfp_sref_off``
        :Updates: ``incidence_angle``

        """
        S = self.hswfp_sref_off.seidel_coeffs["spherical_power"]
        if S > 0:
            C = self.hswfp_sref_off.seidel_coeffs["cylindrical_power"]
        else:
            hswfp_n = deepcopy(self.hswfp_sref_off)
            hswfp_n.gradients = -hswfp_n.gradients
            hswfp_n.compute_poly_coeffs()
            hswfp_n.compute_seidel_coeffs()
            S = hswfp_n.seidel_coeffs["spherical_power"]
            C = hswfp_n.seidel_coeffs["cylindrical_power"]

        self.incidence_angle = arctan(sqrt(C / abs(S)))

    def compute_incidence_angle_old(self):
        """Compute the angle of incidence of the beam upon a spherical mirror.

        Uses the seidel coefficients obtained from ``sref`` data to compute
        the angle of incidence of the input rays as they hit the mirror. ``seidel_coeffs``
        of ``hswfp_sref_off`` must be present before calling this method.

        :Requires: ``seidel_coeffs`` of ``hswfp_sref_off``
        :Updates: ``incidence_angle``

        """
        S = self.hswfp_sref_off.seidel_coeffs["spherical_power"]
        C = self.hswfp_sref_off.seidel_coeffs["cylindrical_power"]

        self.incidence_angle = arctan(sqrt(C / abs(S)))

    def compute_tilt_angle(self):
        """Compute the tilt angle of the Hartmann sensor.

        Uses the seidel coefficients obtained from ``sref`` data to compute
        the tilt angle of the Harmann sensor.

        :Requires: ``seidel_coeffs`` of ``hswfp_sref_off``
        :Updates: ``tilt_angle``

        """
        if self.hswfp_sref_off.seidel_coeffs["spherical_power"] > 0:
            phi = self.hswfp_sref_off.seidel_coeffs["phi"]
        else:
            hswfp_n = deepcopy(self.hswfp_sref_off)
            hswfp_n.gradients = -hswfp_n.gradients
            hswfp_n.compute_poly_coeffs()
            hswfp_n.compute_seidel_coeffs()
            phi = self.hswfp_sref_off.seidel_coeffs["phi"]

        if phi > 0:
            self.tilt_angle = pi / 2 - phi
        else:
            self.tilt_angle = -pi / 2 - phi

    def compute_on(self):
        """Compute the on-axis gradients and the wavefront coefficients.

        This is the wrapper method for the computation of the on-axis
        gradients and the wavefront coefficients.

        """
        self.compute_normal_vectors()
        self.compute_gradients_on()
        self.compute_centroids_on()
        self.compute_coeffs_on()

    def compute_normal_vectors(self):
        """Compute sref and live normal bectors."""
        self.compute_normal_vectors_sref()
        self.compute_normal_vectors_live()

    def compute_gradients_on(self):
        """Calculate on-axis gradients for all ``hswfp`` instance variables.

        :Uses: :func:`~HS_OFF2ON.compute_bradients_sref_on`,
               :func:`~HS_OFF2ON.compute_bradients_live_on`,
               :func:`~HS_OFF2ON.compute_bradients_live_sref_on`
        """
        self.compute_gradients_sref_on()
        self.compute_gradients_live_on()
        self.compute_gradients_live_sref_on()

    def compute_centroids_on(self):
        """Transforms off-axis centroids to on-axis centroids.

        :Requires: ``incidence_angle``, ``tilt_angle``, ``hsg_sref_off``,
                   ``hsg_live_off``
        :Updates: ``centroids`` of ``hsc_cref_on``, ``hswfp_live_sref_on``,
                  ``hswfp_live_sref_on``

        """
        self.hsc_cref_on = HS_Centroids()
        self.hsc_sref_on = HS_Centroids()
        self.hsc_live_on = HS_Centroids()
        origin = self.hsg_sref_off.origin
        lever_arm = self.hsg_sref_off.lever_arm
        pixel_size = self.hsg_sref_off.pixel_size
        ia = self.incidence_angle
        ta = self.tilt_angle
        rotmat_cam = matrix([[cos(ta), -sin(ta)], [sin(ta), cos(ta)]])

        # cref_on is constructed by transforming cref_off centroids
        cc = transpose(matrix(self.hsg_sref_off.gradients[:, [2, 3]]))
        cc = array(transpose(rotmat_cam * cc))
        cc[:, 0] = cc[:, 0] / cos(ia)

        # sc = self.hsg_sref_off.gradients[:,[0,1]] + self.hsg_sref_off.gradients[:,[2,3]]
        # sc = rotmat_cam*transpose(matrix(sc))
        # sc = array(transpose(rotmat_cam*sc))

        # lc = self.hsg_live_off.gradients[:,[0,1]] + self.hsg_live_off.gradients[:,[2,3]]
        # lc = rotmat_cam*transpose(matrix(lc))
        # lc = array(transpose(rotmat_cam*lc))

        # sref_on and live_on centroids are constructed from the on-axis gradients
        sc = self.hswfp_sref_on.gradients * lever_arm + cc
        lc = self.hswfp_live_on.gradients * lever_arm + cc

        self.hswfp_sref_on.centroids = cc
        self.hswfp_live_on.centroids = cc
        self.hswfp_live_sref_on.centroids = sc
        # self.hswfp_live_sref_on.centroids = self.hsc_sref_on.centroids

        self.hsc_cref_on.centroids = cc / pixel_size + origin
        self.hsc_sref_on.centroids = sc / pixel_size + origin
        self.hsc_live_on.centroids = lc / pixel_size + origin

    def compute_coeffs_on(self):
        """Compute the on-axis polynomial coefficients for all ``hswfp`` instance
        variables.

        :Requires: ``hswfp_sref_on``, ``hswfp_live_on``, ``hswfp_live_sref_on``

        """
        self.hswfp_sref_on.compute_poly_coeffs()
        self.hswfp_sref_on.compute_seidel_coeffs()

        self.hswfp_live_on.compute_poly_coeffs()
        self.hswfp_live_on.compute_seidel_coeffs()

        self.hswfp_live_sref_on.compute_poly_coeffs()
        self.hswfp_live_sref_on.compute_seidel_coeffs()

    def compute_sref_off(self):
        """Compute the off-axis gradients and the polynomial coefficients from
        ``sref`` data.

        This method calcualtes the gradients between the reference
        (``cref``) and off-axis ``sref`` centroids (the centroids that are
        supposed to be due to the rays refelcted by a cold spherical
        mirror), then calculates the corresponding polynomial coefficients.

        :Requires: ``hsc_cref_off``, ``hsc_sref_off``
        :Updates: ``hsg_sref_off``, ``hswfp_sref_off``

        """
        self.hsg_sref_off = HS_Gradients(self.hsc_cref_off, self.hsc_sref_off)

        self.hsg_sref_off.magnification = self.magnification

        self.hsg_sref_off.construct_gradients()

        self.hswfp_sref_off.centroids = self.hsg_sref_off.gradients[:, [2, 3]]
        self.hswfp_sref_off.gradients = self.hsg_sref_off.gradients[:, [0, 1]]

        self.hswfp_sref_off.compute_poly_coeffs()
        self.hswfp_sref_off.compute_seidel_coeffs()

    def compute_live_off(self):
        """Compute the off-axis gradients and the polynomial coefficients from
        ``live`` data.

        This method calcualtes the gradients between the reference
        (``cref``) and off-axis ``live`` centroids (the centroids that are
        supposed to be due to the rays refelcted by a thermally agitated
        spherical mirror), then calculates the corresponding polynomial
        coefficients.

        :Requires: ``hsc_cref_off``, ``hsc_live_off``
        :Updates: ``hsg_live_off``, ``hswfp_live_off``

        """
        self.hsg_live_off = HS_Gradients(self.hsc_cref_off, self.hsc_live_off)
        self.hsg_live_sref_off = HS_Gradients(self.hsc_sref_off, self.hsc_live_off)

        self.hsg_live_off.magnification = self.magnification
        self.hsg_live_sref_off.magnification = self.magnification

        self.hsg_live_off.construct_gradients()
        self.hsg_live_sref_off.construct_gradients()

        self.hswfp_live_off.centroids = self.hsg_live_off.gradients[:, [2, 3]]
        self.hswfp_live_off.gradients = self.hsg_live_off.gradients[:, [0, 1]]

        self.hswfp_live_sref_off.centroids = self.hsg_live_sref_off.gradients[:, [2, 3]]
        self.hswfp_live_sref_off.gradients = self.hsg_live_sref_off.gradients[:, [0, 1]]

        self.hswfp_live_off.compute_poly_coeffs()
        self.hswfp_live_off.compute_seidel_coeffs()

        self.hswfp_live_sref_off.compute_poly_coeffs()
        self.hswfp_live_sref_off.compute_seidel_coeffs()

    def compute_normal_vectors_sref(self):
        """Compute the vecotrs normal to the reflecting surface of a cold spherical mirror.

        This method computes the vectors normalised and perpendicular to the
        reflecting surface from the off-axis ``sref`` data, then transforms
        them to the on-axis normal vectors.

        :Requires: ``tilt_angle``, ``incidence_angle``, ``hswfp_sref_off``
        :Updates: ``normal_vectors_sref_off``, ``normal_vectors_sref_on``

        """
        ta = self.tilt_angle
        ia = self.incidence_angle
        centroids = self.hswfp_sref_off.centroids
        gradients = self.hswfp_sref_off.gradients
        noc = shape(centroids)[0]
        # Rotate the centroids and gradients to align camera y axis
        # to master y axis
        rotmat_cam = matrix([[cos(ta), -sin(ta)], [sin(ta), cos(ta)]])
        grads_r = transpose(rotmat_cam * transpose(matrix(gradients)))

        # Make vectors in the direction of input rays from POV of camera
        in_angle = -ia * 2
        rotmat_in = matrix(
            [
                [cos(in_angle), 0, sin(in_angle)],
                [0, 1, 0],
                [-sin(in_angle), 0, cos(in_angle)],
            ]
        )
        z_neg = matrix([[0], [0], [-1]])
        z_neg_rot = transpose(rotmat_in * z_neg)

        n_i_POVcam = kron(ones((noc, 1)), array(z_neg_rot))

        # Determine the vector normal to the reflecting surface
        r, c = shape(grads_r)
        n_l_unscaled = ones((r, c + 1))
        n_l_unscaled[:, :-1] = grads_r

        n_l_norm = norm(n_l_unscaled, axis=1)
        n_l_POVcam = n_l_unscaled / n_l_norm[:, None]

        n_s_unscaled = n_l_POVcam - n_i_POVcam
        n_s_norm = norm(n_s_unscaled, axis=1)
        n_s_POVcam = n_s_unscaled / n_s_norm[:, None]

        self.normal_vectors_sref_off = n_s_POVcam

        # self.compute_incidence_angle()
        # ia = self.incidence_angle
        self.normal_vectors_sref_on = zeros((noc, 3))
        rotmat_m = matrix([[cos(ia), 0, sin(ia)], [0, 1, 0,], [-sin(ia), 0, cos(ia)],])
        for k in range(noc):
            nv_k = matrix(n_s_POVcam[k, :])
            res_mat = transpose(rotmat_m * transpose(nv_k))
            self.normal_vectors_sref_on[k, :] = array(res_mat)[0, :]

    def compute_normal_vectors_live(self):
        """Compute the vecotrs normal to the reflecting surface of a thermally agitated
        spherical mirror.

        This method computes the vectors normalised and perpendicular to the
        reflecting surface from the off-axis ``live`` data,
        then transforms them to the on-axis normal vectors.

        :Requires: ``tilt_angle``, ``incidence_angle``, ``hswfp_live_off``
        :Updates: ``normal_vectors_live_off``, ``normal_vectors_live_on``
        """
        ta = self.tilt_angle
        ia = self.incidence_angle
        centroids = self.hswfp_live_off.centroids
        gradients = self.hswfp_live_off.gradients
        noc = shape(centroids)[0]
        # Rotate the centroids and gradients to align camera y axis
        # to master y axis
        rotmat_cam = matrix([[cos(ta), -sin(ta)], [sin(ta), cos(ta)]])
        grads_r = transpose(rotmat_cam * transpose(matrix(gradients)))
        cents_r = transpose(rotmat_cam * transpose(matrix(centroids)))
        # Make vectors in the direction of input rays from POV of camera
        in_angle = -ia * 2
        rotmat_in = matrix(
            [
                [cos(in_angle), 0, sin(in_angle)],
                [0, 1, 0],
                [-sin(in_angle), 0, cos(in_angle)],
            ]
        )
        z_neg = matrix([[0], [0], [-1]])
        z_neg_rot = transpose(rotmat_in * z_neg)
        n_i_POVcam = kron(ones((noc, 1)), z_neg_rot)

        # Determine the vector normal to the reflecting surface
        r, c = shape(grads_r)
        n_l_unscaled = ones((r, c + 1))
        n_l_unscaled[:, :-1] = grads_r

        n_l_norm = norm(n_l_unscaled, axis=1)
        n_l_POVcam = n_l_unscaled / n_l_norm[:, None]

        n_s_unscaled = n_l_POVcam - n_i_POVcam
        n_s_norm = norm(n_s_unscaled, axis=1)
        n_s_POVcam = n_s_unscaled / n_s_norm[:, None]

        self.normal_vectors_live_off = n_s_POVcam

        # self.compute_incidence_angle()
        # ia = self.incidence_angle
        self.normal_vectors_live_on = zeros((noc, 3))
        rotmat_m = matrix([[cos(ia), 0, sin(ia)], [0, 1, 0,], [-sin(ia), 0, cos(ia)],])
        for k in range(noc):
            nv_k = matrix(n_s_POVcam[k, :])
            res_mat = transpose(rotmat_m * transpose(nv_k))
            self.normal_vectors_live_on[k, :] = array(res_mat)[0, :]

    def compute_gradients_sref_on(self):
        """Compute the on-axis gradients due to the reflection from the cold
        spherical mirror.

        This method constructs the gradients one would obtain on-axis, from the array
        ``normal_vectors_sref_on``.

        :Requires: ``normal_vectors_sref_on``
        :Updates: ``hswfp_sref_on``

        """
        n_i = array([0, 0, -1])
        noc = shape(self.normal_vectors_sref_on)[0]
        n_l = zeros((noc, 3))
        n_s = self.normal_vectors_sref_on
        # reflect n_i w.r.t. n_s to get n_l
        for k in range(noc):
            n_l[k, :] = n_i - 2 * (sum(n_i * n_s[k, :])) * n_s[k, :]

        gr = zeros((noc, 2))
        gr[:, 0] = n_l[:, 0] / n_l[:, 2]
        gr[:, 1] = n_l[:, 1] / n_l[:, 2]

        self.hswfp_sref_on.gradients = gr

    def compute_gradients_live_on(self):
        """Compute the on-axis gradients due to the reflection from the thermally
        agitated spherical mirror.

        This method constructs the gradients one would obtain on-axis, from the array
        ``normal_vectors_live_on``.

        :Requires: ``normal_vectors_live_on``
        :Updates: ``hswfp_live_on``

        """
        n_i = array([0, 0, -1])
        noc = shape(self.normal_vectors_live_on)[0]
        n_l = zeros((noc, 3))
        n_s = self.normal_vectors_live_on
        # reflect n_i w.r.t. n_s to get n_l
        for k in range(noc):
            n_l[k, :] = n_i - 2 * (sum(n_i * n_s[k, :])) * n_s[k, :]

        gr = zeros((noc, 2))
        gr[:, 0] = n_l[:, 0] / n_l[:, 2]
        gr[:, 1] = n_l[:, 1] / n_l[:, 2]

        self.hswfp_live_on.gradients = gr

    def compute_gradients_live_sref_on(self):
        """Compute on-axis gradients between live and sref.

        :Requires: ``gradients`` of ``hswfp_live_sref_on``, ``hswfp_live_on``, and
                   ``hswfp_sref_on``
        :Updates: ``hswfp_live_sref_on``

        """
        self.hswfp_live_sref_on.gradients = (
            self.hswfp_live_on.gradients - self.hswfp_sref_on.gradients
        )


# Won Kim 7/11/2018 3:49:06 PM
