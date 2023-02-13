import serial
import os, time
import RPi.GPIO as GPIO
import pynmea2
import logging
logging.basicConfig(level=logging.DEBUG)

GPIO.setmode(GPIO.BOARD)

class AT_GPS():

    def __init__(self):
        # Set up port for communication
        logging.info("Setting up port for communication")
        self.port = serial.Serial("/dev/ttyUSB2", baudrate=115200, timeout=1)
        self._init_gps()
        self.metadata = ['timestamp', 'lat', 'lat_dir', 'lon', 'lon_dir', 'gps_qual', 'num_sats', 'horizontal_dil', 'altitude', 'altitude_units', 'geo_sep', 'geo_sep_units', 'age_gps_data', 'ref_station_id']
        #self.metadata = list(self._get_gps_nmea().name_to_idx.keys())


    def str2b(self, strr):
        # Using Encode
        #return strr.encode('utf-8')
        logging.info("encoding strr to utf-8")
        return bytes(strr, 'utf-8')

    def serial_txrx(self, msg):
        #bytes(test_string, 'utf-8')
        #self.port.write(self.str2b(msg + '\r\n'))
        self.port.write(self.str2b(msg + '\r'))
        rcv = self.port.read(128)
        # Decode binary RX to ascii
        logging.info("Decode binary RX to ascii")
        rcv = rcv.decode('utf-8')
        logging.info(f"Decoded rcv is {rcv}")
        #print(rcv)
        time.sleep(1)
        #rcv = self.port.read(64)
        #print(rcv)
        return rcv

    def _gps_cold_start(self):
        logging.info("Getting gps cold start")
        rx = self.serial_txrx('AT+QGPSDEL=0')
        logging.info(f"Gps cold start is {rx}")

    def _get_firmware_info(self):
        logging.info("Getting firmware information")
        rx = self.serial_txrx('ATI')
        logging.info(f"Firmware info : {rx}")
        return rx.splitlines()

    def _check_loc(self):
        rx = self.serial_txrx('AT+QGPSLOC?')

        return rx.splitlines()

    def _init_gps(self):
        # Turn on GPS
        logging.info("GPS turned on")
        rx = self.serial_txrx('AT+QGPS=1')
        time.sleep(30)
        # Set <nmeasrc> to 1 to enable acquisition of NMEA sentances via AT+QGPSGNMEA.
        logging.info("Seting <nmeasrc> to 1 to enable acquisition of NMEA sentances via AT+QGPSGNMEA.")
        rx = self.serial_txrx('AT+QGPSCFG="nmeasrc",1')
        logging.info(f"In _init_gps : {rx}")

    def _get_gps_nmea(self):
        rx_default = "$GPGGA,,,,,,0,,,,,,,,*66"
        # Obtain GGA sentence in nmea format
        logging.info("Obtaining GGA sentence in nmea format")
        rx = self.serial_txrx('AT+QGPSGNMEA="GGA"')
        try:
            # Decode nmea sentance
            #print(rx)
            #buff = str(rx).split('\r\n')
            # Decode binary string to ascii
            #rx = rx.decode('utf-8')
            # Get nmea parse
            rx = rx.splitlines()
            rx = rx[2]
            rx = rx.split('+QGPSGNMEA: ')[-1]
            #rx = rx.split('+QGPSGNMEA: ')
            rx = pynmea2.parse(rx)
        except:
            rx = pynmea2.parse(rx_default)

        #rx2 = {k: getattr(rx, k) for k in rx.name_to_idx}
        rx = rx.__dict__['data']

        return rx
