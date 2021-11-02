import logging, os, pathlib
file = pathlib.Path("./Logs/")
if not file.exists():
    os.mkdir("./Logs")
logging.basicConfig(filename="./Logs/output.txt", filemode="a", format='%(asctime)s %(message)s', level=logging.INFO)
from utils.trip_capture import trip_capture

logging.info("-------------New Logs------------")
logging.info("Capturing Trips")
a = trip_capture()
logging.info("Monitoring Trips")
a._moniter_trip()
