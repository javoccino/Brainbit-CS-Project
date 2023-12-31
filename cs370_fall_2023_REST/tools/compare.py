import pickle
import re
import os
import math
import itertools 
from tools.eeg import UserInfo
from tools.logging import logger

username_average = []
#to get the current working directory
directory = os.getcwd()

print(directory)

# list to store files
res = []
# Iterate directory
for file in os.listdir(directory):
    # check only text files
    if file.endswith('.pkl'):
        res.append(file)
print("RES:")
print(res)
print(directory + "\\" + "%s_data.pkl" % UserInfo["Username"])

print("\n--------------COMPARING DATA---------------------\n")

def parse(str):
        #print("PARSING:")
        PackNum = re.findall(r"(PackNum=\d+)", str)
        Marker = re.findall(r"(Marker=\d+)", str)
        O1 = re.findall(r"(O1=-?\d+\.?\d+)", str)
        O2 = re.findall(r"(O2=-?\d+\.?\d+)", str)
        T3 = re.findall(r"(T3=-?\d+\.?\d+)", str)
        T4 = re.findall(r"(T4=-?\d+\.?\d+)", str)
        #print(PackNum)  
        #print(Marker) 
        #print(O1) 
        #print(O2) 
        #print(T3) 
        #print(T4)  
        #print("NEXT NUMS")

        O1 = re.sub("O1=", "", O1[0])
        O2 = re.sub("O2=", "", O2[0])
        T3 = re.sub("T3=", "", T3[0])
        T4 = re.sub("T4=", "", T4[0])

        list_variables = [float(O1), float(O2), float(T3), float(T4)] #[O1, O2, T3, T4]
        #print("CLEANED:\n")
        #print(O1)
        #print(O2)
        #print(T3)
        #print(T4)
        
        return list_variables

# Python program to get average of a list 
def Average(lst): 
    return sum(lst) / len(lst) 

#note in the for loop below two thing at time
def compare_data(username, surveyData):
    #save all parse data save as float numbers for login user
    list_one = []

    #plan to use one list to have another user data to then compare avarege the distance 
    #formula meaning after get the avg of current user to potential parthner next partner will use this list to compare
    list_two = []

    #collect all the distance answers btw LoginUser and other users to then avg out all ans in the list
    list_distance_avg_ans_per_user = []

    #holds username and age value from surveyData
    usernames_and_ages = []

    #stores username and age values from survey data into usernames_and_ages
    for row in surveyData[1:]: #skips first row incase of header
        if len(row) > 3: #avoids index error, makes sure data is there
                usernames_and_ages.append((row[2],row[3])) #know age is always in index 2 of column and username is in index 3
                #print(usernames_and_ages)

    #make the actual login user open pickle part 
    with open(directory + "\\" + "%s_data.pkl" % username, 'rb') as f:       
        new_one_data = pickle.load(f) # deserialize using load()
        one_data_set = new_one_data["movie_play_data"]
        for x in one_data_set:
                first = ""
                for i in range(len(x)):
                      if i % 2 == 0:
                            first = x[i]
                            list_one.append(parse(str(first)))

        print("------------------MAIN - -----------------------" )

        print("len: " + str(len(list_one)))

        print("------------------------------------------------------------------/n")

    #go though all pkl file expect login user to
    #get their brian bit data list to then
    #compare login user and other user data using the distance formula
    for x in res:
          #going through all the pkl files expect user
          if (directory + "\\" + x != directory + "\\" + "%s_data.pkl" % username):   
                print("---------------------%s----------------------" % x)
                with open(directory + "\\" + x, 'rb') as f:       #other user data files
                    new_two_data = pickle.load(f) # deserialize using load()
                    two_data_set = new_two_data["movie_play_data"]
                    two_data_username = new_two_data["Username"]
                    two_data_set_email = new_two_data["Email"]
                    two_data_age = ''

                    for age, name in usernames_and_ages:
                        if two_data_username == name:
                              #print(name + " MATCH")
                              two_data_age = age
                    
                        
                    
                    for y in two_data_set:      #go thorugh user data list   
                        #parse data list to clean data so we only have numbers   x
                        first = ""
                        for i in range(len(y)):
                            if i % 2 == 0:
                                    first = y[i]
                                    list_two.append(parse(str(first)))
                    print("len: " + str(len(list_two)))
                    #print(two_data_set_email)
                    print("-------------------------------------------")
            
                #compare Login user data to the other user data
                for (a,b) in zip(list_one, list_two):
                    # Calculate the Euclidean distance  
                    # between points a and b
                    # for clear explanation, comparing each packet number with logined user with other users
                    distance_ans_per_data = math.dist(a, b)
                    list_distance_avg_ans_per_user.append(distance_ans_per_data) 
                
                #get the avg of all distance formula ans
                #here transfer to Matchmaking page
                #transfer user name, the AVG, and email(if needed) to html webpage/jinja
                avg_login_dif_user = Average(list_distance_avg_ans_per_user) 
                print("Total avg: " + str(avg_login_dif_user) + "\n")
                list_two.clear()
                list_distance_avg_ans_per_user.clear()

                second_list = [two_data_username, avg_login_dif_user, two_data_set_email, two_data_age]
                username_average.append(second_list)
    
    print("\nList separated:")
    print(username_average)

    return username_average