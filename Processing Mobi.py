from calendar import calendar
import email
import time
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
db = firestore.client()
db.collection('Meessage').document('111111').update({'Message':""})
db.collection('Meessage').document('123457').update({'Message':""})

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
    print('check doc status')
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
        
def available_docs(Start_dt_time, End_dt_time):
    print('check time')
#     #This takes on the start_date_time and end_date_time and displays all doctors who
#     #are available on that day and displays all doctors available on that day 
#     #These would be the clints start and end time and date split to date, start time and end time 
    
#     #Start_dt_time and end_dt_time is from the users input
    # db = firestore.client()
    # start_dt_time = data()
    # end_dt_time = data()
    # db_date = db.collection
    # pracNumber = find_doc()
    # (u'Operational_Days').document()


    if start_dt_time>=db_date and end_dt_time<=db_date2:
        #get all doctors working at specific time slots with no appointment
        #  3 conditions are  doctors are displayed
        #all avaiable/working
        #must not have an appointment on the timeslot the user wants to book for
        #must be woking akeer but must have 
        print('Mo: Please enter an offfice email for the specific doctor you see and like to choose')
        input()
        return practice_num

    

    





def find_doc():
    print('find doctor')
    # This function searchs for a specific doctor through, either by surname or name or name and surname or office email
    # then returns the doctors practice number when found for further use in booking
    db = firestore.client()
    mo = ' The are 4 options:\nYou can search your doctor by name, or surname, or name and surname or office email\n'
    mo = mo + 'To search your doctor by:\n\tName enter "n" \n\tSurname enter "s"\n\tName and Surname enter "c" \n\tOffice email enter "e"'
    prac_num =''
    #db send and retrive
    c_input = tags(mo)
    while bool(prac_num) == False:
        if c_input.lower() == 'n':
            mo = ' Please enter the Name of the doctor you want to book. e.g) "John" or "Dumi"...'
            docInput = tags(mo)

            docs = db.collection('Doctors').where("Name","==",docInput).get()
            for doc in docs:
                prac_num = u'{}'.format(doc.to_dict()['Practice Number'])

                # print(prac_num)
            #This all can be redudant if we display all the doctors the useer picks on and by picking one hes send the doctor name to us and we taking the practice number but
            if len(prac_num.split())>1:
                mo2 = ' Oooh seems like there are too many doctors who share that  Name.\nPlease enter a different input for a more accurate output'
                #pract_num = tage(mo2)
                tags(mo2)
                #new prompt should have another field for more details
                #more where functions
            elif len(prac_num.split())<1:
                mo2 = ' Sorry seems like we couldnt find your specific doctor  please try again.'
                tags(mo2)
            else:
                print(docInput + ' and ' + prac_num)
                return prac_num

        elif c_input.lower() == 's':
                mo =' Please enter the Surname of the doctor you want to book. e.g) "van de merwe" or "zwane"...'
                docInput = docInput = tags(mo)
                docs = db.collection('Doctors').where("Surname","==",docInput).get()
                for doc in docs:
                        prac_num = u'{}'.format(doc.to_dict()['Practice Number'])
                        # print(prac_num)
                if len(prac_num.split())>1:
                    mo2 = 'Oooh seems like there are too many doctors who share that  Surname.\nPlease enter a different input for a more accurate output'
                    #pract_num = tage(mo2)
                    tags(mo2)
                    #new prompt should have another field for more details
                    #more where functions
                elif len(prac_num.split())<1:
                    mo2 =' Sorry seems like we couldnt find your specific doctor please try again.'
                    tags(mo2)
                else:
                    return prac_num
        elif c_input.lower() == 'c':
            mo = ' Please enter the Initials AND Surname of the doctor you want to book. e.g) "Chris Klopper" or "Frank Mahlangu"...'
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
                mo2 ='Oooh seems like there are too many doctors who share that Name and Surname.\nPlease enter a different input for a more accurate output'
                #pract_num = tage(mo2)
                tags(mo2)
                #new prompt should have another field for more details
                #more where functions
            elif len(prac_num.split())<1:
                mo2 =' Sorry seems like we couldnt find your specific doctor please try again.'
                tags(mo2)
            else:
                return prac_num
        elif c_input.lower() == 'e':
            mo = ' Please enter the Office Email of the doctor you want to book. e.g) "xolanizulumedical@gmail.com" or "info@medicalhealth.co.za"...'
            docInput = tags(mo)
            docs = db.collection('Doctors').where("Email","==",docInput).get()
            for doc in docs:
                prac_num = u'{}'.format(doc.to_dict()['Practice Number'])

                # print(prac_num)
            if len(prac_num.split())>1:
                mo2 ='Oooh seems like there are too many doctors who share that email.\nPlease enter a different input for a more accurate output'
                #pract_num = tage(mo2)
                tags(mo2)
                #new prompt should have another field for more details
                #more where functions
            elif len(prac_num.split())<1:
                mo2 =' Sorry seems like we couldnt find your specific doctor please try again.'
                tags(mo2)
            else:
                print(docInput + ' and ' + prac_num)
                return prac_num
        else: 
            #need to fix
            mo2 ='Mo: Sorry you must have entered an incorrect input please try again or type "cancel" to end the process'
            value = tags(mo2)
            if value.lower() == 'cancel':
                #cancel funntion?
                break
            else:
                prac_num = ''
                break
            
        


    
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



