from calendar import calendar
import email
from enum import auto
from heapq import merge
from platform import python_branch
from pydoc import doc
from sqlite3 import DatabaseError
from tabnanny import check
from tokenize import Name
from tracemalloc import Snapshot
from xml.etree.ElementTree import TreeBuilder
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
    #this takes the doc practice number and the requested start time and end time dte of the user and compare if doctor is working on the day and if yes
    ##thee it goes to the appointment database and checks if he is not already book for that specific time slot if not it books the client boi
    ##if no he has an appointment at that day and time slot then ill say hes booked and display the date and time when the doctor is available on that day the the user picks another time slot
    db = firestore.client()
    workDay = db.collection('Opertaionl_Day.').document(number).collection('working').where('operational_type','==','working').get()
    for doc in workDay:
        db_date = u'{}'.format(doc.to_dict()['start_dt_time'])
        db_date2 = u'{}'.format(doc.to_dict()['end_dt_time'])
    #Nathi this takes the number which is the doctors practice number and goes to operational days and checks his time slots are within the users range
    #db_date is the doctors operational day start_time_date and db_date2 is end_dt_time
    if start_dt_time>=db_date and end_dt_time<=db_date2:
            #compare with appointments USER (start_dt_time and end_dt_time) AND DOCTORUSER (start_dt_time and end_dt_time) in that database to see if hes not booked or not already
            #db_ap_date is the doctors appointment date actually start_date_time and db_ap_date2 is  end_date_time 
            date = start_dt_time[0]
            chkslot = db.collection('Appoinments').document(number).collection('Booking_ID').get()
            for doc in chkslot:
                db_ap_date = u'{}'.format(doc.to_dict()['Start_date'])
                db_ap_date2 = u'{}'.format(doc.to_dict()['End_date'])
            if start_dt_time==db_ap_date and end_dt_time==db_ap_date2:
                mo = 'Mo: Your doctore is booked for the same time slot you want.\nWould you like to see all the time slots hes available on in this day'
                y_or_n = tags(mo)
                if y_or_n.lower() =='yes' or y_or_n.lower() =='y':
                    mo = 'Please select a time slot.'
                    #react native avaible slots
                    slot = tags(mo)
                    slots= slots.split('-')
                    start_time_date= date + ' ' + slots[0]
                    end_time_date = date + ' ' + slots[1]
                    return [start_time_date, end_time_date]
                elif y_or_n.lower() =='no' or y_or_n.lower() =='n':
                    #take them
                    print('Mo: Look like you wouldnt like an appointment on this day....\nLets start over')
                    print('Mo: Hey! I am mobi how can i help you')
                else:
                    print('Mo: Look like you wouldnt like an appointment on this day....\nLets start over')
                    print('Mo: Hey! I am mobi how can i help you')
            else:
                return[start_dt_time, end_dt_time]
    else:
            confirm2= True
            return [start_dt_time, end_dt_time]
        #I got it this is suppose to return the start date and time as confirmation
        
# def available_docs(Start_dt_time, End_dt_time):
#     #This takes on the start_date_time and end_date_time and displays all doctors who
#     #are available on that day and displays all doctors available on that day 
#     #These would be the clints start and end time and date split to date, start time and end time 
    
#     #Start_dt_time and end_dt_time is from the users input

#     #We need the database to fetch all the doctors whos dates and times fit the discription 
#     #I think databe of operational_days should be, doc_id, start_date, start_time,end_date, end_time
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
    mo = 'Mo: The are 4 options:\n You can search your doctor by name, or surname, or name and surname or office email'
    mo = mo + 'To search your doctor by:\nname enter "n" \nsurname enter "s"\nname and surname enter "c" \noffice email enter "e"'
    
    while True:
        c_input = tags(mo)
        if c_input == 'n':
            mo = 'Mo: Please enter the Name of the doctor you want to book. e.g) "John" or "Dumi"...'
            docInput = tags(mo)
            docs = db.collection('Doctors').where("Name","==",docInput).get()
            for doc in docs:
                prac_num = u'{}'.format(doc.to_dict()['Practice Number'])
                # print(prac_num)
            #This all can be redudant if we display all the doctors the useer picks on and by picking one hes send the doctor name to us and we taking the practice number but
            if len(prac_num.split())>1:
                mo2 = 'Mo: oooh seems like there are too many doctors who share that  Name.\nPlease enter a different input for a more accurate output'
            elif len(prac_num.split())<1:
                mo2 = 'Mo: Sorry seems like we couldnt find your specific doctor  please try again.'
            else:
                return prac_num

        elif c_input == 's':
                mo ='Mo: Please enter the Surname of the doctor you want to book. e.g) "van de merwe" or "zwane"...'
                docInput = docInput = tags(mo)
                docs = db.collection('Doctors').where("Surname","==",docInput).get()
                for doc in docs:
                        prac_num = u'{}'.format(doc.to_dict()['Practice Number'])
                        # print(prac_num)
                if len(prac_num.split())>1:
                    mo2 = 'Mo: oooh seems like there are too many doctors who share that  Surname.\nPlease enter a different input for a more accurate output'
                elif len(prac_num.split())<1:
                    mo2 ='Mo: Sorry seems like we couldnt find your specific doctor ' + doc  + ' please try again.'
                else:
                    return prac_num

        elif c_input == 'c':
            print('Mo: Please enter the Initials AND Surname of the doctor you want to book. e.g) "Chris Klopper" or "Frank Mahlangu"...')
            docInput = docInput = tags(mo)
            docInput = docInput.split()
            initials = docInput[0]
            surname = docInput[1]
            #if not run remove .get()
            docs = db.collection('Doctors').where("Surname","==",surname).where("Initials","==",initials).get()
            
            for doc in docs:
                    prac_num = u'{}'.format(doc.to_dict()['Practice Number'])
                    # print(prac_num)
            if len(prac_num.split())>1:
               mo2 ='Mo: oooh seems like there are too many doctors who share that Name and Surname.\nPlease enter a different input for a more accurate output'
            elif len(prac_num.split())<1:
                mo2 ='Mo: Sorry seems like we couldnt find your specific doctor please try again.'
            else:
                return prac_num
        elif c_input == 'e':
            print('Mo: Please enter the Office Email of the doctor you want to book. e.g) "xolanizulumedical@gmail.com" or "info@medicalhealth.co.za"...')
            docInput = docInput = tags(mo)
            docs = db.collection('Doctors').where("Email","==",docInput).get()
            for doc in docs:
                prac_num = u'{}'.format(doc.to_dict()['Practice Number'])
                # print(prac_num)
            if len(prac_num.split())>1:
                mo2 ='Mo: oooh seems like there are too many doctors who share that email.\nPlease enter a different input for a more accurate output'
            elif len(prac_num.split())<1:
                mo2 ='Mo: Sorry seems like we couldnt find your specific doctor please try again.'
                
            else:
                return prac_num
        elif c_input == 'cancel':
            #need o fix
            print('Mo: canceling process....')
            return ''
        else: 
            #need to fix
            print('Mo: Sorry you must have entered an incorrect input please try again or type "cancel" to end the process')
        mo = mo2 + ' ' + mo
        


    
