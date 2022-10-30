from calendar import calendar
import email
from enum import auto
from platform import python_branch
from sqlite3 import DatabaseError
from tabnanny import check
from tokenize import Name
import nltk 
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import numpy as np
import datetime

from keras.models import load_model
model = load_model('chatbot_model.h5')
import json
import random
intents = json.loads(open('intents.json', encoding='utf-8').read())
words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('classes.pkl','rb'))

#  Database from firebase connction
#follow th step on website
#to get firebase installed onto pc
#db is online
#https://firebase.google.com/docs/admin/setup/#python
#while running if a weird error occurs
#use: pip install -U pycryptodome
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("med-mobi-firebase.json")
app = firebase_admin.initialize_app(cred)
db = firestore.client()

from firebase_admin import db

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence

def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0]*len(words)
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s:
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))

def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words, show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list


def doc_status(number,start_dt_time ,end_dt_time):
#     #this takes the doc practice number and the requested start time and end time dte of the user and compare if doctor is working on the day and if yes
    ##thee it goes to the appointment database and checks if he is not already book for that specific time slot if not it books the client boi
    ##if no he has an appointment at that day and time slot then ill say hes booked and display the date and time when the doctor is available on that day the the user picks another time slot


#     doc_stat = """ SELECT operation_type FROM operational_days WHERE doctor_id = :number"""
    
#     doc_compr = db.collection('Operational_Days').where('Doctor_ID',"==",number)
#     for doc in doc_compr:
#         doc_stat = u'{}'.format(doc.to_dict()['Operational_type'])
    
#     if bool(doc_stat) ==True:
#         print('Mo: Sorry your doctor is not working on that specific day')
                
#     elif doc_stat.lower() == 'leave':
#          print('Mo: Sorry your doctor is not working on that specific day')
#     else:
#         return doc_stat
    
# def available_docs(cStart_dt_time, cEnd_dt_time):
#     #This takes on the start_date_time and end_date_time and displays all doctors who
#     #are available on that day and displays all doctors available on that day 
#     #These would be the clints start and end time and date split to date, start time and end time 
#     cStart_dt_time =cStart_dt_time.split(' ')
#     cEnd_dt_time = cEnd_dt_time.split(' ')
#     app_date = cStart_dt_time[0]
#     app_start_tm =cStart_dt_time[1]
#     app_end_tm =cEnd_dt_time[1]
#     #We need the database to fetch all the doctors whos dates and times fit the discription 
#     #I think databe of operational_days should be, doc_id, start_date, start_time,end_date, end_time
#     db.collection('Operational_days').where("start_date","<=",app_date, "<=", "end_date") AND .where(sart)
#     #or alternitively we could have a python loop that checks every entry in the operational_days if the date and time are between the time frame and time slot and the doctor is working so therefore we can fetch the doctors details for display purpose(whether he is available or not
#     # which the code would  be
#     #for loop till the end of enteries in the operational_day table
#     date1 = start_date
#     date2 = end_date
#     time1 = start_time
#     time2 = end_time
#     if (date1 <= app_date<=date2):
#         if time1 <= app_start_tm and time2 >= app_end_tm:
#          #take the doctors practice number to check if hes not book already for that slot
         
    





def find_doc():
    # This function searchs for a specific doctor through, either by surname or name or name and surname or office email
