from flask import request, g                                                                 
from tools.logging import logger   
from neurosdk.cmn_types import * 
from tools.eeg import UserInfo
import pickle

def handle_request():
    if g.hb == None:
        return ["Data Flowing"]

    g.hb.exec_command(SensorCommand.CommandStopSignal)

    #with open("%s_data.pkl" % UserInfo["Username"], 'wb') as f:  # open pkl file
    #    pickle.dump(UserInfo, f) # serialize the list
    #    f.close()

    #with open("%s_data.pkl" % UserInfo["Username"], 'rb') as f:  #'testing_data_objects.pkl'
    #    one_data = pickle.load(f) # deserialize using load()
    #    print(one_data) # print student names


    return ["Data Stop Flowing"]
