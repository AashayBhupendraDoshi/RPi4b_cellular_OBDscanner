import pickle, os, sys
import numpy as np
import pandas as pd

# For uploading to s3
import logging
import boto3
from botocore.exceptions import ClientError

unique_key = '000000000002'
cache_addr = "./cache/"
trip_data_addr = "./trip_data/"
metadata_file = 'system_check.pkl'
uploaded_trips_file = 'uploaded_trips.pkl'

logging.basicConfig(level=logging.DEBUG)

def check_cache():
    # Return 1 if cache files exist
    # Else return 0
    file_names = os.listdir(cache_addr)
    if len(file_names)>0:
        logging.info("Cache files found")
        return 1
    else:
        logging.info("No cache files found")
        return 0

def process_cache():
    
    trip = {}
    # Check Cache Folder fro files
    logging.info("Checking cache folder for files")
    file_list = os.listdir(cache_addr)
    
    
    # If no files are present, return 0
    if file_list == []:
    #if not file_list:
        logging.info("No cache files are present")
        return 0
    

    # Check if metadata file is present
    # If yes process it
    metadata = None
    logging.info(f"Processing metadata : {metadata}")
    if metadata_file in file_list:
        with open(cache_addr +  metadata_file, 'rb') as handle:
            metadata = pickle.load(handle)
    else:
        logging.info(f"metadata is {metadata}")
    trip['system_data'] = metadata
    IMU_Headers = metadata['IMU_Headers']
    GPS_Headers = metadata['GPS_Headers']
    # Delete system_check file from list as it has been
    # processed
    file_list.remove(metadata_file)
    logging.info(f"Cache file i.e. {metadata_file} is removed")
    logging.info("Processing ends")



    # Create new list containing only non_blank files
    new_list = []
    for names in file_list:
        # Check if file os not empty to prevent EOF error
        logging.info(f"Checking for non empty os file to prevent EOF error {file_list}")
        if os.path.getsize(cache_addr + names) > 0: 
            buff = int(names.split('.')[0])
            new_list+=[buff]
        else:
            logging.warning("Os file is empty")
            logging.info(f"New list is {new_list}")
    # If no file present has size greate than 0
    # ,i.e., is not null, then return 0
    if new_list == []:
        logging.info("No files are found")
        return 0

    # Arrange non-blank files to read them chronologically
    sorted_list = new_list.sort()
    logging.info(f"Arranging non-empty files to reading them chronologically: {sorted_list}")
    main_list = []
    # Process All Non-Empty files Chronologically
    # and store to a numpy array
    logging.info("Processing all non-empty files chronologically and storing to a numpy array")
    for vals in new_list:

        #f = open(cache_addr + str(vals) + '.pkl', 'rb')
        #a = pickle.load(f)
        #f.close()
        #print(str(vals))
        try:
            a = pickle.load(open(cache_addr + str(vals) + '.pkl', 'rb'))
            buff_list = []
            for keys in a.keys():
                if keys == 'imu':
                    buff_list += a[keys]
                
                elif keys == 'gps':
                    buff_list += a[keys]
                
                elif a[keys] is None:
                    continue
                else:

                    buff_list += [a[keys].to_tuple()[0]]
                    logging.info(f"Files stored successfully \n {buff_list}")
            
            if len(buff_list)==0:
                # In case car in on, but engine is not started
                # ,i.e., turned the key only to connect battery
                # and not turn-on ignition, all readings will be none
                # since sensors are not powered untill ignition is on
                new_list.remove(vals)
                logging.warning("Ignition not turned on. all file readings set to none!")
                #continue
            else:
                main_list += [np.array(buff_list)]
                logging.info(f"Processed main list: {main_list}")
        except:
            logging.exception("Unable to process files and stores into a numpy array")
            continue

    
    #print(np.stack(main_list).shape)
    main_list = np.array(main_list)
    logging.info(f"Processed main list: {main_list}")

    # Find names of all available data entries
    f = open(cache_addr + str(new_list[0]) + '.pkl', 'rb')
    a = pickle.load(f)
    available_keys = []
    for key in a.keys():
        try:
            buff = a[key].to_tuple()
            available_keys += [key]
        except :
            logging.exception(available_keys) 
            continue
    
    
    # Convert Numpy array to pandas dataframe
    logging.info("Converting Numpy array to pandas dataframe")
    buff_df = pd.DataFrame(main_list, columns = IMU_Headers + GPS_Headers + available_keys)
    logging.info(f"Converted data frame : {buff_df}")
    trip['trip_data'] = buff_df
    
    # Save trip-file in trip_data directory
    file_names = os.listdir(trip_data_addr)
    file_names.remove(uploaded_trips_file)
    if file_names == []:
        logging.info(f"file_names array is empty : {file_names}")
        with open( trip_data_addr + '1.pkl', 'wb' ) as f:
            #pickle.dump(buff_point, f, protocol=pickle.HIGHEST_PROTOCOL)
            pickle.dump(trip, f)
    else:
        new_list = []
        for names in file_names:
            buff = int(names.split('.')[0])
            new_list+=[buff]
        # If no file present has size greate than 0
        # ,i.e., is not null, then return 0
        #if new_list == []:
        #    return 0

        # Arrange non-blank files to read them chronologically
        new_list.sort()
        new_name = new_list[-1] + 1
        with open( trip_data_addr + str(new_name) + '.pkl', 'wb' ) as f:
            #pickle.dump(buff_point, f, protocol=pickle.HIGHEST_PROTOCOL)
            pickle.dump(trip, f)
    
    
    # Clean Cache
    file_names = os.listdir(cache_addr)
    for vals in file_names:
        os.remove(cache_addr + vals)
        logging.info("Cache cleared")

    return 0



