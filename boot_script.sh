cd /home/pi/obd_data_module/
/usr/bin/python3 -c "from utils.general_utils import *; process_cache()"
sh ./boot_upload.sh & sh ./boot_obd.sh

# In rc.local type "sh ./boot_script.sh > last_trip_log.txt"
# Ensure the obd logging is turned off or to lowest level