# def doc_working_days():
#     #This function is for displaying a doctors days which he is availableand the timeslots
def Booking():
    print('Booking')
    db = firestore.client()
    ###################################################Date
    resp = 'Please be informed that we start booking from 08:00 - 17:00 \n We book based on the availability of the client, then we check the availability of the doctor then we book!!\nWhat date would you like to book for?\n Please enter the date in the format: YYYY-MM-DD, for example 2022-05-24'
    
    bot_respon = db.collection(u'Meessage').document('111111').update({'Message' : resp})
    user_input= ''
    date = tags(resp) 
    print(date)  
    # date_time_slot = get_dt_time()
    #this now will be the user booking start time and end time dates separated
    # strt_dt_time = date_time_slot[0]
    # end_dt_time = date_time_slot[1]

    #getting the doctor now and his practice number
    # print(strt_dt_time)
    # print(end_dt_time)
    ################################################TimeSlots######################################
    resp =' What time slots would you like?'
    bot_respon = db.collection(u'Meessage').document('111111').update({'Message' : resp})
    user_input= ''
    slot = tags(resp)
    print(slot)
    slots = []
    slots = slot.split('-')
    start_dt_tm = date + ' ' + slots[0]
    end_dt_tm = date + ' ' + slots[1]
    print(start_dt_tm, end_dt_tm)
    ################################################Doctor################################
    resp = ' Would you like to see any avaiable doctor on your selected date and time, enter "a" or \nDo you have a specific doctor you would like to see whos in our system then enter "s"'
    user_input= ''
    dec = tags(resp)
    while True:
        if dec.lower() == 'a' or dec.lower() == 'available':
            available_doc = db.collection('Operational_Days').document().collection('working').where('operational_type','==','working').get()
            for doc in available_doc:
                doctors = u'{}'.format(available_doc.to_dict()['Doctor_ID'])
            print(doctors)
            finalDoct = 'Dr' + db.collection('Meessage').document('111111').update({'Message':doctors}) 
            break #after getting a doctor
        elif dec.lower() == 's' or dec.lower() == 'specific': 
            prac_num = find_doc()
            break
        else:
            resp = ' Sorry its either you entered the wrong value, i cant understand you statement please try again.\nRemember enter "s" - to pick a specific doctor or "a" to choose a doctor who is available at the time and slot you selected'
            dec = tags(resp)
    #After this loop it should display the booking cause it has client id, doctor id, start&end date and time  maybe we could add something for adding a reason for booking

    #DATABASE UPDATES APPPOINTMENTS DATABASE