def upload_file_s3(file_name,object_name):
    """Upload a file to an S3 bucket
    :param file_name: File to upload (including complete address)
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """
    print("file", file_name, object_name)
    REGION_NAME = 'ap-south-1'
    bucket = 'motodb-carminer-data'
    # bucket_address is the location in the s3 bucket where the data will be loaded
    bucket_address = '/temp/'
    # Upload the file
    s3_client = boto3.client('s3',
                            aws_access_key_id='AKIAYUK4V2N3EH6VHTSW', 
                            aws_secret_access_key='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', 
                            region_name=REGION_NAME
                )
    try:
        logging.info("File uploading starts")
        response = s3_client.upload_file(file_name, bucket, bucket_address + object_name)
        logging.info(f"File uploaded successfully {resopnse}")
    except ClientError as e:
        logging.error(f"File uploading failed. {e}")
        return False
    return True


def upload_trip_data():
    logging.info("Trip data uploading starts")
    #uploaded_files = pickle.load(open(trip_data_addr + 'uploaded_trips.pkl'),encoding="utf-8")
    with open(trip_data_addr + uploaded_trips_file, 'rb') as f:
        uploaded_files = pickle.load(f)
        
    file_list = os.listdir(trip_data_addr)
    file_list.remove('uploaded_trips.pkl')
    for vals in file_list:
        if vals not in uploaded_files:
            # File name in s3 should have unique_key appended to it
            buff = upload_file_s3(trip_data_addr + vals, unique_key +'_'+ vals)
            logging.info(f"Files updated with unique key : {buff}")
            if buff:
            # Update uploaded files list only if file is uploaded
            # successfully
                uploaded_files += [vals]
                
    # Store updated uploaded_trips file
    with open(trip_data_addr + 'uploaded_trips.pkl', 'wb') as f:
        pickle.dump(uploaded_files,f)
        logging.info(f"Trip data stored on file! {file_list}")
    
    return 0            
           
# process_cache()
check_cache()
upload_trip_data()