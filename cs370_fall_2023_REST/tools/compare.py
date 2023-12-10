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

print(directory)#+ "\cs370_fall_2023_REST")
#directory += "\cs370_fall_2023_REST"

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
def compare_data(username):
    #save all parse data save as float numbers for login user
    list_one = []

    #logger.debug("debug" + username)

    #plan to use one list to have another user data to then compare avarege the distance 
    #formula meaning after get the avg of current user to potiential parthner next partthner wil use this list to compare
    list_two = []

    #collect all the distance answers btw LoginUser and other users to then avg out all ans in the list
    list_distance_avg_ans_per_user = []

    #make the actual login user this open pickel part 
    with open(directory + "\\" + "%s_data.pkl" % username, 'rb') as f:       #"BOB_data.pkl"  #%s_data.pkl" % UserInfo["Username"]
        new_one_data = pickle.load(f) # deserialize using load()
        one_data_set = new_one_data["movie_play_data"]
        for x in one_data_set:
                #list_one.append(parse(x[0]))
                first = ""
#                print("\nanother forloop\n")
                for i in range(len(x)):
                      if i % 2 == 0:
                            #print(x[i])
                            first = x[i]
                            #print("SAVED STRING: ")
#                            print(first)
                            list_one.append(parse(str(first)))

        print("------------------MAIN - -----------------------" )
#        print(list_one[764])
        print("len: " + str(len(list_one)))
#        print(list_one[0])
        print("------------------------------------------------------------------/n")
        
    #must do some type of function to for loop through all the data 
    #ideas
    #through name, a number session, a number id type, 

    #go though all pkl file expect login user to
    #get their brian bit data list to then
    #compre login user and other user data using the distance formula
    for x in res:
          #going through all the pkl files expect user
          if (directory + "\\" + x != directory + "\\" + "%s_data.pkl" % username):   #%s_data.pkl" % UserInfo["Username"]
                print("---------------------%s----------------------" % x)
                with open(directory + "\\" + x, 'rb') as f:       #other user data files
                    new_two_data = pickle.load(f) # deserialize using load()
                    two_data_set = new_two_data["movie_play_data"]
                    two_data_username = new_two_data["Username"]
                    #name
                    for y in two_data_set:      #go thorugh user data list   x
                        #list_two.append(parse(y))   #parse data list to clean data go we only have numbers   x
                        first = ""
#                        print("\nanother forloop\n")
                        for i in range(len(y)):
                            if i % 2 == 0:
                                    #print(x[i])
                                    first = y[i]
#                                    print("SAVED STRING: ")
#                                    print(first)
                                    list_two.append(parse(str(first)))
#                    print("---------------------%s----------------------" % x)
#                    print(x)
#                    print(list_two)
                    print("len: " + str(len(list_two)))
                    print("-------------------------------------------")
            
                #compare Login user data to the other user data
#                len_1 = len(list_one)   #geting lenth of data of login user
#                len_2 = len(list_two)
#                index = 0
#                if(len_1 > len_2):
#                     index = len_2
#                elif(len_1 < len_2):
#                     index = len_1
#                else:
#                     index = len_1
#                count = 0
#                while count < index:
                    # Calculate the Euclidean distance  
                    # between points P and Q 
#                    distance_ans_per_data = math.dist(list_one[count], list_two[count]) 
                    #print(distance_ans_per_data) 
#                    list_distance_avg_ans_per_user.append(distance_ans_per_data)
#                    count+=1

                for (a,b) in zip(list_one, list_two):
                    # Calculate the Euclidean distance  
                    # between points P and Q 
                    #print(list_one[a])
                    #print(list_two[b])
#                    distance_ans_per_data = math.dist(list_one[count], list_two[count])
                    distance_ans_per_data = math.dist(a, b)
                    list_distance_avg_ans_per_user.append(distance_ans_per_data) 
#                    count+=1
                
#                print(list_distance_avg_ans_per_user)
                #get the avg of all distance formula ans
                #here transfer to Matchmaking page
                #transfer user name, the AVG, and email(if needed) to html webpage
                avg_login_dif_user = Average(list_distance_avg_ans_per_user) 
                print("Total avg: " + str(avg_login_dif_user) + "\n")
                list_two.clear()
                list_distance_avg_ans_per_user.clear()

                second_list = [two_data_username, avg_login_dif_user]
                username_average.append(second_list)

    print("\nList separated:")
    #print(list_one)
    #print(list_two)
    print(username_average)
    #return username_average

#compare_data()