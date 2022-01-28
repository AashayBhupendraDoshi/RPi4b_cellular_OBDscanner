## Introduction
A Rpi based system to collect data from the OBDii port of a car and transmit it to AWS S3 bucket
Collects OBDii data from the car, motion sensor from onboard motion-sensors, GPS data and transmits
it to the AWS cloud. The components used are:
- Raspberry Pi 4b 4GB
- MPU9250 9-axis IMU
- Quectel EC25 CAT4 LTE HAT
- Any USB based ELM327 OBD scanner

Note:
- Though this system was build on top of raspberry pi, it shoudl run on any linux based system, only the specific console terminals (used for OBD and GPS) and IMU support will need to be addressed.
- The specific Quectel will be based on the region you are in (EC25-E since the device was developed in India). Please refer [this](https://www.quectel.com/wp-content/uploads/pdfupload/Quectel_EC25_Series_LTE_Standard_Specification_V2.1.pdf) document while selecting your module. 

## Pre-requisites:
1. Python3 :

* [Download Python3](https://www.python.org/downloads/)

* [Installation Steps](https://realpython.com/installing-python/)

* Check installation is done on local with checking python3 version

    ```
    python3 --version
    ```

* You will also need to install libqmi-utils and udhcpc packages on the system

    ```
    sudo apt-get update
    sudo apt-get install libqmi-utils udhcpc
    ```


## Installation:

* Clone the project:

    ```
    git clone https://github.com/AashayBhupendraDoshi/motoDB_hardware.git

    cd motoDB_hardware/
    ```

* For installing all packages in `requirements.txt` file, run following command in your project directory:

    ```
    pip3 install -r requirements.txt
    ```

## Configuration:
Befire starting there are a few steps you will have to follow:
- Add your AWS public and secret kes in the /utils/general_utils.py file
- Setup the tty consoles (in utils/obd_utils.py and in utils/gps_utils.py) according to your setup. In the current setup the OBD is connected to the bottom left USB port and 4G module to the top left port of the Rpi4B
```
```
## Run:

* To run the bash script:

    ```
    bash boot_script.sh
    ```

## Logs:

* You can see logs in the following file:
    ```
    test_output.txt
    ```
