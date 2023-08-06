"""
Copyright (C) University of Adelaide, Australia - All Rights Reserved
This source code is protected under proprietary reference only license.
Please refer to the accompanying LICENSE file for further information.
"""

from numpy import *
from HWS.HS_Gradients import *
from scipy import linalg


class HS_WFP:
    """A class used to fit a sum of two-dimensional polynomials to the gradients to
    characterise the transverse wavefront abberation.

    The class performs a least squares fit of the gradients to a sum of the polynomials
    (the instance variables ``X_bases`` and ``Y_bases``)
    and calculates the polynomial coeefficients. Once the coefficients are obtained, a
    user can also construct the corresponding transverse wavefron aberration map using
    the coefficients and the functions in ``poly_bases``.

    The polynomial coefficients can also be used to (in a limited sense) calculate
    the Zernike (up to the second order) and aome Seidel coefficients.

    **Instantiation**

    Upon instantiation, the class will build the basis functions (or bases) and
    determine how many basis functions are required for the operation.

    Two parameters a user can choose are ``hsgr`` and ``order``, ``hsgr`` is an instance
    of :class:`HS_Gradients <HWS.HS_Gradients.HS_Gradients>` and ``order`` is
    an integer from 1 to 6.

    ``order`` specifies the maximum power of polynomials that the class will use to
    characterise the wavefront. The class allows the maximum order of 6, which is
    the default value of ``order``.

    :func:`~HS_WFP.determine_no_of_bases` which is run during instantiation, sets
    ``no_of_bases`` to a value consistent with ``order``.

    Two variables ``gradients`` and ``centroids`` are generated from ``hsgradients``
    if it is set as an instance of :class:`HS_Gradients <HWS.HS_Gradients.HS_Gradients>`
    by using the input parameter ``hsg``.

    A user should note that the centroids (i.e., the 3rd and the 4th columns of the
    ``gradients`` instance variable of ``hsgradients``) should be in metre units about
    a suitably chosen origin (normally the centre of an image), which should automatically
    the case when the gradients are constructed using
    :func:`HS_Gradients.construct_gradients() <HWS.HS_Gradients.HS_Gradients.construct_gradients>` as normal.

    **Basis Functions**

    There are three sets of basis functions in this class:

    - polynomial basis functions (``poly_all_bases``) are the polynomial basis functions
      that can be used in the polynomial wavefront reconstruction using the method
      :func:`~HS_WFP.calculate_wf`. These functions are NOT used in least squares fitting.

    - X basis functions (``X_all_bases``) are the partial x derivatives of the polynomial
      basis functions, and are used to fit the x components of the gradients.

    - Y basis functions (``Y_all_bases``) are the partial y derivatives of the polynomial
      basis functions, and are used to fit the y components of the gradients.

    **Instance Variables**

    - ``unitization_length``: the length factor used to scale the coordinates of the
      centroids

      The variable is relevant only when ``to_unitize`` is ``True``.

      :Type: positive *float*
      :Required by: :func:`~HS_WFP.build_XY`, :func:`~HS_WFP.deunitize`

    - ``to_unitize``: a *boolean* to indicate whether the centroids should be scaled or not

      If ``True``, the lengths in centroids and basis fucntions will be scaled by
      ``unitization_length``.

      :Type: *boolean*
      :Requried by: :func:`~HS_WFP.build_XY`, :func:`~HS_WFP.compute_poly_coeffs`,
                    :func:`~HS_WFP.compute_poly_coeffs_weighted`,
                    :func:`~HS_WFP.calculate_gradients`,

    - ``order``: the maximum power of the polynomials to be used in the least squares fit of
      the gradients

      The default value is 6, which is also the maximum value that is currently available.

      :Type: *integer* (from 1 to 6)
      :Required by: :func:`~HS_WFP.determine_no_of_bases`

    - ``no_of_bases``: the number of polynomial basis functions to be used in the least
      squares fit

      A valid value of this variable must be one of those in the class variable
      ``no_of_bases_array``, depending on ``order``. For example if ``order`` is
      3, the valid ``no_of_bases`` is 9.

      With 6 being the default value of ``order``, the valid ``no_of_bases`` is 27.

      :Type: *integer* (from the class variable ``no_of_bases_array``)
      :Required by: :func:`~HS_WFP.compute_poly_coeffs`,
                    :func:`~HS_WFP.compute_poly_coeffs_weighted`,
                    :func:`~HS_WFP.deunitize`,
                    :func:`~HS_WFP.build_bases`
      :Updated by: :func:`~HS_WFP.determine_no_of_bases`

    - ``hsgradients``: an instance of :class:`HS_Gradients <HWS.HS_Gradients.HS_Gradients>`

      During instantiation, it is split into ``gradients`` and ``centroids`` which are
      subsequently used by other methods in the class.

      :Type: an instance of :class:`HS_Gradients <HWS.HS_Gradients.HS_Gradients>`

    - ``centroids``: the centroids to be used in the least squares fit

      During instantiation, the third and fourth columns of ``hsgradients.gradients`` are
      assigned to this variable.

      :Type: *ndarray*
      :Required by: :func:`~HS_WFP.build_XY`,
                    :func:`~HS_WFP.build_XY_nu`,
                    :func:`~HS_WFP.compute_poly_coeffs_weighted`

    - ``gradients``: the gradients to be used in the least squares fit

      During instantiation, the first and second columns of ``hsgradients.gradients`` are
      assigned to this variable.

      :Type: *ndarray*
      :Required by: :func:`~HS_WFP.compute_poly_coeffs`,
                    :func:`~HS_WFP.compute_poly_coeffs_weighted`,
                    :func:`~HS_WFP.compute_SSR`

    - ``poly_all_bases_names``: the names of all polynomial basis functions that can be
      used in the polynomial wavefront reconstruction

      This variable contains all of the polynomial basis function names that can be used
      in the least squares fitting of the gradients.

      The naming format is xmyn where m, n are positive integers: for eample `x2y3` refers
      to a function (x^2)*(y^3).

      :Type: *list* of *strings*
      :Required by: :func:`~HS_WFP.build_bases`
      :Updated by: :func:`~HS_WFP.build_all_bases`

    - ``poly_bases_names``: the names of the polynomial basis functions used in the
      polynomial wavefront reconstruction

      This variable is derived from ``poly_all_bases_names`` by taking a number of elements
      (set by ``no_of_bases``) starting from the first in ``poly_all_bases_names``.

      :Type: *list* of *strings*
      :Required by: :func:`~HS_WFP.compute_poly_coeffs`,
                    :func:`~HS_WFP.compute_poly_coeffs_weighted`
      :Updated by: :func:`~HS_WFP.build_bases`

    - ``poly_all_bases``: all polynomial basis functions that can be used in the polynomial
      wavefront reconstruction

      :Type: *list*
      :Required by: :func:`~HS_WFP.calcualte_wf`
      :Updated by: :func:`~HS_WFP.build_all_bases`

    - ``poly_coeffs``: a *dict* of the coefficients of the polynomial basis functions
      calculated from the least squares fit

      :Type: *dict*
      :Required by: :func:`~HS_WFP.calcualte_wf`
      :Updated by: :func:`~HS_WFP.compute_poly_coeffs`,
                   :func:`~HS_WFP.compute_poly_coeffs_weighted`

    - ``poly_coeffs_array``: an *ndarray* of the coefficients of the polynomial bases
      functions calculated from the least square fit

      This is an *ndarray* version of ``poly_coeffs``, a convenience

      :Type: *ndarray*
      :Required by: :func:`~HS_WFP.calculate_gradients`,
                    :func:`~HS_WFP.calculate_wf`,
                    (optional) :func:`~HS_WFP.compute_seidel_coeffs`,
                    (optional) :func:`~HS_WFP.compute_zernike_coeffs`
      :Updated by: :func:`~HS_WFP.compute_poly_coeffs`,
                   :func:`~HS_WFP.compute_poly_coeffs_weighted`

    - ``poly_coeffs_u``: a *dict* of the coefficients of the unitized polynomial basis
      functions calculated from the least squares fit

      This variable is used only when ``to_unitize`` is ``True``.

      :Type: *dict*
      :Updated by: :func:`~HS_WFP.compute_poly_coeffs`,
                   :func:`~HS_WFP.compute_poly_coeffs_weighted`

    - ``poly_coeffs_array_u``: an *ndarray* of the coefficients of the unitized
      polynomial basis functions calculated from the least squares fit

      This variable is used only when ``to_unitize`` is ``True``.

      :Type: *ndarray*
      :Required by: :func:`~HS_WFP.deunitize`,
                    (optional) :func:`~HS_WFP.calculate_gradients`
      :Updated by: (optional) :func:`~HS_WFP.compute_poly_coeffs`,
                   (optional) :func:`~HS_WFP.compute_poly_coeffs_weighted`

    - ``SSR``: squared sum of the residues after fitting the gradients to the polynomial
      basis functions

      :Type: positive *float*
      :Updated by: :func:`~HS_WFP.compute_SSR`

    - ``seidel_coeffs``: a *dict* of the Seidel coefficients derived from the polynomial
      basis function coefficients

      :Type: *dict*
      :Update by: (optional) :func:`~HS_WFP.compute_seidel_coeffs`

    - ``zernike_coeffs``: an *ndarray* of the Zernike coefficients derived from the
      polynomial basis function coefficients

      :Type: *dict*
      :Update by: (optional) :func:`~HS_WFP.compute_zernike_coeffs`

    - ``X_all_bases``: a *list* of all basis functions that can be used in the least squares
      fitting of the x components of the gradients

      :Type: *list*
      :Required by: :func:`~HS_WFP.build_bases`
      :Updated by: :func:`~HS_WFP.build_all_bases`

    - ``Y_all_bases``: a *list* of all basis functions that can be used in the least squares
      fitting of the y components of the gradients

      :Type: *list*
      :Required by: :func:`~HS_WFP.build_bases`
      :Updated by: :func:`~HS_WFP.build_all_bases`

    - ``X_bases``: a *list* of all basis functions to be used in the least squares fitting
      of the x components of the gradients

      :Type: *list*
      :Required by: :func:`~HS_WFP.build_XY`, :func:`~HS_WFP.build_XY_nu`
      :Updated by: :func:`~HS_WFP.build_bases`

    - ``Y_bases``: a *list* of all basis functions to be used in the least squares fitting
      of the y components of the gradients

      :Type: *list*
      :Required by: :func:`~HS_WFP.build_XY`, :func:`~HS_WFP.build_XY_nu`
      :Updated by: :func:`~HS_WFP.build_bases`

    - ``X``: an *ndarray* of the values of the functions in ``X_bases`` evaluated at each
      coord of ``centroids``

      :Type: *ndarray*
      :Required by: :func:`~HS_WFP.build_M_matrix`, :func:`~HS_WFP.compute_poly_coeffs`,
                    :func:`~HS_WFP.compute_poly_coeffs_weighted`,
      :Updated by: :func:`~HS_WFP.build_XY`

    - ``Y``: an *ndarray* of the values of the functions in ``Y_bases`` evaluated at each
      coord of ``centroids``

      :Type: *ndarray*
      :Required by: :func:`~HS_WFP.build_M_matrix`, :func:`~HS_WFP.compute_poly_coeffs`,
                    :func:`~HS_WFP.compute_poly_coeffs_weighted`,
      :Updated by: :func:`~HS_WFP.build_XY`

    - ``M``: the M matrix used in the least squares fitting

      :Type: *ndarray*
      :Required by: :func:`~HS_WFP.compute_poly_coeffs`,
                    :func:`~HS_WFP.compute_poly_coeffs_weighted`
      :Updated by: :func:`~HS_WFP.build_M_matrix`

    - ``b``: the b vector used in the least squares fitting

      :Type: *ndarray*
      :Updated by: :func:`~HS_WFP.compute_poly_coeffs`,
                   :func:`~HS_WFP.compute_poly_coeffs_weighted`

    - ``weights``: an *ndarray* of weights used in the weighted least squares fitting

      This variable is used to weight (or scale) ``gradients``, ``X`` and ``Y`` before
      calculating the polynomial coefficients for the wavefront.

      As long as its shape is the same as that of ``gradients``, ``weights`` can be an
      array of any positive numbers (cannot be zero). However, in order for the weighted
      least squares fit to be meaningful, ``weights`` should be roughly proportional to
      the uncertainties of the measured gradients.

      For example, the standard deviation of each coordinate of each centroid, calculated
      using multiple image frames (or averaged images), can be used as ``weights``.

      :Type: *ndarray*
      :Updated by: :func:`~HS_WFP.compute_poly_coeffs_weighted`

    """

    no_of_bases_array = [2, 5, 9, 14, 20, 27]
    """A class variable specifying the numbers of basis functions for each order.

    For example, if the order of the polynomials is 1, the number of basis
    functions is 2 (although order 1 is hardly useful). The maximum order
    implemented in this class is six, for which we have 27 basis functions.

    :Type: *list*
    :Required by: :func:`~HS_WFP.determine_no_of_bases`

    """

    def __init__(self, hsgr=None, order=6):
        self.unitization_length = 1.0
        self.to_unitize = False
        self.order = order
        self.no_of_bases = None
        self.hsgradients = hsgr
        self.centroids = None
        self.gradients = None
        self.poly_bases_names = None
        self.poly_all_bases_names = None
        self.poly_all_bases = None
        self.poly_coeffs = None
        self.poly_coeffs_array = None
        self.poly_coeffs_u = None
        self.poly_coeffs_array_u = None
        self.SSR = None
        self.seidel_coeffs = None
        self.zernike_coeffs = None
        self.M = None
        self.b = None
        self.X = None
        self.Y = None
        self.X_bases = None
        self.Y_bases = None
        self.X_all_bases = None
        self.Y_all_bases = None
        self.weights = None

        self.build_all_bases()
        self.determine_no_of_bases(order)

        if hsgr.__class__.__name__ == "HS_Gradients":
            self.hsgradients = hsgr
            self.gradients = hsgr.gradients[:, 0:2]
            self.centroids = hsgr.gradients[:, 2:4]

    def update_centroids_and_gradients(self):
        """Update centroids and gradients instance variables.

        :Requires: ``hsgradients``
        :Updates: ``centroids``, ``gradients``

        """
        hsgr = self.hsgradients
        self.gradients = hsgr.gradients[:, 0:2]
        self.centroids = hsgr.gradients[:, 2:4]

    def determine_no_of_bases(self, order):
        """Determine the number of basis functions to use given the value of ``order``.

        After ``no_of_bases`` is determined, this method also prepares the basis
        functions that are needed for the calculation of the coefficients.

        :param order: a value from 1 to 6
        :type order: *integer*
        :Uses: :func:`~HS_WFP.build_bases`
        :Updates: ``order``, ``no_of_bases``

        """
        if order > 7:
            raise Exception(
                "The parameter order must be an integer " + "between 0 and 6."
            )
        self.order = order
        self.no_of_bases = HS_WFP.no_of_bases_array[order - 1]
        self.build_bases()

    def build_XY(self):
        """Build ``X`` and ``Y`` arrays

        :Requires: ``centroids``, ``to_unitize``, ``X_bases``, ``Y_bases``,
                   (optional) ``unitization_length``
        :Updates: ``X``, ``Y``

        """
        ctr = self.centroids.copy()

        if self.to_unitize is True:
            ctr = ctr / self.unitization_length

        Xc = [fn(*(ctr[:, 0], ctr[:, 1])) for fn in self.X_bases]
        Yc = [fn(*(ctr[:, 0], ctr[:, 1])) for fn in self.Y_bases]

        self.X = array(Xc)
        self.Y = array(Yc)

    def build_XY_nu(self):
        """Build non-unitized versions of ``X`` and ``Y``, and return them as output.

        :Requries: ``centroids``
        :Returns: the calculated arrays
        :rtype: *ndarray*

        """
        ctr = self.centroids.copy()

        Xc = [fn(*(ctr[:, 0], ctr[:, 1])) for fn in self.X_bases]
        Yc = [fn(*(ctr[:, 0], ctr[:, 1])) for fn in self.Y_bases]

        X = array(Xc)
        Y = array(Yc)

        return X, Y

    def build_M_matrix(self):
        """Build ``M`` using ``X`` and ``Y``

        :Requires: ``X``, ``Y``
        :Updates: ``M``

        """
        self.M = dot(self.X, self.X.T) + dot(self.Y, self.Y.T)

    def compute_poly_coeffs(self):
        """Calculate and update the coefficients of the polynomial basis functions

        :Requries: ``gradients``, ``no_of_bases``, ``poly_bases_names``
        :Uses: :func:`~HS_WFP.build_XY`, :func:`~HS_WFP.build_M_matrix`,
               :func:`~HS_WFP.compute_SSR`, (optional) :func:`~HS_WFP.deunitize`
        :Updates: ``b``, ``poly_coeffs_array``, ``poly_coeffs``, ``SSR``,
                  (optional) ``poly_coeffs_u``, (optional) ``poly_coeffs_array_u``

        """
        self.build_XY()
        self.build_M_matrix()

        gr = -self.gradients

        self.b = dot(self.X, gr[:, 0]) + dot(self.Y, gr[:, 1])

        if self.to_unitize is True:
            self.poly_coeffs_array_u = dot(linalg.inv(self.M), self.b)
            self.poly_coeffs_u = {
                self.poly_bases_names[i]: self.poly_coeffs_array_u[i]
                for i in arange(self.no_of_bases)
            }
            self.deunitize()
        else:
            self.poly_coeffs_array = dot(linalg.inv(self.M), self.b)

        self.poly_coeffs = {
            self.poly_bases_names[i]: self.poly_coeffs_array[i]
            for i in arange(self.no_of_bases)
        }

        self.compute_SSR()

    def compute_poly_coeffs_weighted(self, w):
        """Calculate and update the coefficients of the polynomial basis functions
        using the weighted ``gradients``, ``X`` and ``Y``.

        :param w: the weights to be used in the calculation
        :type w: *ndarray*
        :Requires: ``gradients``, ``poly_bases_names``, ``no_of_bases``
        :Uses: :func:`~HS_WFP.build_XY`, :func:`~HS_WFP.build_M_matrix`,
               :func:`~HS_WFP.compute_SSR`, (optional) :func:`~HS_WFP.deunitize`
        :Updates: ``weights``, ``b``, ``X``, ``Y``,
                  ``poly_coeffs_array``, ``poly_coeffs``, ``SSR``,
                  (optional) ``poly_coeffs_u``, (optional) ``poly_coeffs_array_u``

        """
        self.build_XY()
        if shape(w) != shape(self.centroids):
            raise Exception(
                "The shape of the weight parameter must be "
                + "the same as the shape of the centroids array."
            )

        self.weights = w
        wx = tile(w[:, 0], (shape(self.X)[0], 1))
        wy = tile(w[:, 1], (shape(self.X)[0], 1))
        self.X = self.X / wx
        self.Y = self.Y / wy
        wgr = -self.gradients / w
        self.build_M_matrix()

        self.b = dot(self.X, wgr[:, 0]) + dot(self.Y, wgr[:, 1])

        if self.to_unitize is True:
            self.poly_coeffs_array_u = dot(linalg.inv(self.M), self.b)
            self.poly_coeffs_u = {
                self.poly_bases_names[i]: self.poly_coeffs_array_u[i]
                for i in arange(self.no_of_bases)
            }
            self.deunitize()
        else:
            self.poly_coeffs_array = dot(linalg.inv(self.M), self.b)

        self.poly_coeffs = {
            self.poly_bases_names[i]: self.poly_coeffs_array[i]
            for i in arange(self.no_of_bases)
        }

        self.compute_SSR()

    def compute_SSR(self):
        """Calcualte the squared sum of the residues between the gradients used in the
        fit and the gradients synthesized using the coefficients obtained from the fit

        :Requires: ``gradients``
        :Uses: :func:`~HS_WFP.calculate_gradients`
        :Updates: ``SSR``

        """
        gr = self.calculate_gradients()
        self.SSR = ((self.gradients - gr) ** 2).sum()

    def calculate_gradients(self, coeffs=None):
        """Calculate the gradients from the coefficients of the polynomial basis functions

        If the input parameter ``coeffs`` is not given, the existing instance variable
        of the coefficients will be used.

        If the input parameter ``coeffs`` is given, its length must be equal to the number
        of bases ``no_of_bases``.

        :param coeffs: an array of the coefficients for the polynomial basis functions
        :type coeffs: *ndarray*
        :Requires: (optional) ``poly_coeffs_array``
        :Uses: (optional) :func:`~HS_WFP.build_XY_nu`
        :Returns: the gradients calculated from the coefficients
        :rtype: *ndarray*

        """
        # if coeffs is None:
        #     if self.to_unitize is True:
        #         coeffs = self.poly_coeffs_array_u
        #     else:
        #         coeffs = self.poly_coeffs_array

        if coeffs is None:
            coeffs = self.poly_coeffs_array

        if self.to_unitize is True:
            X, Y = self.build_XY_nu()
        else:
            X = self.X
            Y = self.Y

        grx = -1 * (tile(coeffs, (size(X[0]), 1)).T * X).sum(0)
        gry = -1 * (tile(coeffs, (size(Y[0]), 1)).T * Y).sum(0)
        gr = array([grx, gry]).T

        return gr

    def calculate_wf(
        self,
        coeffs=None,
        resolution=(1024, 1024),
        origin=(511.5, 511.5),
        spacing=(12e-6, 12e-6),
    ):
        """Generate a wavefront from the polynomial coefficients.

        :param coeffs: the coefficients for the polynomial basis functions
        :type coeffs: *ndarray*
        :param resolution: the resolution of the wavefront to be generated
        :type resolution: *tuple*
        :param origin: the coordinates of the origin in pixel units
        :type origin: *tuple*
        :param spacing: the vertical and horizontal spacings between the grid points
        :type spacing: *tuple*
        :Requires: ``poly_all_bases``, (optional) ``poly_coeffs_array``
        :Returns: a two-dimentional array of the generated wavefront
        :rtype: *ndarray*

        """

        xr = (arange(0, resolution[0]) - origin[0]) * spacing[0]
        yr = (arange(0, resolution[1]) - origin[1]) * spacing[1]

        xg, yg = meshgrid(xr, yr)
        wf = zeros(resolution)

        if coeffs is None:
            coeffs = self.poly_coeffs_array

        for k, pc in enumerate(coeffs):
            wf = wf + coeffs[k] * self.poly_all_bases[k](*(xg, yg))

        return wf - wf.min()

    def deunitize(self):
        """Rescale the coefficients of the unitized basis functions back to the values in
        meter units.

        :Requires: ``unitization_length``, ``poly_coeffs_array_u``,
                   ``poly_bases_names``, ``no_of_bases``
        :Updates: ``poly_coeffs_array``, ``poly_coeffs``

        """
        ul = self.unitization_length
        duarr_all = array(
            [
                1,
                1,
                ul,
                ul,
                ul,
                ul ** 2,
                ul ** 2,
                ul ** 2,
                ul ** 2,
                ul ** 3,
                ul ** 3,
                ul ** 3,
                ul ** 3,
                ul ** 3,
                ul ** 4,
                ul ** 4,
                ul ** 4,
                ul ** 4,
                ul ** 4,
                ul ** 4,
                ul ** 5,
                ul ** 5,
                ul ** 5,
                ul ** 5,
                ul ** 5,
                ul ** 5,
                ul ** 5,
            ]
        )
        duarr = duarr_all[0 : self.no_of_bases]

        self.poly_coeffs_array = self.poly_coeffs_array_u / duarr

        self.poly_coeffs = {
            self.poly_bases_names[i]: self.poly_coeffs_array[i]
            for i in arange(self.no_of_bases)
        }

    def compute_seidel_coeffs(self, coeffs=None):
        """Compute the coefficients of some Seidel functions from the polynomial
        coefficients.

        If the input parameter ``coeffs`` is given, this method returns the Seidel
        coefficients calculated from them without updating the instance variable
        ``seidel_coeffs``..

        If ``coeffs`` is not given, this method calculates the Seidel coefficients
        from the instance variable ``poly_coeffs_array`` and updates ``seidel_coeffs``.

        This method expects ``coeffs`` to be an array of at least 5 elements, or a
        *dict* containing at least the following fields: 'x', 'y', 'xy', 'x2' and
        'y2'.

        :param coeffs: the coefficients of the polynomials
        :type coeffs: *ndarray* or *dict*
        :Requires: (optional) ``poly_coeffs_array``
        :Updates: (optional) ``seidel_coeffs``
        :Returns: (optional) the Seidel coefficients
        :rtype: *dict*

        """
        seidel_coeffs = {}
        update_var = False

        if coeffs is None:
            coeffs_arr = self.poly_coeffs_array.copy()
            update_var = True
        elif type(coeffs) is dict:
            coeffs_arr = [
                coeffs["x"],
                coeffs["y"],
                coeffs["x2"],
                coeffs["xy"],
                coeffs["y2"],
            ]
        elif (type(coeffs) is not list) or (type(coeffs) is not ndarray):
            raise Exception(
                "The input parameter coeffs must be a dict, "
                + "a list or a numpy array of the numeric values."
            )
        else:
            coeffs_arr = coeffs

        P = coeffs_arr[2]
        Q = coeffs_arr[3]
        R = coeffs_arr[4]

        seidel_coeffs["prism_x"] = coeffs_arr[0]
        seidel_coeffs["prism_y"] = coeffs_arr[1]
        seidel_coeffs["prism"] = (coeffs_arr[0] ** 2 + coeffs_arr[1] ** 2) ** 0.5
        seidel_coeffs["alpha"] = arctan2(coeffs_arr[1], coeffs_arr[0])
        seidel_coeffs["cylindrical_power"] = 2 * ((R - P) ** 2 + Q ** 2) ** 0.5
        seidel_coeffs["spherical_power"] = (
            P + R - 0.5 * (seidel_coeffs["cylindrical_power"])
        )
        seidel_coeffs["phi"] = 0.5 * arctan2(-Q, R - P)

        if update_var is True:
            self.seidel_coeffs = seidel_coeffs
        else:
            return seidel_coeffs

    def compute_zernike_coeffs(self, coeffs=None):
        """Compute the coefficients of some Zernike functions from the polynomial
        coefficients.

        If the input parameter ``coeffs`` is given, this method returns the Zernike
        coefficients calculated from them without updating the instance variable
        ``seidel_coeffs``..

        If ``coeffs`` is not given, this method calculates the Zernike coefficients
        from the instance variable ``poly_coeffs_array`` and updates ``seidel_coeffs``.

        This method expects ``coeffs`` to be an array of at least 5 elements, or a
        *dict* containing at least the following fields: 'x', 'y', 'xy', 'x2' and
        'y2'.

        Note that the Zernike coefficients calculated with this method are not those
        of true Zernike functions, as they are not scaled to be orthogonal over
        a disc of size comparable to the image size. The method will need to be
        revised to apply appropriate scaling to the Zernike functions.

        :param coeffs: the coefficients of the polynomials
        :type coeffs: *ndarray* or *dict*
        :Requires: (optional) ``poly_coeffs_array``
        :Updates: (optional) ``seidel_coeffs``
        :Returns: (optional) the Seidel coefficients
        :rtype: *dict*

        """
        update_var = False

        if coeffs is None:
            update_var = True
            coeffs_arr = self.poly_coeffs_array
        elif type(coeffs) is dict:
            coeffs_arr = [
                coeffs["x"],
                coeffs["y"],
                coeffs["x2"],
                coeffs["xy"],
                coeffs["y2"],
            ]
        elif (type(coeffs) is not list) or (type(coeffs) is not ndarray):
            raise Exception(
                "The input parameter coeffs must be a dict, "
                + "a list or a numpy array of the numeric values."
            )
        else:
            coeffs_arr = coeffs

        z = zeros(5)
        z[0] = coeffs_arr[0]
        z[1] = coeffs_arr[1]
        z[2] = (coeffs_arr[2] + coeffs_arr[4]) / 4.0
        z[3] = (coeffs_arr[2] - coeffs_arr[4]) / 2.0
        z[4] = coeffs_arr[3] / 2.0

        if update_var is True:
            self.zernike_coeffs = z

    def build_bases(self):
        """Set up the basis functions according to ``no_of_bases``.

        This method simply takes a number of the polynomial functions from ``X_all_bases``
        ``Y_all_bases`` and the polynomial basis function names from
        ``poly_all_bases_names``. The number of items to take is determined by
        ``no_of_bases``.

        :Requires: ``X_all_bases``, ``Y_all_bases``, ``poly_all_bases_names``,
                   ``no_of_bases``
        :Updates: ``X_bases``, ``Y_bases``, ``poly_bases_names``

        """
        self.X_bases = self.X_all_bases[0 : (self.no_of_bases)]
        self.Y_bases = self.Y_all_bases[0 : (self.no_of_bases)]
        self.poly_bases_names = self.poly_all_bases_names[0 : (self.no_of_bases)]

    def build_all_bases(self):
        """Set up the X, Y and polynomial basis functions and the names of the bases
        functions that are available in this class.

        This method prepares sets of all basis functions that can be used in the least
        squares fit of gradients and the construction of wavefronts.

        :func:`~HS_WFP.build_bases` can then take subsets of the functions from these
        sets. ``no_of_bases``, derived from ``order``, determines how many functions
        should be taken.

        :Updates: ``X_all_bases``, ``Y_all_bases``, ``poly_all_bases``,
                  ``poly_all_bases_names``

        """
        self.X_all_bases = [
            lambda x, y: ones(size(x)),
            lambda x, y: zeros(size(x)),
            lambda x, y: 2 * x,
            lambda x, y: y,
            lambda x, y: zeros(size(x)),
            lambda x, y: 3 * x ** 2,
            lambda x, y: 2 * x * y,
            lambda x, y: y ** 2,
            lambda x, y: zeros(size(x)),
            lambda x, y: 4 * x ** 3,
            lambda x, y: 3 * x ** 2.0 * y,
            lambda x, y: 2 * x * y ** 2,
            lambda x, y: y ** 3,
            lambda x, y: zeros(size(x)),
            lambda x, y: 5 * x ** 4,
            lambda x, y: 4 * x ** 3 * y,
            lambda x, y: 3 * x ** 2 * y ** 2,
            lambda x, y: 2 * x * y ** 3,
            lambda x, y: y ** 4,
            lambda x, y: zeros(size(x)),
            lambda x, y: 6 * x ** 5,
            lambda x, y: 5 * x ** 4.0 * y,
            lambda x, y: 4 * x ** 3.0 * y ** 2,
            lambda x, y: 3 * x ** 2 * y ** 3,
            lambda x, y: 2 * x * y ** 4,
            lambda x, y: y ** 5,
            lambda x, y: zeros(size(x)),
        ]

        self.Y_all_bases = [
            lambda x, y: zeros(size(x)),
            lambda x, y: ones(size(x)),
            lambda x, y: zeros(size(x)),
            lambda x, y: x,
            lambda x, y: 2 * y,
            lambda x, y: zeros(size(x)),
            lambda x, y: x ** 2,
            lambda x, y: 2 * x * y,
            lambda x, y: 3 * y ** 2,
            lambda x, y: zeros(size(x)),
            lambda x, y: x ** 3,
            lambda x, y: 2 * x ** 2 * y,
            lambda x, y: 3 * x * y ** 2,
            lambda x, y: 4 * y ** 3,
            lambda x, y: zeros(size(x)),
            lambda x, y: x ** 4,
            lambda x, y: 2 * x ** 3 * y,
            lambda x, y: 3 * x ** 2 * y ** 2,
            lambda x, y: 4 * x * y ** 3,
            lambda x, y: 5 * y ** 4,
            lambda x, y: zeros(size(x)),
            lambda x, y: x ** 5,
            lambda x, y: 2 * x ** 4 * y,
            lambda x, y: 3 * x ** 3 * y ** 2,
            lambda x, y: 4 * x ** 2 * y ** 3,
            lambda x, y: 5 * x * y ** 4,
            lambda x, y: 6 * y ** 5,
        ]

        self.poly_all_bases = [
            lambda x, y: x,
            lambda x, y: y,
            lambda x, y: x ** 2,
            lambda x, y: x * y,
            lambda x, y: y ** 2,
            lambda x, y: x ** 3,
            lambda x, y: x ** 2 * y,
            lambda x, y: x * y ** 2,
            lambda x, y: y ** 3,
            lambda x, y: x ** 4,
            lambda x, y: x ** 3 * y,
            lambda x, y: x ** 2 * y ** 2,
            lambda x, y: x * y ** 3,
            lambda x, y: y ** 4,
            lambda x, y: x ** 5,
            lambda x, y: x ** 4 * y,
            lambda x, y: x ** 3 * y ** 2,
            lambda x, y: x ** 2 * y ** 3,
            lambda x, y: x * y ** 4,
            lambda x, y: y ** 5,
            lambda x, y: x ** 6,
            lambda x, y: x ** 5 * y,
            lambda x, y: x ** 4 * y ** 2,
            lambda x, y: x ** 3 * y ** 3,
            lambda x, y: x ** 2 * y ** 4,
            lambda x, y: x * y ** 5,
            lambda x, y: y ** 6,
        ]

        self.poly_all_bases_names = [
            "x",
            "y",
            "x2",
            "xy",
            "y2",
            "x3",
            "x2y",
            "xy2",
            "y3",
            "x4",
            "x3y",
            "x2y2",
            "xy3",
            "y4",
            "x5",
            "x4y",
            "x3y2",
            "x2y3",
            "xy4",
            "y5",
            "x6",
            "x5y",
            "x4y2",
            "x3y3",
            "x2y4",
            "xy5",
            "y6",
        ]