#     # then returns the doctors practice number when found for further use in booking
    db = firestore.client()
    print('Mo: The are 4 options:\n You can search your doctor by name, or surname, or name and surname or office email')
    print('To search your doctor by:\nname enter "n" \nsurname enter "s"\nname and surname enter "c" \noffice email enter "e"')
    c_input = input('You: ').lower()
    if c_input == 'n':
        print('Mo: Please enter the Name of the doctor you want to book. e.g) "John" or "Dumi"...')
        docInput = input('You: ')
        docs = db.collection('Doctors').where("Name","==",docInput).get()
        for doc in docs:
            prac_num = u'{}'.format(doc.to_dict()['Practice Number'])
            print(prac_num)
        if len(prac_num.split())>1:
            print('Mo: oooh seems like there are too many doctors who share that  Name.\nPlease enter a different input for a more accurate output')
        elif len(prac_num.split())<1:
            print('Mo: Sorry seems like we couldnt find your specific doctor ' +  doc +' please try again.')
        else:
            return prac_num

    elif c_input == 's':
            print('Mo: Please enter the Surname of the doctor you want to book. e.g) "van de merwe" or "zwane"...')
            docInput = input('You: ')
            docs = db.collection('Doctors').where("Surname","==",docInput).get()
            for doc in docs:
                    prac_num = u'{}'.format(doc.to_dict()['Practice Number'])
                    print(prac_num)
            if len(prac_num.split())>1:
                print('Mo: oooh seems like there are too many doctors who share that  Surname.\nPlease enter a different input for a more accurate output')
            elif len(prac_num.split())<1:
                print('Mo: Sorry seems like we couldnt find your specific doctor ' + doc  + ' please try again.')
            else:
                return prac_num

    elif c_input == 'c':
        print('Mo: Please enter the Name AND Surname of the doctor you want to book. e.g) "Chris Klopper" or "Frank Mahlangu"...')
        do = input('You: ')
        prac_num= """ SELECT practice_num FROM doctors WHERE LOWER(name) IN (:doc) AND LOWER(surname) IN (:doc)"""
        if len(prac_num.split())>1:
            print('Mo: oooh seems like there are too many doctors who share that Name and Surname.\nPlease enter a different input for a more accurate output')
        elif len(prac_num.split())<1:
            print('Mo: Sorry seems like we couldnt find your specific doctor ' + doc + ' please try again.')
        else:
            return prac_num
    elif c_input == 'e':
        print('Mo: Please enter the Office Email of the doctor you want to book. e.g) "xolanizulumedical@gmail.com" or "info@medicalhealth.co.za"...')
        doc = input('You: ')
        docs = db.collection('Doctors').where("Email","==",docInput).get()
        for doc in docs:
            prac_num = u'{}'.format(doc.to_dict()['Practice Number'])
            print(prac_num)
        if len(prac_num.split())>1:
            print('Mo: oooh seems like there are too many doctors who share that email.\nPlease enter a different input for a more accurate output')
        elif len(prac_num.split())<1:
            print('Mo: Sorry seems like we couldnt find your specific doctor' + doc + ' please try again.')
               
        else:
            return prac_num
    elif c_input == 'cancel':
        print('Mo: canceling process....')
        return ''
    else: 
        print('Mo: Sorry you must have entered an incorrect input please try again or type "cancel" to end the process')
    


    
# def display_booking():
#     #this displays a recently build booking thea:
#     #Patient name, surname, Appointment start and end date and time, doctor name and surname
# def all_booking():
#     #This function will take a patients id number and display all booking which are not past today or which have not passed
def get_dt_time():
    #this one gets the date and times from react native, separates the:
    #start_date_time (10-11-2022 12:30) and end_date_time (10-11-2022 13:00)
    from datetime import datetime # has format yyyy-mm-dd so react must return same format
    today = datetime.now().date().strftime("%y-%m-%d")
    print('Mo: Please be informed that we start booking from 08:00 - 17:00 \n We book based on the availability of the client, then we check the availability of the doctor then we book!!')
    while True:
        print('Mo: What date would you like to book for\n Please enter the date in the format: YYYY-MM-DD HH:MM, for example 2022-05-24')
        #Display react CALendar
        date = input('You:')          
        if bool(date) == True and date >= today:
            #React native displays button for time slots in format 09:30-10:00 or ...
            print('Mo: What time slots would you like')
            slots = input('You: ')
            #slots = from react
            slots= slots.split('-')
            start_time_date= date + ' ' + slots[0]
            end_time_date = date + ' ' + slots[1]
            return [start_time_date, end_time_date]
        else:
            print('Mo: Sorry seems like your your date is invalid either its empty or the date has passed. \nLets try again')
     
    
    
