import obd
obd.logger.setLevel(obd.logging.DEBUG)

class myOBD():
    def __init__(self):
        self._connect_obd()
        self._init_pids()
        
    
    def _connect_obd(self):
        self.connection = obd.OBD()
        print('Protocol USED: ', self.connection.protocol_name())

    def _init_pids(self):
        # Initialize PIDs
        #
        #
	    # Set Mode 0 PIDs
	    # These are vehicle status PIDs such elm version
	    # Fuel_Status, Freeze_DTC, etc which should be
	    # checked at the start of the trip
        self.mode0 = {}
        self.mode0['ELM_VERSION'] = obd.commands.ELM_VERSION
        self.mode0['ELM_VOLTAGE'] = obd.commands.ELM_VOLTAGE
        self.mode0['STATUS'] = obd.commands.STATUS
        self.mode0['FREEZE_DTC'] = obd.commands.FREEZE_DTC
        self.mode0['FUEL_STATUS'] = obd.commands.FUEL_STATUS

        # Initialize Mode 1 PIDs
	    # These are parameters to be actively monitered
        self.mode1 = {}
        self.mode1['ENGINE_LOAD'] = obd.commands.ENGINE_LOAD
        self.mode1['COOLANT_TEMP'] = obd.commands.COOLANT_TEMP
        self.mode1['FUEL_PRESSURE'] = obd.commands.FUEL_PRESSURE
        self.mode1['INTAKE_PRESSURE'] = obd.commands.INTAKE_PRESSURE
        self.mode1['RPM'] = obd.commands.RPM
        self.mode1['SPEED'] = obd.commands.SPEED
        self.mode1['TIMING_ADVANCE'] = obd.commands.TIMING_ADVANCE
        self.mode1['INTAKE_TEMP'] = obd.commands.INTAKE_TEMP
        self.mode1['MAF'] = obd.commands.MAF
        self.mode1['THROTTLE_POS'] = obd.commands.THROTTLE_POS
        self.mode1['RUN_TIME'] = obd.commands.RUN_TIME
        self.mode1['FUEL_LEVEL'] = obd.commands.FUEL_LEVEL
        self.mode1['BAROMETRIC_PRESSURE'] = obd.commands.BAROMETRIC_PRESSURE
        self.mode1['AMBIANT_AIR_TEMP'] = obd.commands.AMBIANT_AIR_TEMP
        self.mode1['FUEL_TYPE'] = obd.commands.FUEL_TYPE
        self.mode1['ETHANOL_PERCENT'] = obd.commands.ETHANOL_PERCENT
        self.mode1['OIL_TEMP'] = obd.commands.OIL_TEMP
        self.mode1['FUEL_RATE'] = obd.commands.FUEL_RATE
        
        # Initialize Mode 2 PIDs (Freeze Frame Data)
	# Only if a DTC has been detected, i.e., FREEZE_DTC is not None
        self.mode2 = {}
        self.mode2['DTC_ENGINE_LOAD'] = obd.commands.DTC_ENGINE_LOAD
        self.mode2['DTC_COOLANT_TEMP'] = obd.commands.DTC_COOLANT_TEMP
        self.mode2['DTC_FUEL_PRESSURE'] = obd.commands.DTC_FUEL_PRESSURE
        self.mode2['DTC_INTAKE_PRESSURE'] = obd.commands.DTC_INTAKE_PRESSURE
        self.mode2['DTC_RPM'] = obd.commands.DTC_RPM
        self.mode2['DTC_SPEED'] = obd.commands.DTC_SPEED
        self.mode2['DTC_TIMING_ADVANCE'] = obd.commands.DTC_TIMING_ADVANCE
        self.mode2['DTC_INTAKE_TEMP'] = obd.commands.DTC_INTAKE_TEMP
        self.mode2['DTC_MAF'] = obd.commands.DTC_MAF
        self.mode2['DTC_THROTTLE_POS'] = obd.commands.DTC_THROTTLE_POS
        self.mode2['DTC_RUN_TIME'] = obd.commands.DTC_RUN_TIME
        self.mode2['DTC_FUEL_LEVEL'] = obd.commands.DTC_FUEL_LEVEL
        self.mode2['DTC_BAROMETRIC_PRESSURE'] = obd.commands.DTC_BAROMETRIC_PRESSURE
        self.mode2['DTC_AMBIANT_AIR_TEMP'] = obd.commands.DTC_AMBIANT_AIR_TEMP
        self.mode2['DTC_FUEL_TYPE'] = obd.commands.DTC_FUEL_TYPE
        self.mode2['DTC_ETHANOL_PERCENT'] = obd.commands.DTC_ETHANOL_PERCENT
        self.mode2['DTC_OIL_TEMP'] = obd.commands.DTC_OIL_TEMP
        self.mode2['DTC_FUEL_RATE'] = obd.commands.DTC_FUEL_RATE

	# Initialize Model 3 PIDs (Diagnostic Trouble Codes)
        self.GET_DTC = obd.commands.GET_DTC

        pass
    

    def _get_current_data(self):
        current_screen = {}
        for keys in self.mode1.keys():
            r = self.connection.query(self.mode1[keys])
            current_screen[keys] = r.value
        
        return current_screen

    def _get_freeze_frame(self):
        freeze_screen = {}
        for keys in self.mode2.keys():
            r = self.connection.query(self.mode2[keys])
            freeze_screen[keys] = r.value
        
        return freeze_screen

    def _get_dtc(self):
        
        r = self.connection.query(self.GET_DTC)
        return r.value
        

    def _get_system_info(self):
        info = {}
        for keys in  self.mode0.keys():
            if keys in ["ELM_VERSION", "ELM_VOLTAGE"]:
                r = self.connection.query(self.mode0[keys])
                info[keys] = r
                continue
            r = self.connection.query(self.mode0[keys])
            info[keys] = r.value

        return info


#    def _get_data(self, mode, PID):
#        if mode is [1, 2]:
#            c = obd.commands[mode][PID]
#            r = self.connection.query(c)
#            print(r.value, r.time, r.messages)
#        else:
#            c = obd.commands[mode]
#            r = self.connection.query(c)
#            print(r)

#connection = obd.OBD()
#c = obd.commands[1][12]
#r = connection.query(c)
#print(r.value, r.time, r.messages)
#print(obd.commands.__dict__)

#if __name__ == '__main__':
#    car = myOBD()
#    buff = car._get_current_data()
#    #print(buff)
#    #car._get_gata(2,1)
#    for keys in buff.keys():
#        print(keys,': ', buff[keys])
    
#    print('DTC:   ', car.GET_DTC)
