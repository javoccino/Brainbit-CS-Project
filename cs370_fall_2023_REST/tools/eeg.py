from neurosdk.scanner import Scanner
from neurosdk.sensor import Sensor
from neurosdk.brainbit_sensor import BrainBitSensor
from neurosdk.cmn_types import *
import re

from tools.logging import logger   

import pickle
#doing all this a the "module level" in "Demo" server mode it will work fine :)

UserInfo = {
  "Username": "",
  "Password": "",
  "clip_name" : "movie.mp4",
  "movie_play_data": [],
}

full_data = []

def on_sensor_state_changed(sensor, state):
    logger.debug('Sensor {0} is {1}'.format(sensor.Name, state))

def on_brain_bit_signal_data_received(sensor, data):
    
    logger.debug(data)
    UserInfo["movie_play_data"].append(data) #add to the list of the UserInfo
   
def returnpswrd(username):
    with open("%s_data.pkl" % username, 'rb') as f:  #'testing_data_objects.pkl'
        userDict = pickle.load(f) # deserialize using load()
        password = userDict["Password"]
    return password

def checkUser(username):
    try:
        with open("%s_data.pkl" % username, 'rb') as f:
            userDict = pickle.load(f)
            if username in userDict['Username']:
                check= True; 
    except FileNotFoundError:
        # Handle the case where the file is not found
        check = False
    return check

def store_signup(username, password, rpassword):
    result = f"Signup info: {username}, {password}, {rpassword}"
    if(password == rpassword):
        UserInfo["Username"] = username
        UserInfo["Password"] = password
        print(UserInfo)

        with open("%s_data.pkl" % UserInfo["Username"], 'wb') as f:  # open pkl file
            pickle.dump(UserInfo, f) # serialize the list
            f.close()

        print("\n-------------Printing plk-----------------------\n") #to see if the pkl works

        with open("%s_data.pkl" % UserInfo["Username"], 'rb') as f:  #'testing_data_objects.pkl'
            one_data = pickle.load(f) # deserialize using load()
            print(one_data) # print student names

        #response = requests.get(url) #stores the Response information from the get request into response
        #print(response)
        #if response.status_code == 200: #.status_code grabs response code, 200 means success
        #    data = response.json() #storing json content into data as a dictionary
        #    print(data)
        #else:
        #    print("fail")


        return True
    else:
        return False


logger.debug("Create Headband Scanner")
gl_scanner = Scanner([SensorFamily.SensorLEBrainBit])
gl_sensor = None
logger.debug("Sensor Found Callback")
def sensorFound(scanner, sensors):
    global gl_scanner
    global gl_sensor
    for i in range(len(sensors)):
        logger.debug('Sensor %s' % sensors[i])
        logger.debug('Connecting to sensor')

        gl_sensor = gl_scanner.create_sensor(sensors[i])
        gl_sensor.sensorStateChanged = on_sensor_state_changed
        gl_sensor.connect()
        gl_sensor.signalDataReceived = on_brain_bit_signal_data_received
        gl_scanner.stop()
        del gl_scanner

gl_scanner.sensorsChanged = sensorFound

logger.debug("Start scan")
gl_scanner.start()


def get_head_band_sensor_object():
    return gl_sensor