# def doc_working_days():
#     #This function is for displaying a doctors days which he is availableand the timeslots
# def Booking():
#     #This function is for the booking intent
#     print('Mo: Please be informed that we start booking from 08:00 - 17:00 \n We book based on the availability of the client, then we check the availability of the doctor then we book!!
#     print('Mo: Please pick a date and the time slot youd like to book for.')
#     #Get dates and times from react natives
#     booking = get_dt_time()
#     #Get a doctor
#     while True:
#         print('Mo: Do you have a specific doctor you want to see who is in our system or \nWould you like me to display all the doctors available on your specific date(' + booking[0] + ' ' + booking[1] + '-' + booking[2] ')')
#         print('Mo: If you have a specific doctor please type "s" \nand if you would like to pick from available doctor on the day please type "d"')
#         if input('You: ').lower() =='s':
#             prac_num = find_doc()
#             if bool(prac_num) == False:
#                 break
#             else:
#                 doc_status(prac_num)
# def Cancel_Booking():
#     #This function is for the canceling intent
# def Reschedule():
#     #This function is for the rescheduling intent

def getResponse(ints, intents_json):
    #this is the function whos if statement must be modified for scheduling and rescheduling and booking and medical inquries
    #These functions work but im not sure cause my pc is acting up
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    #This is how we need to code the pop-ups but we need this whole entire function to save inputed data
    for i in list_of_intents:
        #Now we can add functions in the if statements that will take from the next user input
        if(i['tag']== 'booking' and i['tag']== tag):
            #needs calender and after will take user in3/put through a function
            #Must check if date is not before today, if doctor will be availble and if time is fine
     
       
##########################################################################################################################################################################
 ####################Booking Appointments starts here######################################
            #This must possibly be initialised as an array
            
            date_time_sot = get_dt_time()
            d_date= date_time_sot[0].split(' ')
            d_date= d_date[0]
            # result will me confirmation of booking
            print('Mo: Do you have a specific doctor you want to see who is in our system or \nWould you like me to display all the doctors available on your specific date (' + d_date + ')')
            choice = False
            while choice==False:
                print('Mo: If you have a specific doctor please type "s" \nand if you would like to pick from available doctor on the day please type "d"')
                doctor_name=input('You: ')
                if doctor_name.lower() =='s' or doctor_name.lower() =='specific':
                    prac_num = find_doc()
                    #status = doc_status(prac_num)
                    choice=True
                    break
                elif doctor_name.lower() =='d':
                    #avail_docs(book_date)
                    #then user needs to select doctor and then we book
                    choice=True
                    break
                else:
                    print('Mo: Sorry the input you entered is invalid please try again.\nRemember enter"s" for Specific doctor OR "d" for available doctors on the Day')
                    break

            break
##########################################################################################################################################################################
####################Canciling Appointments starts here######################################
        elif(i['tag']== 'cancel' and i['tag']== tag):
            #will use a function to determine if the is any booking anytime soon and will ask if you want to cancel this booking
            result = 'are you sure you want to cancel booking'
            break
##########################################################################################################################################################################
####################Rescheduling Appointments starts here######################################
        elif(i['tag']== 'reschedule' and i['tag']== tag):
            #will have anothe if statement to determine if user has any booking still open to rebook for
            #this will show current booking and display a calender of when next youd like to book
            result = 'to which day would you like to change to'
            break
        elif(i['tag']== tag):
            #this is for any other intent like greetings, goodbyes and so on
            result = random.choice(i['responses'])
            break
        else:
            #this is for an unrecognised intent
            result = "Please ask the right questions or statement"
    return result

def chatbot_response(msg):
    ints = predict_class(msg, model)
    res = getResponse(ints, intents)
    return res

while True:
     print('Mo: ' + chatbot_response(input('You: ') ))