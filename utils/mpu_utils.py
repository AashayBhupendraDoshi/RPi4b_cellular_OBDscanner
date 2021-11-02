import time
from mpu9250_jmdev.registers import *
from mpu9250_jmdev.mpu_9250 import MPU9250
import logging
logging.basicConfig(level=logging.INFO)

class mpu():
    
    def __init__(self):
        self._init_mpu()
        
    def _init_mpu(self, calibrate=0):
        self.mpu = MPU9250(
            address_ak=AK8963_ADDRESS, 
            address_mpu_master=MPU9050_ADDRESS_68, # In 0x68 Address
            address_mpu_slave=None, 
            bus=1,
            gfs=GFS_1000, 
            afs=AFS_8G, 
            mfs=AK8963_BIT_16, 
            mode=AK8963_MODE_C100HZ)

        if calibrate==1:
        # Calibrate sensors
        # The calibration function resets the sensors, so you need to reconfigure them
            logging.info("Calibrating sensors")
            logging.info("The calibration function resets the sensors")
            logging.info("Sensors getting reconfigured")
            self.mpu.calibrate() 
        
        # Apply the settings to the registers.
        logging.info("Applying the settings to the registers.")
        self.mpu.configure() 
        return 0



    def get_reading_metadata(self):
    # return labels with data description for each array position
        logging.info("Getting values for metadata and returning data description for each array position")
        return self.mpu.getAllDataLabels()

    def get_reading(self):
    # returns a array with data from all sensors
        logging.info("Getting array with data from all sensors")
        return self.mpu.getAllData()
