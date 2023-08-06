"""
This file is *not* licensed under the Unviersity of Adelaide license as laid out in
the accompanying LICENSE file.

HS_Export.py exports data to file

4-Oct-2018: updated the HS_Export class to export to HDF5 instead of pickle. The file content is the same but the export format is now HDF5
          : Also set the avImage to be compressed. This looks to reduce the file size by slightly more than 50%
          : 'datetime' does not transfer easily to HDF5 so this is converted to ISOFORMAT
"""
import os
import subprocess as sp
from socket import gethostname
from numpy import *
from datetime import datetime, timedelta
import pickle
from time import strftime, gmtime
import h5py

from HWS.HS_CamConfig import *
from HWS.HS_Image import *


class HS_Export:
    # A class to export data to file.

    def __init__(self, IFO="H1", optic="ETMY_HWS", frameDir="/home/controls/temp"):
        self.avGradients = None
        self.avGpstime = 0
        self.avImage = None
        self.numberOfAvg = 0
        self.lastSaveTime = datetime.now()
        self.averageDuration = 20
        self.IFO = IFO
        self.optic = optic
        self.frameDir = frameDir
        self.timeDir = None
        self.filename = None
        self.hostname = gethostname()
        self.origin_x = None
        self.origin_y = None
        self.mask_radius = None
        self.mask_center_x = None
        self.mask_center_y = None

    def update_averages(self, gradients, image, gpstime):
        # update the averages to be saved
        if self.numberOfAvg == 0:
            self.avGradients = gradients
            self.avGpstime = gpstime
            self.avImage = image

            self.numberOfAvg = 1
        else:
            self.avGradients = self.avGradients + gradients
            self.avGpstime = self.avGpstime + gpstime
            self.avImage = self.avImage + image

            self.numberOfAvg = self.numberOfAvg + 1

    def export_if_necessary(self):
        # export the data to file if enough time has elapsed
        tdelta = datetime.now() - self.lastSaveTime

        if self.numberOfAvg > 0 and (tdelta.total_seconds() > self.averageDuration):
            # get the averages
            self.avGradients = self.avGradients / self.numberOfAvg
            self.avGpstime = self.avGpstime / self.numberOfAvg
            self.avImage = self.avImage / self.numberOfAvg
            self.avImage = self.avImage.astype("uint16")

            # udpate the save time so it is stored in the file
            self.lastSaveTime = datetime.now()

            # create the time directory string and check it exists
            self.timeDir = str(int(floor(self.avGpstime / 1e5) * 1e5)) + "/"
            dirSub = (
                self.frameDir + "/" + self.IFO + "/" + self.optic + "/" + self.timeDir
            )

            if os.path.exists(dirSub) == False:
                # create the sub directory
                os.makedirs(dirSub)

            # create the filename and export the data
            self.filename = (
                dirSub
                + str(int(round(self.avGpstime)))
                + "_"
                + self.IFO
                + "_"
                + self.optic
                + "_HS_Export.hdf5"
            )
            # pickle.dump(self,open(self.filename,"wb"),2)
            print(self.filename)

            # export the data using HDF5
            f = h5py.File(self.filename, "w")
            f["avGradients"] = self.avGradients
            f["avGradients"].attrs["numberOfAvg"] = self.numberOfAvg
            f["avGradients"].attrs["lastSaveTime"] = self.lastSaveTime.isoformat()
            f["avGradients"].attrs["avGpstime"] = self.avGpstime
            f["avGradients"].attrs["averageDuration"] = self.averageDuration
            f["avGradients"].attrs["IFO"] = self.IFO
            f["avGradients"].attrs["optic"] = self.optic
            f["avGradients"].attrs["frameDir"] = self.frameDir
            f["avGradients"].attrs["timeDir"] = self.timeDir
            f["avGradients"].attrs["filename"] = self.filename
            f["avGradients"].attrs["hostname"] = self.hostname
            f["avGradients"].attrs["mask_radius"] = self.mask_radius
            f["avGradients"].attrs["mask_center_x"] = self.mask_center_x
            f["avGradients"].attrs["mask_center_y"] = self.mask_center_y
            f["avGradients"].attrs["origin_x"] = self.origin_x
            f["avGradients"].attrs["origin_y"] = self.origin_y

            dset = f.create_dataset("avImage", data=self.avImage, compression="gzip")
            f.close()

            print(
                "Saved file - "
                + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
                + " UTC"
            )

            # reset the averages
            self.numberOfAvg = 0
