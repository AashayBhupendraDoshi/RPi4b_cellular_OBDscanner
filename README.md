# Introduction
A Rpi based system to collect data from the OBDii port of a car and transmit it to AWS S3 bucket
Collects OBDii data from the car, motion sensor from onboard motion-sensors, GPS data and transmits
it to the AWS cloud. The components used wre:
-Raspberry Pi 4b 4GB
-MPU9250 9-axis IMU
-Quectel EC25 CAT4 LTE HAT
-Any USB based ELM327 OBD scanner

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
