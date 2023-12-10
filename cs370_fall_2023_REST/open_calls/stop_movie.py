from flask import request, g                                                                 
from tools.logging import logger   
from neurosdk.cmn_types import * 
from tools.eeg import UserInfo
import pickle

def handle_request():
    if g.hb == None:
        return ["Data Flowing"]

    g.hb.exec_command(SensorCommand.CommandStopSignal)

    print("\n-------------Printing plk-----------------------\n") #to see if the pkl works

    with open("%s_data.pkl" % UserInfo["Username"], 'wb') as f:  #'testing_data_objects.pkl'
        pickle.dump(UserInfo, f) # serialize the list
        f.close()
        
    
    print("\n-------------finish plk-----------------------\n")

    return ["Data Stop Flowing"]

  