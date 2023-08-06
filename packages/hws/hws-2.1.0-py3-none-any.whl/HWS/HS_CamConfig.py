"""
Copyright (C) University of Adelaide, Australia - All Rights Reserved
This source code is protected under proprietary reference only license.
Please refer to the accompanying LICENSE file for further information.
"""

from HWS.HS_Camera import *
import os


class HS_CamConfig:
    """A class to hold the camera configuration data.

    ``HS_CamConfig`` is a class that retrieves and stores the camera configuration
    of Dalsa Pantera 1M60 camera.

    The class needs :class:`HS_Camera <HWS.HS_Camera.HS_Camera>` to retrieve the
    camera configuration, and will not work by itself. (May change in a future)

    **Instantiation**

    Although the class can be instantiated separately, a user will not have to
    do so in most cases. When :class:`HS_Camera <HWS.HS_Camera.HS_Camera>` is
    instantiated, ``HS_CamConfig`` is also instantiated and assigned as one of
    its instance variables.

    **Instance Variables**

    The instance variables consist of those which are retrieved when the serial
    command 'gcp' is executed. The sensor and digitizer temperature values are
    not retrieved by 'gcp' but another command, and is assigned to an instance
    variable of :class:`HS_Camera <HWS.HS_Camera.HS_Camera>`.

    For descriptions of each camera parameters, consult the camera manual.

    """

    def __init__(self):
        # self.fg_directory = '/opt/EDTpdv/'
        self.fg_directory = os.getenv("FG_DIRECTORY")
        self.model_number = None
        self.camera_serial_number = None
        self.sensor_serial_number = None
        self.tap_1_gain = None
        self.tap_2_gain = None
        self.firmware_design_rev = None
        self.dsp_design_rev = None
        self.pretrigger = None
        self.video_mode = None
        self.data_mode = None
        self.binning_mode = None
        self.gain_mode = None
        self.output_configuration = None
        self.exposure_control = None
        self.exposure_mode = None
        self.sync_frequency = None
        self.exposure_time = None

    def get_parameters(self, cam):
        """Get camera configuration parameters.

        :param cam: an instance of :class:`HS_Camera <HWS.HS_Camera.HS_Camera>`
        :Uses: :func:`HS_Camera.serial_cmd() <HWS.HS_Camera.HS_Camera.serial_cmd>`,
               :func:`~HS_CamConfig.parse_ccd_output`

        """
        gcpout = cam.serial_cmd("gcp")
        # Dan+Cao : Unsure why this has been commented out
        # if 'OK>' not in gcpout['stdout']:
        #     raise \
        #       Exception('Failed to retrieve the parameters from the camera.')
        self.parse_ccd_output(gcpout["stdout"])

    def parse_ccd_output(self, gcpstr):
        """Parse the output from 'gcp' command, and updates the camera parameters.

        :param gcpstr: an output from 'gcp' command
        :type gcpstr: *string*
        :Updates: all instance variables of ``HS_CamConfig``

        """
        pstr = []

        for fs in gcpstr.split("\n"):
            fsl = fs.split(":")
            if (size(fsl) == 2) and (len(fsl[1]) > 0):
                pstr = pstr + [fsl[1].strip()]

        self.model_number = pstr[0]
        self.camera_serial_number = pstr[1]
        self.sensor_serial_number = pstr[2]
        self.tap_1_gain = pstr[3]
        self.tap_2_gain = pstr[4]
        self.firmware_design_rev = pstr[5]
        self.dsp_design_rev = pstr[6]
        self.pretrigger = pstr[7]
        self.video_mode = pstr[8]
        self.data_mode = pstr[9]
        self.binning_mode = pstr[10]
        self.gain_mode = pstr[11]
        self.output_configuration = pstr[12]
        self.exposure_control = pstr[13]
        self.exposure_mode = pstr[14]
        self.sync_frequency = pstr[15]
        self.exposure_time = pstr[16]
