import os, sys, time, datetime
import pickle
from utils.general_utils import *
from utils.obd_utils import myOBD
from utils.mpu_utils import mpu
#from utils.gps_utils import AT_GPS

# Since Inboard Computer is powered by the car-charger
# It will start whenever the car is turned on and will shutdown
# whenever the car is turned off.
# Since we do not know the duration of the trips and don't have a
# battery to run the in-board computer, we are calling and saving
# each individual data-point in the 'cache' folder. When the car
# is turned off, the data-points will remain in the cache.
# Once the car is turned on again, these files will be processed
# into a single trip file and saved in the 'trip_data' folder

class trip_capture():
    def __init__(self, capture_frequency=1):
        # Capture Frequency is the number of points per seconds
        # does the user want
        # Process and clear cache
        self.cache_addr = "./cache/"
        #process_cache()
        # Init OBD
        self.obd = myOBD()
        # Init mpu
        self.mpu = mpu()
        self.mpu_metadata = self.mpu.get_reading_metadata()
        # Init GPS
        self.gps = AT_GPS()
        self.gps_metadata = self.gps.metadata
        self.sleep_time = 1/capture_frequency
        self._system_check()
        #self._moniter_trip()

    def _system_check(self):
        # Get Initial system checks before getting trip data
        # These include DTC's during the start of the trip
        # These cannot  be done in the end since we do not know
        # when the trip will end

        #system_data = {}
        system_data = self.obd._get_system_info()
        if system_data['ELM_VERSION'] is not None:
            system_data['ELM_VERSION'] = system_data['ELM_VERSION'].value
        if system_data['ELM_VOLTAGE'] is not None:
            system_data['ELM_VOLTAGE'] = system_data['ELM_VOLTAGE'].value.to_tuple()[0]
        system_data['STATUS'] = None
        system_data['Start_Time'] = datetime.datetime.now()
        #system_data['System_Data'] = self.obd._get_system_info()
        system_data['Trouble_Codes'] = self.obd._get_dtc()
        system_data['Freeze_Frame'] = self.obd._get_freeze_frame()
        system_data['IMU_Headers'] = self.mpu_metadata
        system_data['GPS_Headers'] = self.gps_metadata

        with open( self.cache_addr + 'system_check.pkl', 'wb' ) as f:
            pickle.dump(system_data, f, protocol=pickle.HIGHEST_PROTOCOL)

        return 0

    def _moniter_trip(self):
	# Every data-point is saved as a dictionary in a pickle file
	# which is named in a serial order
        counter = 0
        while(True):
            buff_point = self.obd._get_current_data()

            buff_mpu = self.mpu.get_reading()
            buff_point['imu'] = buff_mpu
            #for i in range(len(buff_mpu)):
            #    buff_point[self.mpu_metadata[i]] = buff_mpu[i]
            buff_gps = self.gps._get_gps_nmea()
            buff_point['gps'] = buff_gps
            with open( self.cache_addr + str(counter) + '.pkl', 'wb' ) as f:
                pickle.dump(buff_point, f, protocol=pickle.HIGHEST_PROTOCOL)

            time.sleep(self.sleep_time)
            counter +=1

        return 0

#a = trip_capture()
#a._moniter_trip()