def Cancel_Booking():
#   #This function is for the canceling intent
    db = firestore.client()

    mo = ' You trying to cancel an appointment, please allow me to check if you have any recent bookings and i will display them for you please enter yes or no to continue'
    
    bot_respon = db.collection(u'Meessage').document('111111').update({'Message' : mo})
    #get reponse from user
    user_input= ''

    while user_input == user_input or user_input == '':
        bot_respon =  db.collection('Meessage').document('123457').get()
        user_input= u'{}'.format(bot_respon.to_dict()['Message']) 

    # answer = user_input.lower()
    # mo = 'It works'
    # bot_respon = db.collection(u'Meessage').document('111111').update({'Message' : mo})
    # if answer == 'y':
    #    print('vvv')
    # else:
    #     print('Work on')


    #function to display all bookings
# def Reschedule():
#     #This function is for the rescheduling intent
def reschedule():
    from datetime import date
    from datetime import timedelta
    yesterday = date.today() - timedelta(days=1)
    resc = ' Please be informed you are entering the process of altering details of an existing booking, this means after making this change your old booking will no longer exist...\nPlease hold on while I fetch all bookings that can be altered.\nThe only bookings that can be altered are bookings no later than yesterday ('+ str(yesterday) + ')'

    db.collection(u'Meessage').document('111111').update({'Message' : resc})
    time.sleep(6)
    #fetch from database and if results == 0 then 
    booking = []
    #Popuate booking with database results 
    if len(booking) == 0:
        resc = ' Oops sorry seems like there are no available bookings for you to alter, if your booking is older than yesterday then booking has already been removed from the system please try booking a new appointment...'
    elif len(booking) == 1:
        resc = ' You have one boking which can be altered'
        #display the booking

    else:
        resc = ' Please pick the booking you would like to change or enter the booking id of that booking'

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
            Cancel_Booking()
        ##########################################################################################################################################################################
        ####################Rescheduling Appointments starts here######################################
        elif(i['tag']== 'reschedule' and i['tag']== tag):
            #will have anothe if statement to determine if user has any booking still open to rebook for
            #this will show current booking and display a calender of when next youd like to book
            reschedule()
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
    print('Intents')
    return res

def data():
        db = firestore.client()
        # getdata=checkValue()
        # while getdata==False:
        
        user_input =""
        time_loop()
        bot_respon =  db.collection('Meessage').document('123457').get()
        user_input= u'{}'.format(bot_respon.to_dict()['Message']) 

        mo = chatbot_response(user_input)
        db.collection(u'Meessage').document('111111').update({'Message' : mo})
        bot_respon =  db.collection('Meessage').document('123457').update({'Message':""})
    # return user_input

def tags(mo):
    db = firestore.client()
    #send mo response to db
     #db send and retrive
    db.collection(u'Meessage').document('111111').update({'Message' : mo})
    user_input= ''
    time_loop()
    bot_respon =  db.collection('Meessage').document('123457').get()
    user_input= u'{}'.format(bot_respon.to_dict()['Message']) 
    return user_input

def time_loop():
    db.collection('Meessage').document('123457').update({'Message':""}) 
    bot_respon =  db.collection('Meessage').document('123457').get()
    user_input= u'{}'.format(bot_respon.to_dict()['Message'])
    num = 2
    while user_input == '' or bool(user_input) == False:
        # time.sleep(num)
        bot_respon =  db.collection('Meessage').document('123457').get()
        user_input= u'{}'.format(bot_respon.to_dict()['Message']) 
        if user_input == '' or bool(user_input) == False:
            num += 1
        else:
            print('break')
            break

print('started')

while True:
    
        #print('Mo: ' + chatbot_response(input('You: ') ))
        #fetch from react native
        data()

        

