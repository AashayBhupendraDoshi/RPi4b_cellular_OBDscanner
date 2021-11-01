from utils.trip_capture import trip_capture
import logging
logging.basicConfig(level=logging.INFO)

logging.info("Capturing Trips")
a = trip_capture()
logging.info("Monitering Trips")
a._moniter_trip()
