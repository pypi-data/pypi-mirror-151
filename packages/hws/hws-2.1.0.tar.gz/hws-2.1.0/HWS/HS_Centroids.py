"""
Copyright (C) University of Adelaide, Australia - All Rights Reserved
This source code is protected under proprietary reference only license.
Please refer to the accompanying LICENSE file for further information.
"""

from numpy import *
import scipy.ndimage

try:
    from skimage.filter import threshold_otsu
except ImportError:
    from skimage.filters import threshold_otsu

from HWS.HS_Image import *


class HS_Centroids:
    """A class to handle centroiding an image.

    ``HS_Centroids`` is a class to generate and interact with centroids
    of Hartmann Sensor images.

    **Instance Variables**

    .. note:: Some variables are here as a result of the porting process
              (from Matlab to Python), and may be removed in a future
              revision.

    - ``centroids``: an N by 2 array of the spot positions where N is the
      number of centroids.

      :Type: *ndarray*
      :Required by: :func:`~HS_Centroids.average_centroids`
      :Updated by: :func:`~HS_Centroids.find_centroids`

    - ``average``: a 1 by 2 array of the average of all centroids.

      :Type: *ndarray*
      :Updated by: :func:`~HS_Centroids.average_centroids`

    - ``hsimage``: an instance of ``HS_Image``, which contains an image
      to be centroided.

      :Type: an instance of :class:`HS_Image <HWS.HS_Image>`
      :Required by: :func:`~HS_Centroids.find_centroids_from_image`,
                    :func:`~HS_Centroids.find_centroids_using_template`

    - ``threshold``: (optional) a value specifying the threshold of an image pixel
      values.

      If it is not *None*, each pixel value of
      ``hsimage.modified_image`` that are smaller than ``threshold`` is set to
      zero before centroiding.

      :Required by: (optional) :func:`~HS_Centroids.find_centroids_using_template`

    - ``no_of_centroids``: the total number of centroids in a image.

      :Type: *integer*
      :Updated by: :func:`~HS_Centroids.find_centroids_using_template`

    - ``rejected_centroids``: (optional) the centroids rejected by the method
      :func:`~HS_Centroids.find_centroids_from_image` with the input parameter
      ``to_remove_small_spots`` set to ``True``

      :Type: *ndarray*
      :Updated by: (optional) :func:`~HS_Centroids.find_centroids_from_image`

      (WK) The term "centroids" may not be accurate when we set the minimum
      acceptable slice to be greater than 1. May need to change the name
      later.

    - ``radius``: the half-width of a square area of the pixels from which the
      centroids are calculated (pixel units).

      :Type: positive *float*
      :Required by: :func:`~HS_Centroids.find_centroids_using_template`

    - ``weight_factor``: An exponent to be applied to the pixel values of an
      image to be centroided.

      :Type: positive *float*
      :Required by: :func:`~HS_Centroids.find_centroids_using_template`

    - ``resolution``: The resolution of an image to be centroided.

      :Type: *list* of two elements
      :Updated by: :func:`~HS_Centroids.determine_resolution`

    - ``intensities``: The sums of the pixel values of the centroids.

      :Type: *ndarray*
      :Updated by: :func:`~HS_Centroids.find_centroids_using_template`

    - ``moments``: a list of x, y, x2 and y2 moments.

      :Type: *dict*
      :Updated by: :func:`~HS_Centroids.compute_moments`

    .. note:: The variables below are currently not in use.

    - ``half_offset``
    - ``corner_centroids``
    - ``centroids_x``
    - ``centroids_y``
    - ``spot_spacing``
    - ``spacing_tolerance_factor``
    - ``dev_tolerance``
    - ``is_template``
    - ``spots_are_valid``
    - ``expected_no_centroids``

    """

    def __init__(self):
        self.centroids = None
        self.corner_centroids = None
        self.centroids_x = None
        self.centroids_y = None
        self.spot_spacing = None
        self.slices_size = None
        self.spacing_tolerance_factor = 0.1
        self.dev_tolerance = 2
        self.threshold = None
        self.ot_modifier = 1.0
        self.otsu_threshold = None
        self.hsimage = None
        self.is_template = None
        self.spots_are_valid = None
        self.no_of_centroids = None
        self.expected_no_centroids = None
        self.rejected_centroids = None
        self.radius = 10
        self.average = None
        self.half_offset = None
        self.weight_factor = 2
        self.intensities = None
        self.max_pvs = None
        self.resolution = None
        self.moments = {}
        self.moments["x"] = None
        self.moments["y"] = None
        self.moments["x2"] = None
        self.moments["y2"] = None

    def average_centroids(self):
        """Average the centroids.

        :Requires: ``centroids``
        :Updates: ``average``

        """
        self.average = array([self.centroids[:, 0].mean(), self.centroids[:, 1].mean()])

    def find_centroids(self, refcents=None):
        """Calculate the centroids using the reference as the reference.

        If an array of the centroids ``refcents`` is given as an input parameter,
        it is used as a set of initial coordinates to calculate the centroids.

        If no parameters are given, the method will attempt to detect the spots
        in an image, then calculate the centroids.

        :uses: :func:`~HS_Centroids.find_centroids_from_image`,
               :func:`~HS_Centroids.find_centroids_using_template`
        :param refcents: N by 2 ndarray of the reference centroids
        :type refcents: *ndarray* or *None*

        """
        if refcents is None:
            self.find_centroids_from_image()
        else:
            self.find_centroids_using_template(refcents)

    def determine_resolution(self):
        """Determine the resolution of an image to be centroided.

        First checks if the instance variable ``hsimage`` is an instance
        of :class:`HS_Image <HWS.HS_Image.HS_Image>`, then obtains the
        shape of the array ``hsimage.original_image``.

        :Requires: ``hsimage.original_image``
        :Updates: ``resolution``

        """
        if self.hsimage.__class__.__name__ == "HS_Image":
            self.resolution = zeros(2)
            res = shape(self.hsimage.original_image)
            self.resolution[0] = res[1]
            self.resolution[1] = res[0]
        else:
            raise Exception("hsimage is not an instance of HS_Image.")

    def find_centroids_from_image(self, to_filter_spots=False, size_threshold=1):
        """Find the centroids of an image.

        The method determines the image thresholding pixel value by calling
        ``skf.threshold_otsu`` method, uses that value to
        threshold the image, then detects the spots in the image using the
        ``scipy`` methods ``ndimage.label`` and ``ndimage.find_objetcts``.

        The method then calls the instance method
        :func:`~HS_Centroids.find_centroids_using_template` to compute the
        centroids.

        Optionally, if ``to_filter_spots`` is set ``True``, the
        method rejects any detected objects whose slice size is equal or
        lower than ``size_threshold``.

        :param to_filter_spots: (optional) if ``True``, spots of small size are not in                                                 cluded as centroids.
        :type to_filter_spots: *boolean*
        :param size_threshold: (optional) the maximum spot slice size to be rejected by
                                          filtering.
        :type size_threshold:
        :Requires: ``hsimage.modified_image``
        :uses: :func:`~HS_Centroids.determine_resolution`
               :func:`~HS_Centroids.find_centroids_using_template`
        :Updates: ``otsu_threshold``, ``centroids``

        """
        self.determine_resolution()
        otsu_threshold = threshold_otsu(self.hsimage.modified_image)

        bi = self.hsimage.modified_image > otsu_threshold * self.ot_modifier
        ilabel, noc = scipy.ndimage.label(bi)

        spot_slices = scipy.ndimage.find_objects(ilabel)
        rejected_centroids = None
        # print noc, shape(spot_slices)

        # for debugging
        # self.spot_slices = spot_slices
        if to_filter_spots is True:
            peaks, rejected_centroids = self.calculate_slice_centres_filtered(
                spot_slices, size_threshold
            )
        else:
            peaks = self.calculate_slice_centres(spot_slices)

        # print peaks
        self.find_centroids_using_template(peaks)
        self.otsu_threshold = otsu_threshold
        if rejected_centroids is not None:
            self.rejected_centroids = rejected_centroids

    def calculate_slice_centres_filtered(self, spot_slices, size_threshold):
        """Determine the centres of the objects detected from an image and filter
        out those that are too small.

        The method is called optionally by :func:`~HS_Centroids.find_centroids_from_image`.

        :param spot_slices: slice objects returned by SciPy method ``find_objects``
        :type spot_slices: *list* of *tuples*
        :param size_threshold: (optional) the maximum spot slice size to be rejected by filtering
        :type size_threshold: non-negative *integer*
        :returns: coordinates of the detected objects and rejected objects
        :rtype: *tuple* of *ndarrays*

        """
        # noc = shape(spot_slices)[0]
        # peaks = zeros((noc,2))

        # counter = 0
        peaks = None
        rejected_centroids = None
        slices_size = None

        for sr in spot_slices:
            ss = (sr[0].stop - sr[0].start) * (sr[1].stop - sr[1].start)
            x = round((sr[1].start + sr[1].stop - 1) / 2.0)
            y = round((sr[0].start + sr[0].stop - 1) / 2.0)
            if ss > size_threshold:
                if peaks is None:
                    peaks = array([x, y])
                    slices_size = array([ss])
                else:
                    peaks = vstack((peaks, array([x, y])))
                    slices_size = vstack((slices_size, array([ss])))
            else:
                if rejected_centroids is None:
                    rejected_centroids = array([x, y])
                else:
                    # print rejected_centroids
                    rejected_centroids = vstack((rejected_centroids, array([x, y])))

        self.slices_size = slices_size.ravel()

        return peaks, rejected_centroids

    def calculate_slice_centres(self, spot_slices):
        """Determine the centres of the objects detected from an image.

        :param spot_slices: slice objects returned by SciPy method ``find_objects``
        :type spot_slices: *list* of *tuples*
        :returns: coordinates of the detected objects and rejected objects
        :rtype: *tuple* of *ndarrays*

        """
        # noc = shape(spot_slices)[0]
        # peaks = zeros((noc,2))

        # counter = 0
        peaks = None
        slices_size = None

        for sr in spot_slices:
            ss = (sr[0].stop - sr[0].start) * (sr[1].stop - sr[1].start)
            x = round((sr[1].start + sr[1].stop - 1) / 2.0)
            y = round((sr[0].start + sr[0].stop - 1) / 2.0)
            if peaks is None:
                peaks = array([x, y])
                slices_size = array([ss])
            else:
                peaks = vstack((peaks, array([x, y])))
                slices_size = vstack((slices_size, array([ss])))

        self.slices_size = slices_size.ravel()

        return peaks

    def find_centroids_using_template_old(self, refcents):
        """Calculate the centroids of an image using an array of the
        centroids as starting positions.

        :param refcents: an N by 2 array of the reference centroids (N = the number of
                         centroids)
        :type refcents: ndarray
        :Requires: ``hsimage.modified_image``, ``weight_factor``, ``radius``
        :uses: :func:`~HS_Centroids.determine_resolution`,
               :func:`~HS_Centroids.determine_range`,
               :func:`~HS_Centroids.calculate_centroid`,
        :Updates: ``centroids``, ``intensities``, ``max_pvs``,
                  ``no_of_centroids``
        """
        self.determine_resolution()
        noc = shape(refcents)[0]
        peaks = rint(refcents).astype(int)
        # im = self.hsimage.modified_image.copy()
        im = self.hsimage.modified_image.astype(float)
        if self.threshold != None:
            im[im < self.threshold] = 0

        wim = im ** self.weight_factor

        self.centroids = []
        self.intensities = []
        self.max_pvs = []

        for p in peaks:
            xr, yr = self.determine_range(p, self.radius)
            xg, yg = meshgrid(xr, yr)
            xg = xg.astype(int)
            yg = yg.astype(int)

            twim = wim[yg, xg]
            tim = im[yg, xg]
            ctr = self.calculate_centroid(xg, yg, twim)

            # print(ctr)
            # print(any(ctr == None))
            if any(ctr) == None:
                # self.centroids.append(ctr)
                newp = ctr
            else:
                newp = rint(ctr).astype(int)

            if (newp[0] == p[0]) and (newp[1] == p[1]):
                self.centroids.append(ctr)
            elif (newp[0] != None) and (newp[1] != None):
                xr, yr = self.determine_range(newp, self.radius)
                xg, yg = meshgrid(xr, yr)
                xg = xg.astype(int)
                yg = yg.astype(int)
                try:
                    twim = wim[yg, xg]
                except IndexError:
                    print(newp, xr, yr)
                tim = im[yg, xg]
                self.centroids.append(self.calculate_centroid(xg, yg, twim))

            # print p
            self.intensities.append(tim.sum())
            self.max_pvs.append(tim.max())

        self.centroids = array(self.centroids)
        self.intensities = array(self.intensities)
        self.max_pvs = array(self.max_pvs)
        self.no_of_centroids = noc

    def find_centroids_using_template(self, refcents):
        """Calculate the centroids of an image using an array of the
        centroids as starting positions.

        :param refcents: an N by 2 array of the reference centroids (N = the number of
                         centroids)
        :type refcents: ndarray
        :Requires: ``hsimage.modified_image``, ``weight_factor``, ``radius``
        :uses: :func:`~HS_Centroids.determine_resolution`,
               :func:`~HS_Centroids.determine_range`,
               :func:`~HS_Centroids.calculate_centroid`,
        :Updates: ``centroids``, ``intensities``, ``max_pvs``,
                  ``no_of_centroids``
        """
        self.determine_resolution()
        noc = shape(refcents)[0]
        peaks = rint(refcents).astype(int)
        # im = self.hsimage.modified_image.copy()
        im = self.hsimage.modified_image.astype(float)
        if self.threshold != None:
            im[im < self.threshold] = 0

        wim = im ** self.weight_factor

        self.centroids = []
        self.intensities = []
        self.max_pvs = []

        for p in peaks:
            xr, yr = self.determine_range(p, self.radius)
            xg, yg = meshgrid(xr, yr)
            xg = xg.astype(int)
            yg = yg.astype(int)

            twim = wim[yg, xg]
            tim = im[yg, xg]
            ctr = self.calculate_centroid(xg, yg, twim)

            # print(ctr)
            # print(any(ctr == None))
            if (ctr[0] == None) or (ctr[1] == None):
                self.centroids.append(ctr)
                newp = ctr
            else:
                newp = rint(ctr).astype(int)

            if (newp[0] == p[0]) and (newp[1] == p[1]):
                self.centroids.append(ctr)
            elif (newp[0] != None) and (newp[1] != None):
                xr, yr = self.determine_range(newp, self.radius)
                xg, yg = meshgrid(xr, yr)
                xg = xg.astype(int)
                yg = yg.astype(int)
                try:
                    twim = wim[yg, xg]
                except IndexError:
                    print(newp, xr, yr)
                tim = im[yg, xg]
                self.centroids.append(self.calculate_centroid(xg, yg, twim))

            # print p
            self.intensities.append(tim.sum())
            self.max_pvs.append(tim.max())

        self.centroids = array(self.centroids)
        self.intensities = array(self.intensities)
        self.max_pvs = array(self.max_pvs)
        self.no_of_centroids = noc

    def determine_range(self, p, r, resolution=None):
        """Determine the x and y ranges centred at p with length ``r``.

        It ensures that the range does not go over the maximum and
        minimum possible coordinate values (in pixel units).

        :param p: the x and y coordinate of the centre of the range to
                  be found.
        :type p: *list* or *ndarray* of two elements
        :param r: the distance from ``p``
        :type p: positive *float*
        :returns: two *ndarrays* for the ranges in x and in y directions
        :rtype: *tuple*

        """
        if resolution is None:
            resolution = self.resolution

        xmax = resolution[0]
        ymax = resolution[1]
        xr = arange(max(0, p[0] - r), min(p[0] + r + 1, xmax))
        yr = arange(max(0, p[1] - r), min(p[1] + r + 1, ymax))

        return xr, yr

    def calculate_centroid(self, xc, yc, tim):
        """Calculate the centroid of a region of an image.

        The method simply calcualtes the centre of mass of an image (or
        a region thereof) ``tim``, treating its pixel values like
        masses.

        :param xc: a 2D array of x coordinates, as generated by the numpy
                   method ``meshgrid``
        :type xc: *ndarray*
        :param yc: a 2D array of y coordinates, as generated by the numpy
                   method ``meshgrid``
        :type yc: *ndarray*
        :param tim: a 2D array of pixel values, whose shape must be the same as
                   ``xc`` and ``yc``
        :type tim: *ndarray*
        :returns: the calculated centroid (x and y coordinates)
        :rtype: *ndarray*

        """

        total_intensity = float(tim.sum())
        xcf = xc.astype(float)
        ycf = yc.astype(float)

        if total_intensity == 0:
            xct = None
            yct = None
        else:
            xct = (tim * xcf).sum() / total_intensity
            yct = (tim * ycf).sum() / total_intensity

        return array([xct, yct])

    def compute_moments(self):
        """Calculate the moments x, y, x2 and y2.

        :Requires: ``centroids``, ``intensities``
        :Updates: ``moments``

        """
        if (self.centroids == None) or (self.intensities == None):
            raise Exception(
                "Instance variables centroids and intensities "
                + "must be present for the moments calculation."
            )
        totI = self.intensities.sum()
        avC = dot(self.centroids.T, self.intensities) / totI
        self.moments["x"] = avC[0]
        self.moments["y"] = avC[1]
        self.moments["x2"] = (
            (self.centroids[:, 0] - self.moments["x"]) ** 2 * self.intensities
        ).sum() / totI
        self.moments["y2"] = (
            (self.centroids[:, 1] - self.moments["y"]) ** 2 * self.intensities
        ).sum() / totI

    def estimate_beam_width(self):
        """Calculate the estimate of the beam widths in x and y
        directions from the moment x2 and y2.

        :returns: the beam widths in x and y directions
        :rtype: *tuple*
        """
        self.calculate_moments()
        width_x = 4 * (self.second_moments["x2"]) ** 0.5
        width_y = 4 * (self.second_moments["y2"]) ** 0.5

        return (width_x, width_y)