def display_booking(client_Id, intent):
    #THE CLIENT ID IS FROM THE LOG IN PAGE imporrt from database
    from datetime import datetime, date, timedelta
    today = datetime.now().date().strftime("%y-%m-%d HH:mm" )
    # yesterday = date.today() - timedelta(days=1)
    # yesterday.strftime("%y-%m-%d HH:mm")

    #Now you have to select all the users appointments WHERE the appointment start_dt_time >= today From database
    #then well display booking



# def all_booking():
#     #This function will take a patients id number and display all booking which are not past today or which have not passed
def get_dt_time():
    mo = 'Mo: Please be informed that we start booking from 08:00 - 17:00 \n We book based on the availability of the client, then we check the availability of the doctor then we book!!'
    mo = mo + '\nMo: What date would you like to book for\n Please enter the date in the format: YYYY-MM-DD HH:MM, for example 2022-05-24'
    date = tags( mo)        
    input()
    print(date)
    if bool(date) == True:
        #React native displays button for time slots in format 09:30-10:00 or ...
        mo ='Mo: What time slots would you like'
        slots = tags(mo)
        input()
        #slots = from react
        slots= slots.split('-')
        print(slots[0])
        start_time_date= date + ' ' + slots[0]
        end_time_date = date + ' ' + slots[0]
        print(end_time_date)
        print(start_time_date)
        print(slots)
        return [start_time_date, end_time_date]
       #Make react react native have minimuValue in the calander display function of todays date so it cant take a date before today


     
    
    
# def doc_working_days():
#     #This function is for displaying a doctors days which he is availableand the timeslots
def Booking():
    date_time_slot = get_dt_time()
    #this now will be the user booking start time and end time dates separated
    strt_dt_time = date_time_slot[0]
    end_dt_time = date_time_slot[1]

    #getting the doctor now and his practice number
    print('Mo: Would you like to see any avaiable doctor on your selected date and time, enter "a" or \nDo you have a specific doctor you would like to see whos in our system then enter "s"')
    dec = input('You: ')
    while True:
        if dec.lower() == 'a':
            print('hey')
        elif dec.lower() == 's': 
            prac_num = find_doc()
        else:
            print('Mo: Could not understand your input try entering "a" to have all avaible doctors shown to you OR enter "s" to pick a specific doctor')

    status = doc_status(prac_num, strt_dt_time, end_dt_time)

    #at the end this function needs to display a booked appointment and its details

def Cancel_Booking():
#     #This function is for the canceling intent
    print('Mo: You trying to cancel an appointment, please allow me to check if you have any recent bookings and i will display them for you ')

    #function to display all bookings
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
            Booking()
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

# bot_respon = db.collection('Doctors').document('219958065').get()
# user_inp = u'{}'.format(bot_respon.to_dict()['Surname'])
# print(user_inp)
# mo = chatbot_response(user_inp)
# show = db.collection(u'users').document().get({u'Message' : mo})
# print(show)
def data():
        db = firestore.client()
        user_input =""
        bot_respon =  db.collection('Meessage').document('123457').get()
        user_input= u'{}'.format(bot_respon.to_dict()['Message']) 
        if bool(user_input) == False:
            return user_input 
        else:
            print(user_input)
            #respond
            mo = chatbot_response(user_input)
            db.collection(u'Meessage').document('123457').update({'Message' : mo})
            print(mo)
            # new = u'{}'.format(bot_respon.to_dict()['Message'])
            # pausedb = db.collection(u'Meessage').document('123457').get()
            # userGet = u'{}'.format(pausedb.to_dict()['Message']) 
            # input(userGet)
            return user_input

def tags(mo):
        db = firestore.client()
        db.collection(u'Meessage').document('123457').update({'Message' : mo})
        user_input =""
        bot_respon = db.collection(u'Meessage').document('123457').get()
        user_input = u'{}'.format(bot_respon.to_dict()['Message'])
        if bool(user_input) == False:
            while cont  == False:
                bot_respon = db.collection(u'Meessage').document('123457').get()
                user_input = u'{}'.format(bot_respon.to_dict()['Message'])
                if bool(user_input) == True:
                    cont = True       
        print(mo)
        return user_input

while True:
    
        #print('Mo: ' + chatbot_response(input('You: ') ))
        #fetch from react native
        data()
        input()
    
