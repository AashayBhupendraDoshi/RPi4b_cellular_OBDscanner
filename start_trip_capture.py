import logging
logging.basicConfig(filename="./output.txt", level=logging.INFO)
from utils.trip_capture import trip_capture

logging.info("Capturing Trips")
a = trip_capture()
logging.info("Monitoring Trips")
a._moniter_trip()
