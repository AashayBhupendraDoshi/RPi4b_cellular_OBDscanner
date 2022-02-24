import logging, os, pathlib
file = pathlib.Path("./Logs/")
if not file.exists():
    os.mkdir("./Logs")
logging.basicConfig(filename="./Logs/output.txt", filemode="a", format="%(asctime)s - %(filename)s - %(funcName)s - %(lineno)d - %(levelname)s : %(message)s", datefmt='%d/%m/%Y %I:%M:%S %p', level=logging.INFO)
from utils.trip_capture import trip_capture

logging.info("Capturing Trips")
a = trip_capture()
logging.info("Monitoring Trips")
a._moniter_trip()
