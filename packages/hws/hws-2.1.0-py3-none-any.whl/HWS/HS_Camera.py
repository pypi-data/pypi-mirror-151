"""
Copyright (C) University of Adelaide, Australia - All Rights Reserved
This source code is protected under proprietary reference only license.
Please refer to the accompanying LICENSE file for further information.
"""

import os
import subprocess as sp
from numpy import *
from datetime import datetime, timedelta
from builtins import input

from HWS.HS_CamConfig import *
from HWS.HS_Image import *


class HS_Camera:
    """A class to operate a DALSA Pantera 1M60 Camera through a frame grabber.

    This class should be a single communication point between the Hartmann
    Sensor equipments (camera and frame grabber) and the rest of the codes.

    It holds variables and methods relevant to the system initialization
    and diagnostics, as well as image acquisition from the frame grabber.

    **Instantiation**

    During instantiation, if the input parmeter ``check_status`` is ``True``,
    the class checks if the connection can be made to the camera assumed
    connected to the device channel specified by the instance variable
    ``device_no``. If the connection cannot be made, it raises an error and
    exits.

    After a successful connection, the class creates an instance of the
    class :class:`HS_CamConfig <HWS.HS_CamConfig.HS_CamConfig>` and
    assigns it to the instance variable ``camera_parameters``.

    Then if the instance variable ``camera_folder`` is not set by a user,
    :func:`~HS_Camera.set_camera_folder` is called to set a default folder for
    storing acquired image frames and other data.

    **Camera Commands**

    All of the Dalsa Pantera 1M60 camera commands are represented in
    this class, although not all of them may be useful or relevant for a
    normal day-to-day operation of the camera.

    As such the descriptions of those methods are not full, and a user should
    consult the camera manual for the details.

    To call the camera commands from Python, some methods use the method
    :func:`~HS_Camera.serial_cmd` and other methods (which requires additional
    parameters) use :func:`~HS_Camera.serial_cmd_alt`. This is because the
    methods with parameters do not run when passed as a *list* (as was
    recommended by Python) to the medhos in the ``subprocess`` module.

    To overcome this, the camera commands with parameters are called by
    passing the command and its parameters as a whole string, which is what
    :func:`~HS_Camera.serial_cmd_alt` does.

    **Instance Variables**

    - ``device_no``: the number 0 or 1 specifying the frame grabber's device
      channel to which a camera is connected.

      :Type: *integer* of value 0 or 1

    - ``fg_directory``: the directory in which the frame grabber is installed.

      During instantiation, the value of this variable is obtained from the
      instance variable ``fg_directory`` of
      :class:`HS_Camconfig <HWS.HS_CamConfig>`.

      :Type: *string*

    - ``camera_config_file``: the name of the camera configuration file
      (e.g., dalsa_1m60.cfg)

      :Type: *string*

    - ``camera_parameters``: an instance of HS_CamConfig that holds the
      camera paremeters retrieved by the frame grabber ``gcp`` command.

      :Type: an instance of :class:`HS_Camconfig <HWS.HS_CamConfig>`
      :Updated by: :func:`~HS_Camera.get_camera_parameters`

    - ``valid_image_shape``: the horizontal and vertical dimensions of
      the CCD array of the camera.

      :Type: *tuple* of two positive *integers*

    - ``dark_image``: an image acquired with neither ambient light nor a light
      source.

      It is up to a user to ensure that the image is really dark.

      :Type: *ndarray*

    - ``frame_folder``: the folder within which the acquired image frames are
      stored.

      :Type: *string*

    - ``temperature``: a list of the camera digitizer and sensor temperatures.

      The variable has two elements, ``sensor`` and ``digitizer`` temperatures
      that one can retrieved by using the camera command ``vt``.

      :Type: *dict* of two *float* values
      :Updated by: :func:`~HS_Camera.get_temperature`

    - ``exposure_time``: the camera exposure time in seconds.

      :Type: positive *float*
      :Updated by: :func:`~HS_Camera.get_exposure_time`

    - ``timeouts``: the number of timeouts that occurred during the frame
      acquisition.

      :Type: non-negative *integer*
      :Updated by: :func:`~HS_Camera.parse_take_message`

    - ``overruns`` the number of overruns that occurred during the frame
      acquisition.

      :Type: non-negative *integer*
      :Updated by: :func:`~HS_Camera.parse_take_message`

    - ``frame_rate``: the frame rate used to acquire the frames.

      :Type: positive *integer*
      :Updated by: :func:`~HS_Camera.parse_take_message`

    - ``gpstime``: the gps time at which the most recent frame was acquired.

      :Type: positive *integer*
      :Updated by: :func:`~HS_Camera.take_frames`

    - ``bad_pixels_data``: *dict* of data gathered when the bad pixels are
      located using a dark image.

      The variable has the following fields:

      - ``csn``: the camera serial number
      - ``pv_threshold``: threshold pixel value used to determine bad pixels
      - ``coords``: the coordinates of the bad pixels (pixel units)
      - ``gpstime``: the gps time at which the last frame was taken
      - ``exposure_time``: the exposure time used to take the frames

      :Type: *dict*
      :Updated by: :func:`~HS_Camera.take_and_locate_bad_pixels`

    - ``camera_folder``: the folder in which the bad pixels data, the acquired
      frames, reference centroids, etc. are stored.

      If it is not defined by a user at instantiation,
      :func:`~HS_Camera.set_camera_folder` will set it to the default value and
      ensure that the camera folder exists.

      :Type: *string*
      :Updated by: (optional) :func:`~HS_Camera.set_camera_folder`

    - ``take_command_list``: a list of a command and parameters used to take the
      image frames.

      :Type: *list* of *strings*
      :Updated by: :func:`~HS_Camera.build_take_command`

      It is not used by the instance methods, but is here so that a user can
      verify what commands were used to take the image frames.

    - ``take_command_string``: a string of the command and parameters used to
      take the image frames.

      It is costructed by inserting space in between and concatenating all the
      entries in ``take_command_list``.

      :Type: *string*
      :Updated by: :func:`~HS_Camera.build_take_command`

      It is not used by the instance methods, but is here so that a user can
      verify what commands were used to take the image frames.

      .. note:: The variables below are currently not in use, and may be removed
                in future revisions unless found useful.

    - ``lever_arm``: the length of the lever arm of the camera); the distance
      between the Hartmann plate and the CCD (in meters).

      :Type: positive *float*

    - ``exposure_default_incr``
    - ``pcmax``
    - ``upper_th``
    - ``lower_th``
    - ``pixel_size``
    - ``background_std``
    - ``test_image``
    - ``responsivity``
    - ``no_of_images``
    - ``max_PV``
    - ``background``
    """

    # This is the top folder in which the camera folder will be made if you use
    # set_camera_folder method.
    master_folder = "/home/controls/camera_folder/"
    """A class variable specifying the folder inside which all camera folders
    are to be found.

    :Type: *string*
    :Required by: :func:`~HS_Camera.set_camera_folder`
    """

    def __init__(self, device_no=0, camera_folder=None, check_status=True):
        self.fg_directory = None
        self.camera_config_file = "dalsa_1m60.cfg"
        self.camera_parameters = None
        self.lever_arm = None
        self.pixel_size = 12e-6
        self.valid_image_shape = (1024, 1024)
        self.max_PV = 4095
        self.background = None
        self.background_std = None
        self.dark_image = None
        self.test_image = None
        self.responsivity = None
        self.frame_folder = None
        self.temperature = None
        self.exposure_time = None
        self.no_of_images = None
        self.timeouts = None
        self.overruns = None
        self.frame_rate = None
        self.exposure_default_incr = None
        self.pcmax = None
        self.upper_th = None
        self.lower_th = None
        self.gpstime = None
        self.bad_pixels_data = None
        self.camera_folder = camera_folder

        if (device_no != 0) and (device_no != 1):
            raise InvalidDeviceNo

        self.device_no = int(device_no)
        self.camera_parameters = HS_CamConfig()
        self.fg_directory = self.camera_parameters.fg_directory

        self.take_command_list = None
        self.take_command_str = None

        if check_status is True:
            self.check_camera_connection()
            self.get_camera_parameters()

        if (self.camera_folder is None) and (check_status is True):
            self.set_camera_folder()

        # res = self.check_camera_connection()
        # if res != 1:
        #     pass

        # self.exposure_time = self.get_exposure_time()
        # self.get_camera_parameters()

    def set_camera_folder(self):
        """Set up the default camera folder in which to store data.

        :Updates: ``camera_folder``

        """
        csn = self.camera_parameters.camera_serial_number
        cf = HS_Camera.master_folder + csn

        if os.path.exists(HS_Camera.master_folder):
            if not os.path.exists(cf):
                print("The camera folder " + csn + " does not exist." + "Creating...")
                os.makedirs(cf)
                print("Created the camera folder: " + cf + "/")
        else:
            print(
                "The master folder "
                + HS_Camera.master_folder
                + " does not exist. "
                + "Creating..."
            )
            os.makedirs(HS_Camera.master_folder)
            print("Ceated the master folder: " + HS_Camera.master_folder)
            os.makedirs(cf)
            print("Created the camera folder: " + cf)

        self.camera_folder = cf + "/"

    def on_or_off(self):
        """Check if the camera is accessible.

        :Uses: :func:`~HS_Camera.serial_cmd`
        :Returns: 0 (inaccessible) or 1 (accessible)
        :rtype: *integer*

        """
        try:
            scout = self.serial_cmd("vt")
        except SerialCommandFailure:
            print("The camera is not accessible")
            return 0

        if "OK>" in scout["stdout"]:
            print("The camera is accessible")
            return 1
        else:
            print("The camera is not accessible")
            return 0

    def check_camera_connection(self, n=1):
        """Check the camera connection multiple times.

        If the connection fails, advises a user to check the equipment. If the
        connection cannot be made after a certain number of attempts (beyond the
        first attempt), the method raises an exception.

        If n is zero, no further attempts are made beyond the first one.

        :param n: the number of times to re-attempt connecting to the camera
        :type n: *integer*
        :Uses: :func:`~HS_Camera.on_or_off`

        """
        if n > 0:
            for ii in arange(n):
                flag = self.on_or_off()
                if flag == 1:
                    break
                else:
                    foo = input(
                        "Please check the equipments, then "
                        + "hit any key to check the connection again."
                    )
        elif n == 0:
            flag = self.on_or_off()
        else:
            raise Exception("n must be a positive integer.")
        if flag != 1:
            raise CameraInaccessible

    def load_camera_config(self, ccf=None):
        """Load the camera configuration file into the frame grabber.

        This method is not in use at the moment, since connection failure often
        requires resolution that is beyond the capabilities of this class.

        May need a different approach to make this method useful.

        :param ccf: (optional) the full path file name of the configuration
                    file
        :type ccf: *string*
        :Uses: :func:`~HS_Camera.syscom`

        """
        if ccf is None:
            ccf = self.fg_directory + "camera_config/" + self.camera_config_file

        clist = [(self.fg_directory + "initcam"), "-c", str(self.device_no), "-f", ccf]

        cout = self.syscom(clist)

    def take_frames(self, folder=None, fprefix=None, no_of_frames=1, nbuf=1):
        """Take image frames using the camera.

        :param folder: the folder in which to save the image frames
        :type folder: *string*
        :param fprefix: the file prefix for the image frame files
        :param no_of_frames: the number of frames to take
        :param nbuf: the number of ring buffers to use when taking the frames
        :type nbuf: *integer* (from 1 to 4)
        :Uses: :func:`~HS_Camera.build_take_command`, :func:`~HS_Camera.syscom`,
               :func:`~HS_Camera.parse_take_message`, :func:`~HS_Camera.utc2gps`
        :Updates: ``gpstime``, ``fprefix``, ``frame_folder``, ``frame_rate``,
                  ``timeouts``, ``overruns``

        """
        if folder is None:
            folder = self.camera_folder + "frames/"

        self.frame_folder = folder

        if fprefix is None:
            fprefix = "image"

        self.fprefix = fprefix

        self.build_take_command(folder, fprefix, no_of_frames, nbuf)

        if not os.path.exists(folder):
            print("The folder named " + folder + " does not exist. " + "Creating...")
            os.makedirs(folder)
            print("Created the folder: " + folder)

        scout = self.syscom(self.take_command_list)

        self.parse_take_message(scout["stdout"])

        if (self.timeouts + self.overruns) > 0:
            raise AcquisitionFailure(self.timeouts, self.overruns)

        # utc2gps returns a GPS time in days not seconds
        self.gpstime = self.utc2gps(datetime.utcnow()) * 86400

    def take_and_locate_bad_pixels(self, pv_threshold=150, no_of_frames=100, nbuf=1):
        """Take the image frames and locate pixels whose values are higher than
        the specified threshold value.

        The method updates the instance variable ``bad_pixels_data`` which is a
        dict of several fields; for details see the description of the variable.

        The method also saves ``bad_pixel_data`` as a file.

        :param pv_threshold: the threshold pixel value to determine bad pixels
        :type pv_threshold: *float*
        :param no_of_frames: the number of image frames to take
        :type no_of_frames: positive *integer*
        :param nbuf: the number of ring buffers to use when taking the frames
        :type nbuf: *integer* (from 1 to 4)
        :Requires: ``camera_parameters.camera_serial_number``, ``camera_folder``,
                   :class:`HS_Image <HWS.HS_Image.HS_Image>`
        :Uses: :func:`~HS_Camera.take_and_average_frames`,
               :func:`HS_Image.locate_bad_pixels() <HWS.HS_Image.HS_Image.locate_bad_pixels>`,
        :Updates: ``bad_pixels_data``

        """
        csn = self.camera_parameters.camera_serial_number
        folder = self.camera_folder + "dark_images/"
        nof = no_of_frames
        nbf = nbuf
        hsi = self.take_and_average_frames(
            folder, fprefix="dark", no_of_frames=nof, nbuf=nbf
        )
        hsi.locate_bad_pixels(pv_threshold)

        bad_pixels_data = {}
        bad_pixels_data["csn"] = csn
        bad_pixels_data["pv_threshold"] = pv_threshold
        bad_pixels_data["coords"] = hsi.bad_pixels
        bad_pixels_data["gpstime"] = self.gpstime

        self.get_exposure_time()
        bad_pixels_data["exposure_time"] = self.exposure_time

        bp_fileloc = self.camera_folder + "bad_pixels_data_" + csn
        save(bp_fileloc, bad_pixels_data)

        self.bad_pixels_data = bad_pixels_data

        print(
            "Saved bad pixels data as a file "
            + "bad_pixels_data_"
            + csn
            + ".npy "
            + "in the folder "
            + self.camera_folder
        )
        return hsi

    def build_take_command(self, folder, fprefix, no_of_frames, nbuf):
        """Build a command string used to take image frames.

        :param folder: the folder in which to save the image frames
        :type folder: *string*
        :param fprefix: the file prefix for the image frame files
        :type fprefix: *string*
        :param no_of_frames: the number of frames to take
        :type no_of_frames: positive *integer*
        :param nbuf: the number of ring buffers to use when taking the frames
        :type nbuf: *integer* (from 1 to 4)
        :Requires: ``fg_directory``, ``device_no``
        :Updates: ``take_command_list``, ``take_command_string``

        """
        clist = [
            self.fg_directory + "take",
            "-c",
            str(self.device_no),
            "-N",
            str(nbuf),
            "-s",
            str(1),
            "-l",
            str(no_of_frames),
            "-f",
            folder + fprefix,
        ]

        self.take_command_list = clist
        self.take_command_str = " ".join(clist)

    def take_and_average_frames(
        self, folder=None, fprefix=None, no_of_frames=1, nbuf=1
    ):
        """Take and average the image frames, the return an instance of the
        :class:`HS_Image <HWS.HS_Image>` class.

        :param folder: the folder in which to save the image frames
        :type folder: *string*
        :param fprefix: the file prefix for the image frame files
        :type fprefix: *string*
        :param no_of_frames: the number of frames to take
        :type no_of_frames: positive *integer*
        :param nbuf: the number of ring buffers to use when taking the frames
        :type nbuf: *integer* (from 1 to 4)
        :Uses: :func:`~HS_Camera.take_frames`,
               :class:`HS_Image <HWS.HS_Image.HS_Image>`,
               :func:`HS_Image.read_image() <HWS.HS_Image.HS_Image.read_image>`
        :returns: an instance of :class:`HS_Image <HWS.HS_Image.HS_Image>`
        :rtype: :class:`HS_Image <HWS.HS_Image.HS_Image>`

        """
        self.take_frames(folder, fprefix, no_of_frames, nbuf)

        if fprefix is not None:
            self.fprefix = fprefix

        if folder is not None:
            self.frame_folder = folder

        ifolder = self.frame_folder
        ifprefix = self.fprefix
        hsi = HS_Image(
            location_type="folder",
            location=ifolder,
            fprefix=ifprefix,
            first_frame=1,
            no_of_frames=no_of_frames,
        )

        hsi.read_image()
        return hsi

    def parse_take_message(self, scstr):
        """Parse the output message from the frame grabber to retrieve
        ``frame_rate``, ``timeouts``, and ``overruns`` values.

        :param scstr: the output message
        :type scstr: *string*
        :Updates: ``frame_rate``, ``timeouts``, ``overruns``

        """
        pstr = scstr.split("\n")

        for fs in pstr:
            if "frames/sec" in fs:
                self.frame_rate = float(fs.split(" ")[0])

            if "overruns" in fs:
                stlist = fs.strip().split(" ")

        self.timeouts = int(stlist[2])
        self.overruns = int(stlist[4])

    def check_pixel_maximum(self, im):
        """(Not implemented Yet)"""
        # if im.max() > self.max_PV:
        pass

    def check_image_shape(self, im):
        """Check the shape of the image array.

        The method is not useful at the moment as the class already assumes that an
        image frame is of certain shape when reading it.

        """
        if shape(im) != self.valid_image_shape:
            raise InvalidImageShape(shape(im), self.valid_image_shape)

    def get_camera_parameters(self):
        """Get camera parameters.

        :Uses: :class:`HS_CamConfig <HWS.HS_CamConfig.HS_CamConfig>`,
               :func:`HS_CamConfig.get_parameters() <HWS.HS_CamConfig.HS_CamConfig.get_parameters>`,
               :func:`~HS_Camera.get_temperature`
        :Updates: ``camera_parameters``

        """
        self.camera_parameters = HS_CamConfig()
        self.camera_parameters.get_parameters(self)
        self.get_temperature()

    def get_temperature(self):
        """Get the sensor and digitizer temperatures of the camera

        :Uses: :func:`~HS_Camera.serial_cmd`
        :Updates: ``temperature``

        """
        temperature = {}

        scout = self.serial_cmd("vt")
        pstr = []
        if "OK>" in scout["stdout"]:
            vtstr = scout["stdout"]
            for fs in vtstr.split("\n"):
                fsl = fs.split(":")
                if (size(fsl) == 2) and (len(fsl[1]) > 0):
                    pstr = pstr + [fsl[1].strip()]
        else:
            print("Warning: Failed to obtain camera temperature values.")

        temperature["digitizer"] = float(pstr[0].split(" ")[0])
        temperature["sensor"] = float(pstr[1].split(" ")[0])

        self.temperature = temperature

    def get_exposure_time(self):
        """Get the exposure time (in units of seconds) used to take the image frames.

        :Uses: :func:`~HS_Camera.get_camera_parameters`
        :Updates: ``exposure_time``

        """
        self.get_camera_parameters()
        et = self.camera_parameters.exposure_time.split(" ")[0]
        et = float(et) * 1e-6
        self.exposure_time = et

    def serial_cmd(self, sc):
        """Run a camera serial command.

        :param sc: the serial command to be run
        :type sc: *string* or *list* of *strings*
        :Requires: ``fg_directory``, ``device_no``
        :Uses: :func:`~HS_Camera.syscom`
        :Returns: the output message generated by running the command.
        :rtype: *dict*

        """
        fgdir = self.fg_directory
        cmdlist = [(fgdir + "serial_cmd"), "-c", str(self.device_no)]

        cmdstr = (fgdir + "serial_cmd") + " -c " + str(self.device_no)
        scstr = cmdstr + " " + sc

        if type(sc) is str:
            sclist = cmdlist + [sc]
        elif type(sc) is list:
            sclist = cmdlist + sc
        else:
            raise InvalidCommandFormat

        scout = self.syscom(sclist)

        if scout["stdout"] == "\n":
            # return scout
            raise SerialCommandFailure(sc, scstr)
        elif "Error" in scout["stdout"]:
            # return scout
            raise SerialCommandError(sc, scstr, scout)

        return scout

    def serial_cmd_alt(self, sc):
        """Run a camera serial command.

        Unlike :func:`~HS_Camera.serial_cmd`, this method passes a serial command
        and its associated parameters as a string to :func:`~HS_Camera.syscom_alt`,
        which is necessary if the serial command to be run has extra parameters.

        The serial command ``sc`` must be a string encapsulated by the double
        quotation marks.

        :param sc: the serial command to be run
        :type sc: *string*
        :Requires: ``fg_directory``, ``device_no``
        :Uses: :func:`~HS_Camera.syscom_alt`
        :Returns: the output message generated by running the command.
        :rtype: *dict*

        """
        fgdir = self.fg_directory
        cmdstr = (fgdir + "serial_cmd") + " -c " + str(self.device_no)
        scstr = cmdstr + " " + sc

        scout = self.syscom_alt(scstr)

        if scout["stdout"] == "\n":
            return scout
            raise SerialCommandFailure(sc, scstr)
        elif "Error" in scout["stdout"]:
            # return scout
            raise SerialCommandError(sc, scstr, scout)

        return scout

    def syscom(self, sclist):
        """Run a system command.

        :param sclist: a *list* of the command to be run and the parameters
        :type sclist: *list*
        :Returns: a *dict* consisting of returncode, stdout, and stderr output
        :rtype: *dict*

        """
        mycom = sp.Popen(sclist, stdout=sp.PIPE, stderr=sp.PIPE)
        sco = mycom.communicate()
        scout = {}
        scout["returncode"] = mycom.returncode
        scout["stdout"] = sco[0].decode()
        scout["stderr"] = sco[1].decode()

        return scout

    def syscom_alt(self, scstr):
        """Run a system command.

        Unlike :func:`~HS_Camera.syscom`, this method passes the string of a command
        and its associated parameters as a *string* instead of as a *list*. This is
        necessary when running a camera serial command that contains extra parameters.

        Other system commands with multiple parameters can be run normally using
        :func:`~HS_Camera.syscom`, so this method is used only for some camera serial
        commands.

        :param scstr: a *string* of a system command and parameters
        :type scstr: *string*
        :Returns: a *dict* consisting of returncode, stdout, and stderr output
        :rtype: *dict*

        """
        mycom = sp.Popen(scstr, shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
        sco = mycom.communicate()
        scout = {}
        scout["returncode"] = mycom.returncode
        scout["stdout"] = sco[0].decode()
        scout["stderr"] = sco[1].decode()

        return scout

    def set_output_mode(self, mode, to_output=False):
        """Set the output mode for the camera.

        ``mode`` takes one of two values:
        - 0: single tap readout, maximum 30 fps
        - 1: dual tap readout, maximum 60 fps (default)

        :param mode: 0 or 1
        :type mode: *integer*
        :param to_output: ``True`` to return the output list, ``False``
                          to run quietly
        :type to_output: *boolean*
        :Uses: :func:`~HS_Camera.serial_cmd_alt`,
               :func:`~HS_Camera.get_camera_parameters`
        :Updates: ``camera_parameters``
        :Returns: (optional) a list of the output from running the command
        :rtype: *dict*

        """
        scout = self.serial_cmd_alt('"sos ' + str(mode) + '"')
        self.get_camera_parameters()

        if to_output == True:
            return scout

    def set_data_mode(self, mode, to_output=False):
        """Set the data mode for the camera.

        ``mode`` takes one of three values:
        - 12: 12-bit (default)
        - 10: 10-bit
        - 8: 8-bit

        :param mode: 8, 10 or 12
        :type mode: *integer*
        :param to_output: ``True`` to return the output list, ``False``
                          to run quietly
        :type to_output: *boolean*
        :Uses: :func:`~HS_Camera.serial_cmd_alt`,
               :func:`~HS_Camera.get_camera_parameters`
        :Updates: ``camera_parameters``
        :Returns: (optional) a list of the output from running the command
        :rtype: *dict*

        """
        scout = self.serial_cmd_alt('"oms ' + str(mode) + '"')
        self.get_camera_parameters()

        if to_output == True:
            return scout

    def set_baud_rate(self, rate, to_output=False):
        """Set the serial communication speed for the camera.

        ``rate`` specifies the baud rate of the communication and can take one of
        three values: 9600 (default), 19200 or 57600.

        :param rate: 9600, 19200 or 57600
        :type rate: *integer*
        :param to_output: ``True`` to return the output list, ``False``
                          to run quietly
        :type to_output: *boolean*
        :Uses: :func:`~HS_Camera.serial_cmd_alt`,
               :func:`~HS_Camera.get_camera_parameters`
        :Updates: ``camera_parameters``
        :Returns: (optional) a list of the output from running the command
        :rtype: *dict*

        """
        scout = self.serial_cmd_alt('"sbr ' + str(rate) + '"')
        self.get_camera_parameters()

        if to_output == True:
            return scout

    def set_exposure_mode(self, mode, to_output=False):
        """Set the exposure mode of the camera.

        See the camera manual Section 3.7 for a detailed explanation on the exposure
        mode, exposure time, and the frame rate.

        :param mode: *integer* from 2 to 7
        :type mode: *integer*
        :param to_output: ``True`` to return the output list, ``False``
                          to run quietly
        :type to_output: *boolean*
        :Uses: :func:`~HS_Camera.serial_cmd_alt`,
               :func:`~HS_Camera.get_camera_parameters`
        :Updates: ``camera_parameters``
        :Returns: (optional) a list of the output from running the command
        :rtype: *dict*

        """
        scout = self.serial_cmd_alt('"sem ' + str(mode) + '"')
        self.get_camera_parameters()

        if to_output == True:
            return scout

    def set_exposure_control(self, mode, to_output=False):
        """Enable or disable the camera exposure control.

        ``mode`` takes one of two values:

        - 0: disable exposure control
        - 1: enable exposure control

        Relevant only if the camera is in the exposure mode 3

        :param mode: 0 or 1
        :type mode: *integer*
        :param to_output: ``True`` to return the output list, ``False``
                          to run quietly
        :type to_output: *boolean*
        :Uses: :func:`~HS_Camera.serial_cmd_alt`,
               :func:`~HS_Camera.get_camera_parameters`
        :Updates: ``camera_parameters``
        :Returns: (optional) a list of the output from running the command
        :rtype: *dict*

        """
        scout = self.serial_cmd_alt('"sec ' + str(mode) + '"')
        self.get_camera_parameters()

        if to_output == True:
            return scout

    def set_frame_rate(self, rate, to_output=False):
        """Set the frame acquisition rate.

        See section 3.7.3 of the camera manual for the details.

        :param rate: the frame acquisition rate
        :type rate: positive *float*
        :param to_output: ``True`` to return the output list, ``False``
                          to run quietly
        :type to_output: *boolean*
        :Uses: :func:`~HS_Camera.serial_cmd_alt`,
               :func:`~HS_Camera.get_camera_parameters`
        :Updates: ``camera_parameters``
        :Returns: (optional) a list of the output from running the command
        :rtype: *dict*

        """
        scout = self.serial_cmd_alt('"ssf ' + str(rate) + '"')
        self.get_camera_parameters()

        if to_output == True:
            return scout

    def set_exposure_time(self, duration, to_output=False):
        """Set the exposure time (in microseconds) used to acquire a frame.

        See section 3.7.3 of the camera manual for the details.

        :param duration: the exposure time duration
        :type duration: positive *float*
        :param to_output: ``True`` to return the output list, ``False``
                          to run quietly
        :type to_output: *boolean*
        :Uses: :func:`~HS_Camera.serial_cmd_alt`,
               :func:`~HS_Camera.get_camera_parameters`
        :Updates: ``camera_parameters``
        :Returns: (optional) a list of the output from running the command
        :rtype: *dict*

        """
        self.set_exposure_mode(6)
        scout = self.serial_cmd_alt('"set ' + str(duration) + '"')
        self.set_exposure_mode(2)
        scout = self.get_camera_parameters()
        et = self.get_exposure_time()

        if to_output == True:
            return scout

    def set_analog_gain(self, tap, gain, to_output=False):
        """Set the analog gain of the camera.

        See section 3.8 of the camera manual for the details.

        :param tap: tap value of 1 or 2
        :type tap: *integer*
        :param gain: gain value between 0 and 4095
        :type gain: *integer*
        :param to_output: ``True`` to return the output list, ``False``
                          to run quietly
        :type to_output: *boolean*
        :Uses: :func:`~HS_Camera.serial_cmd_alt`,
               :func:`~HS_Camera.get_camera_parameters`
        :Updates: ``camera_parameters``
        :Returns: (optional) a list of the output from running the command
        :rtype: *dict*

        """
        scout = self.serial_cmd_alt('"ssg ' + str(tap) + " " + str(duration) + '"')
        self.get_camera_parameters()

        if to_output == True:
            return scout

    def set_digital_gain(self, gain, to_output=False):
        """Set the digital gain of the camera.

        See section 3.8 of the camera manual for the details.

        :param gain: a value from 0 (default) to 2
        :type gain: *integer*
        :param to_output: ``True`` to return the output list, ``False``
                          to run quietly
        :type to_output: *boolean*
        :Uses: :func:`~HS_Camera.serial_cmd_alt`,
               :func:`~HS_Camera.get_camera_parameters`
        :Updates: ``camera_parameters``
        :Returns: (optional) a list of the output from running the command
        :rtype: *dict*

        """
        scout = self.serial_cmd_alt('"gm ' + str(gain) + '"')
        self.get_camera_parameters()

        if to_output == True:
            return scout

    def set_binning_mode(self, hor, ver, to_output=False):
        """Set the binning mode of the camera.

        See section 3.9 of the camera manual for the details.

        Both parameters take a value from 1, 2, 4 and 8.

        :param hor: horizontal binning value (1, 2, 4 or 8)
        :type hor: *integer*
        :param ver: vertical binning value (1, 2, 4 or 8)
        :type ver: *integer*
        :param to_output: ``True`` to return the output list, ``False``
                          to run quietly
        :type to_output: *boolean*
        :Uses: :func:`~HS_Camera.serial_cmd_alt`,
               :func:`~HS_Camera.get_camera_parameters`
        :Updates: ``camera_parameters``
        :Returns: (optional) a list of the output from running the command
        :rtype: *dict*

        """
        scout = self.serial_cmd_alt('"ssg ' + str(hor) + " " + str(ver) + '"')
        self.get_camera_parameters()

        if to_output == True:
            return scout

    def reboot_camera(self, to_output=False):
        """Reboots the camera.

        Rebooting the camera restores its setting to the previously saved one.

        :param to_output: ``True`` to return the output list, ``False``
                          to run quietly
        :type to_output: *boolean*
        :Uses: :func:`~HS_Camera.serial_cmd`,
               :func:`~HS_Camera.get_camera_parameters`
        :Updates: ``camera_parameters``
        :Returns: (optional) a list of the output from running the command
        :rtype: *dict*

        """
        scout = self.serial_cmd("rc")
        self.get_camera_parameters()

        if to_output == True:
            return scout

    def set_pretrigger(self, pt, to_output=False):
        """Set the camera pre-trigger value.

        May be relevant for some frame grabbers.

        :param pt: a value from 0 to 15
        :type pt: *integer*
        :param to_output: ``True`` to return the output list, ``False``
                          to run quietly
        :type to_output: *boolean*
        :Uses: :func:`~HS_Camera.serial_cmd_alt`,
               :func:`~HS_Camera.get_camera_parameters`
        :Updates: ``camera_parameters``
        :Returns: (optional) a list of the output from running the command
        :rtype: *dict*

        """
        scout = self.serial_cmd_alt('"sp ' + str(pt) + '"')
        self.get_camera_parameters()

        if to_output == True:
            return scout

    def set_video_mode(self, mode, to_output=False):
        """Set the video mode of the camera.

        The mode 0 is the normal operating mode.

        Setting the mode to a value other than 0 displays the corresponding test
        pattern image.

        See section 3.12 of the camera manual for the details.

        :param mode: a value from 0 to 11
        :type mode: *integer*
        :param to_output: ``True`` to return the output list, ``False``
                          to run quietly
        :type to_output: *boolean*
        :Uses: :func:`~HS_Camera.serial_cmd_alt`,
               :func:`~HS_Camera.get_camera_parameters`
        :Updates: ``camera_parameters``
        :Returns: (optional) a list of the output from running the command
        :rtype: *dict*

        """
        scout = self.serial_cmd_alt('"svm ' + str(mode) + '"')
        self.get_camera_parameters()

        if to_output == True:
            return scout

    def get_camera_serial_no(self, to_output=True):
        """Get the output that contains the camera serial number.

        :param to_output: ``True`` to return the output list, ``False``
                          to run quietly
        :type to_output: *boolean*
        :Uses: :func:`~HS_Camera.serial_cmd`,
               :func:`~HS_Camera.get_camera_parameters`
        :Updates: ``camera_parameters``
        :Returns: (optional) a list of the output from running the command
        :rtype: *dict*

        """
        scout = self.serial_cmd("gcs")
        self.get_camera_parameters()

        if to_output == True:
            return scout

    def get_camera_model(self, to_output=True):
        """Get the output that contains the camera model number.

        :param to_output: ``True`` to return the output list, ``False``
                          to run quietly
        :type to_output: *boolean*
        :Uses: :func:`~HS_Camera.serial_cmd`,
               :func:`~HS_Camera.get_camera_parameters`
        :Updates: ``camera_parameters``
        :Returns: (optional) a list of the output from running the command
        :rtype: *dict*

        """
        scout = self.serial_cmd("gcm")
        self.get_camera_parameters()

        if to_output == True:
            return scout

    def get_camera_version(self, to_output=True):
        """Get the output that contains the camera version.

        :param to_output: ``True`` to return the output list, ``False``
                          to run quietly
        :type to_output: *boolean*
        :Uses: :func:`~HS_Camera.serial_cmd`,
               :func:`~HS_Camera.get_camera_parameters`
        :Updates: ``camera_parameters``
        :Returns: (optional) a list of the output from running the command
        :rtype: *dict*

        """
        scout = self.serial_cmd("gcv")
        self.get_camera_parameters()

        if to_output == True:
            return scout

    def get_sensor_serial_no(self, to_output=True):
        """Get the output that contains the camera version.

        :param to_output: ``True`` to return the output list, ``False``
                          to run quietly
        :type to_output: *boolean*
        :Uses: :func:`~HS_Camera.serial_cmd`,
               :func:`~HS_Camera.get_camera_parameters`
        :Updates: ``camera_parameters``
        :Returns: (optional) a list of the output from running the command
        :rtype: *dict*

        """
        scout = self.serial_cmd("gss")
        self.get_camera_parameters()

        if to_output == True:
            return scout

    def restore_factory_setting(self, to_output=False):
        """Restore the camera setting to the factory setting.

        :param to_output: ``True`` to return the output list, ``False``
                          to run quietly
        :type to_output: *boolean*
        :Uses: :func:`~HS_Camera.serial_cmd`,
               :func:`~HS_Camera.get_camera_parameters`
        :Updates: ``camera_parameters``
        :Returns: (optional) a list of the output from running the command
        :rtype: *dict*

        """
        scout = self.serial_cmd("rfs")
        self.get_camera_parameters()

        if to_output == True:
            return scout

    def restore_user_setting(self, to_output=False):
        """Restore the camera setting to the last saved user setting.

        :param to_output: ``True`` to return the output list, ``False``
                          to run quietly
        :type to_output: *boolean*
        :Uses: :func:`~HS_Camera.serial_cmd`,
               :func:`~HS_Camera.get_camera_parameters`
        :Updates: ``camera_parameters``
        :Returns: (optional) a list of the output from running the command
        :rtype: *dict*

        """
        scout = self.serial_cmd("rus")
        self.get_camera_parameters()

        if to_output == True:
            return scout

    def write_user_setting(self, to_output=False):
        """Save the current camera setting.

        :param to_output: ``True`` to return the output list, ``False``
                          to run quietly
        :type to_output: *boolean*
        :Uses: :func:`~HS_Camera.serial_cmd`,
               :func:`~HS_Camera.get_camera_parameters`
        :Updates: ``camera_parameters``
        :Returns: (optional) a list of the output from running the command
        :rtype: *dict*

        """
        scout = self.serial_cmd("wus")
        self.get_camera_parameters()

        if to_output == True:
            return scout

    def utc2gps(self, mydt):
        """Convert utc time to gps time.

        The input parameter ``mydt`` is generated by running ``utcnow()`` method
        of the ``datetime`` module. It is an instance of ``datetime`` class.

        This method then converts the time into gps time, taking into account of
        the stepdates.

        The list of the stepdates ``stepdates_t`` should be revised as we get
        more step dates in the future.

        :param mydt: utc datetime
        :type mydt: *datetime.datetime*
        :Returns: the converted gps time
        :rtype: *float*

        """
        # A date for conversion should be later than first_valid_date.
        first_valid_date = (1980, 1, 6)

        # The dates on which the leap seconds were announced.
        stepdates_t = [
            (1981, 7, 1),
            (1982, 7, 1),
            (1983, 7, 1),
            (1985, 7, 1),
            (1988, 1, 1),
            (1990, 1, 1),
            (1991, 1, 1),
            (1992, 7, 1),
            (1993, 7, 1),
            (1994, 7, 1),
            (1996, 7, 1),
            (1997, 7, 1),
            (1999, 1, 1),
            (2006, 1, 1),
            (2009, 1, 1),
            (2012, 7, 1),
            (2015, 7, 1),
            (2017, 1, 1),
        ]

        stepdates = [datetime(*sdt) for sdt in stepdates_t]

        # Determine how many leap seconds should be added
        leapseconds = sum([mydt > sdt for sdt in stepdates])

        # Time difference (in seconds) between the given date and the start date
        td = mydt - datetime(*first_valid_date)

        # return the time difference (with leap seconds added) in units of days
        return (td.total_seconds() + leapseconds) / (24 * 3600)


class InvalidDeviceNo(Exception):
    def __init__(self):
        self.message = "device_no must be 0 or 1."

    def __str__(self):
        return self.message


class CameraInaccessible(Exception):
    def __init__(self):
        self.message = "Unable to connect to the camera."

    def __str__(self):
        return self.message


class AcquisitionFailure(Exception):
    def __init__(self, timeouts, overruns):
        self.timeouts = timeouts
        self.overruns = overruns
        self.message = (
            "Image acquisition failed: "
            + "{} timeouts and ".format(timeouts)
            + "{} overruns occurred.".format(overruns)
        )

    def __str__(self):
        return self.message


class InvalidImageShape(Exception):
    def __init__(self, image_shape, valid_image_shape):
        self.image_shape = image_shape
        self.valid_image_shape = valid_image_shape
        self.message = (
            "Image shape ({0[0]},{0[1]}) is not valid: " + "Expected ({1[0]},{1[1]})."
        ).format(image_shape, valid_image_shape)

    def __str__(self):
        return self.message


class InvalidCommandFormat(Exception):
    def __init__(self):
        self.message = (
            "The camera serial command arguments must be "
            + "a string or a list of strings."
        )

    def __str__(self):
        return self.message


class SerialCommandFailure(Exception):
    def __init__(self, command, cstr):
        self.command = command
        self.command_string = cstr
        if cstr is None:
            self.message = "Failed to execute the serial command."
        else:
            self.message = "Failed to execute the serial command: " + command

    def __str__(self):
        return self.message


class SerialCommandError(Exception):
    def __init__(self, command, cstr, scout):
        self.command = command
        self.command_string = cstr
        self.command_output = scout
        self.message = (
            "Error occurred when executing the serial command: "
            + command
            + "\n\n"
            + "The error message is as follows:\n"
            + scout["stdout"]
        )

    def __str__(self):
        return self.message


# Won Kim 23/08/2018 12:47:41 PM
