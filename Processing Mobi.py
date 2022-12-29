###3HVE TO RUN pip install geopy AND pip install haversine

import email
import time
from calendar import calendar
from enum import auto
from heapq import merge
from platform import python_branch
from pydoc import doc
from sqlite3 import DatabaseError
from tabnanny import check
from tokenize import Name
from tracemalloc import Snapshot
from xml.etree.ElementTree import TreeBuilder
from geopy.geocoders import Nominatim
import haversine as hs
from haversine import Unit
# import requests 
# import json

# r =requests.get('http://get.geojs.io/')
# ip_req = requests.get('https://get.geojs.io/vl/ip/ip.json')
# ipAdd = ip_req.json()
# print(ipAdd)

import nltk
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()
import os
import pickle

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import datetime
import random

import numpy as np
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
from firebase_admin import credentials, firestore

cred = credentials.Certificate("med-mobi-firebase.json")
app = firebase_admin.initialize_app(cred)
db = firestore.client()

from firebase_admin import db

db = firestore.client()
db.collection('Meessage').document('111111').update({'Message':""})
db.collection('Meessage').document('123457').update({'Message':""})

loggedIn = db.collection('LoggedIn').document('123456789').get()
client_Email = u'{}'.format(loggedIn.to_dict()['user'])
log = db.collection('users').where('Email','==',client_Email).get()
for doc in log:
    client_ID = u'{}'.format(doc.to_dict()['IdNumber'])

print(client_ID)

print(client_Email)

db = firestore.client()

###ADD Doc_status to allavailable and Find_doc, Check for repeating values on the allavaible array thatas all


def clean_up_sentence(sentence):
    # return bag of words array: 0 or 1 for each word in the bag that exists in the sentence
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence.lower())
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
    sentence = sentence.lower()
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

def chatbot_response(msg):
    msg = msg.lower()
    ints = predict_class(msg, model)
    res = getResponse(ints, intents)
    print('Intents')
    return res

def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    
    print(tag)
    for i in list_of_intents:
            ####################Showing Appointments starts here######################################
        if(i['tag']== 'checking' and i['tag']== tag):
            display_booking('display')
            print ('display')
            break
            ####################Meddical issues start here######################################
        elif(i['tag']== 'medical' and i['tag']== tag):
            print ('med')
            selenium()
            break
            ####################Booking Appointments starts here######################################
        elif(i['tag']== 'booking' and i['tag']== tag):
            print ('book')
            Booking()
            ####################Canciling Appointments starts here######################################
        elif(i['tag']== 'cancel' and i['tag']== tag):
            print ('cancel')
            display_booking('cancel')
            break
            ####################Rescheduling Appointments starts here######################################
        elif(i['tag']== 'reschedule' and i['tag']== tag):
            print ('reschedule')
            display_booking('reschedule')
            break
            ####################Any other tag######################################
        elif(i['tag']== tag):
            print ('default')
            result = random.choice(i['responses'])
            break
            ###################UNKOWN INTENT######################################
        else:
            result = "Sorry unrecognised intent, please ask the right questions or statement"

    return result
    
def find_doc():
    print('find doctor')
    # This function searchs for a specific doctor through, either by surname or name or name and surname or office email
    # then returns the doctors practice number when found for further use in booking
    db = firestore.client()
    mo = ' The are 4 options:\nYou can search your doctor by name, or surname, or name and surname or office email\n'
    mo = mo + 'To search your doctor by:\n\tName enter "n" \n\tSurname enter "s"\n\tInitials and Surname enter "c" \n\tOffice email enter "e"'
    prac_num =[]
    # if the orac num gives you erros i changed it from prac_num = ''


    counter = 1
    
    c_input = tags(mo)
    while bool(prac_num) == False:
        if c_input.lower() == 'n' or c_input.lower() == 'name':
            mo = ' Please enter the Name of the doctor you want to book. e.g) "John" or "Dumi"...'
            docInput = tags(mo)

            docs = db.collection('Doctors').where("Name","==",docInput).get()
            for doc in docs:
                numb = u'{}'.format(doc.to_dict()['PracticeNumber'])
                prac_num.append(numb)

                # print(prac_num)
            #This all can be redudant if we display all the doctors the useer picks on and by picking one hes send the doctor name to us and we taking the practice number but
            if len(prac_num)>1:
                
                mo = ' Oooh seems like there are too many doctors who share that  Name.\nPlease pick the number of the exact doctor you want if '
                for num in prac_num:
                    doctors = db.collection('Doctors').where('PracticeNumber','==',num).get()
                    for doc in doctors:
                        pDoctorI = u'{}'.format(doc.to_dict()['Initials'])
                        pDoctorS = u'{}'.format(doc.to_dict()['Surname'])
                        pDoctorSp = u'{}'.format(doc.to_dict()['Specialization'])
                        pLocation = u'{}'.format(doc.to_dict()['Office_Location'])
            
                    mo = mo + '\n\t\t\tNumber: '+ str(counter) +'\n\t\t\tDoctor: Dr '+  str(pDoctorI) + ' '+ str(pDoctorS) +' '+ '\n\t\t\tDoctor Specialization: ' + str(pDoctorSp) + '\n\t\t\tOffice Location: ' + str(pLocation)
                    counter =+ 1
                #pract_num = tage(moPractice Number2)
                mo = mo + '\n\nPlease enter the number of the doctor you want...'
                select = tags(mo)
                while True:
                    x = select.isnumeric()
                    if x == True and int(select) <= counter:
                        prac_num = prac_num[(int(select) -1)]
                    elif select == 'cancel' or select == 'c' or select == 'terminate':
                        mo = " Process of finding a doctor has been terminated..."
                        db.collection('Meessage').document('111111').update({'Message': mo})
                        time_loop()
                        return
                    else:
                        mo = ' Invalid input please try again...'
                        select = tags(mo)
                #new prompt should have another field for more details
                #more where functions
            elif len(prac_num.split())<1:
                mo2 = ' Sorry seems like we couldnt find your specific doctor  please try again.'
                tags(mo2)
            else:

                print(docInput + ' and ' + prac_num)
                return prac_num

        elif c_input.lower() == 's' or c_input.lower() == 'surname':
                mo =' Please enter the Surname of the doctor you want to book. e.g) "van de merwe" or "zwane"...'
                docInput = docInput = tags(mo)

                docs = db.collection('Doctors').where("Surname","==",docInput).get()
                for doc in docs:
                        numb = u'{}'.format(doc.to_dict()['PracticeNumber'])
                        prac_num.append(numb)
                if len(prac_num)>1:
                    mo2 = 'Oooh seems like there are too many doctors who share that Surname.\nPlease enter the number for the doctor you want'
                    for num in prac_num:
                        doctors = db.collection('Doctors').where('PracticeNumber','==',num).get()
                        for doc in doctors:
                            pDoctorI = u'{}'.format(doc.to_dict()['Initials'])
                            pDoctorS = u'{}'.format(doc.to_dict()['Surname'])
                            pDoctorSp = u'{}'.format(doc.to_dict()['Specialization'])
                            pLocation = u'{}'.format(doc.to_dict()['Office_Location'])
                
                        mo = mo + '\n\t\t\tNumber: '+ str(counter) +'\n\t\t\tDoctor: Dr '+  str(pDoctorI) + ' '+ str(pDoctorS) +' '+ '\n\t\t\tDoctor Specialization: ' + str(pDoctorSp) + '\n\t\t\tOffice Location: ' + str(pLocation)
                        counter =+ 1
                    #pract_num = tage(moPractice Number2)
                    mo = mo + '\n\nPlease enter the number of the doctor you want...'
                    select = tags(mo)
                    while True:
                        x = select.isnumeric()
                        if x == True and int(select) <= counter:
                            prac_num = prac_num[(int(select) -1)]
                        else:
                            mo = ' Invalid input please try again...'
                            select = tags(mo)

                elif len(prac_num)<1:
                    mo2 =' Sorry seems like we couldnt find your specific doctor please try again.'
                    tags(mo2)
                else:
                    return prac_num

        elif c_input.lower() == 'c' or c_input.lower() == 'initials' or c_input.lower() == 'initials and surname':
            mo = ' Please enter the Initials AND Surname of the doctor you want to book. e.g) "MC Klopper" or "IR Mahlangu"...'
            docInput = docInput = tags(mo)
            docInput = docInput.split()
            initials = docInput[0]
            surname = docInput[1]
            #if not run remove .get()
            docs = db.collection('Doctors').where("Surname","==",surname).where("Initials","==",initials).get()
            
            for doc in docs:
                    numb = u'{}'.format(doc.to_dict()['PracticeNumber'])
                    prac_num.append(numb)
            if len(prac_num)>1:
                mo2 ='Oooh seems like there are too many doctors who share that Name and Surname.\nPlease pick the number of the doctor you want '
                for num in prac_num:
                    doctors = db.collection('Doctors').where('PracticeNumber','==',num).get()
                    for doc in doctors:
                        pDoctorI = u'{}'.format(doc.to_dict()['Initials'])
                        pDoctorS = u'{}'.format(doc.to_dict()['Surname'])
                        pDoctorSp = u'{}'.format(doc.to_dict()['Specialization'])
                        pLocation = u'{}'.format(doc.to_dict()['Office_Location'])
            
                    mo = mo + '\n\t\t\tNumber: '+ str(counter) +'\n\t\t\tDoctor: Dr '+  str(pDoctorI) + ' '+ str(pDoctorS) +' '+ '\n\t\t\tDoctor Specialization: ' + str(pDoctorSp) + '\n\t\t\tOffice Location: ' + str(pLocation)
                    counter =+ 1
                #pract_num = tage(moPractice Number2)
                mo = mo + '\n\nPlease enter the number of the doctor you want...'
                select = tags(mo)
                while True:
                    x = select.isnumeric()
                    if x == True and int(select) <= counter:
                        prac_num = prac_num[(int(select) -1)]
                    else:
                        mo = ' Invalid input please try again...'
                        select = tags(mo)

            elif len(prac_num)<1:
                mo2 =' Sorry seems like we couldnt find your specific doctor please try again.'
                tags(mo2)
            else:
                return prac_num

        elif c_input.lower() == 'e' or c_input.lower() == 'email' or c_input.lower() == 'office email' or c_input.lower() == 'office' or c_input.lower() == 'mail':
            mo = ' Please enter the Office Email of the doctor you want to book. e.g) "xolanizulumedical@gmail.com" or "info@medicalhealth.co.za"...'
            docInput = tags(mo)

            docs = db.collection('Doctors').where("Email","==",docInput).get()
            for doc in docs:
                numb = u'{}'.format(doc.to_dict()['PracticeNumber'])
                prac_num.append(numb)

            if len(prac_num)>1:
                mo2 ='Oooh seems like there are too many doctors who share that email.\nPlease enter the number of the doctor you want to pick...'
            
                for num in prac_num:
                    doctors = db.collection('Doctors').where('PracticeNumber','==',num).get()
                    for doc in doctors:
                        pDoctorI = u'{}'.format(doc.to_dict()['Initials'])
                        pDoctorS = u'{}'.format(doc.to_dict()['Surname'])
                        pDoctorSp = u'{}'.format(doc.to_dict()['Specialization'])
                        pLocation = u'{}'.format(doc.to_dict()['Office_Location'])
            
                    mo = mo + '\n\t\t\tNumber: '+ str(counter) +'\n\t\t\tDoctor: Dr '+  str(pDoctorI) + ' '+ str(pDoctorS) +' '+ '\n\t\t\tDoctor Specialization: ' + str(pDoctorSp) + '\n\t\t\tOffice Location: ' + str(pLocation)
                    counter =+ 1
                #pract_num = tage(moPractice Number2)
                mo = mo + '\n\nPlease enter the number of the doctor you want...'
                select = tags(mo)
                while True:
                    x = select.isnumeric()
                    if x == True and int(select) <= counter:
                        prac_num = prac_num[(int(select) -1)]
                    else:
                        mo = ' Invalid input please try again...'
                        select = tags(mo)

            elif len(prac_num)<1:
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
                return
            else:
                prac_num = ''
                break


def display_booking(intent):
    #THE CLIENT ID IS FROM THE LOG IN PAGE imporrt from database
    db = firestore.client()
    from datetime import date, datetime, timedelta
    today = datetime.now().date().strftime("%Y-%m-%d %H:%M" )
    yesterday = (datetime.now()- timedelta(days=1)).strftime("%Y-%m-%d %H:%M")
    print (yesterday)
    counter = 1
    Appointments = []

    if intent.lower() == 'reschedule':
        ##############add code calculates date between today and date of appointment if dates greter than 2 days that means he cant chnge the appointment figure it out


        resc = ' Please be informed you are entering the process of altering details of an existing booking, this means after making this change your old booking will no longer exist...\nPlease hold on while I fetch all bookings that can be altered.\nThe only bookings that can be altered are bookings no later than yesterday ('+ str(yesterday) + ')'
        #fetch all bookings whereby start_date_time is of the appointment >= today
        #store all in appointment[]
    

        if len(Appointments) == 0:
            count = len(Appointments)
        else:
            count = len(Appointments.split())

        userID = db.collection('Appointments').where('Patient_ID','==',client_ID).where('Start_date','>=',yesterday).get()
        for doc in userID:
            Appointments = u'{}'.format(doc.to_dict()['Booking_ID'])
        count = len(Appointments.split())


        if count == 0:
            resc = resc + ' Oops sorry seems like there are no available bookings for you to alter, if your booking is older than yesterday then booking has already been removed from the system please try booking a new appointment...'
            db.collection('Meessage').document('111111').update({'Message':resc})
            time_loop()
            return
        elif count == 1:
            resc = resc +' \n\nLooks like you only have one appointment which you can alter, here are the details:\n'
            # #display the booking
            # #GET bookingid then
            # db.collection('Meessage').document('111111').update({'Message':resc})
         
            ###Fetch user informatioon
            user = db.collection('users').where('IdNumber','==',client_ID).get()
            for doc in user:
                pName = u'{}'.format(doc.to_dict()['Name'])
                pSurname = u'{}'.format(doc.to_dict()['Surname'])
            ###Fetch practice number 
            bkID = db.collection('Appointments').where(u'Booking_ID',u'==',Appointments).get()
            for do in bkID:
                pDoctorNum = u'{}'.format(do.to_dict()['Doctor_Pract_Number'])
                start_dt_tm = u'{}'.format(do.to_dict()['Start_date'])
                end_dt_tm = u'{}'.format(do.to_dict()['End_date'])
            ####Fetch doctor details   
            doc_ref = db.collection('Doctors').where('PracticeNumber','==',pDoctorNum).get()
            for doc in doc_ref:
                pDoctorI = u'{}'.format(doc.to_dict()['Initials'])
                pDoctorS = u'{}'.format(doc.to_dict()['Surname'])
                pDoctorSp = u'{}'.format(doc.to_dict()['Specialization'])

            print(pDoctorNum)
            print(pDoctorI)

            resc = resc + '\n\t\t\t\tBooking Num: '+  str(Appointments) +'\n\t\t\t\tPatient Name: '+  str(pName) +' '+  str(pSurname) +'\n\t\t\t\tDoctor: Dr '+  str(pDoctorI) + ' '+ str(pDoctorS) +' '+ '\n\t\t\t\tDoctor Specialization: ' + str(pDoctorSp) + '\n\t\t\t\tAppointment Starts: ' + str(start_dt_tm) + '\n\t\t\t\tAppointment ends: ' + str(end_dt_tm) + '\n\nEnter "Yes" to confirm and reschedule this appointment or "No" to cancel/stop the process'

            answer = tags(resc).lower()

            while True:
                if answer == 'yes' or answer == 'y' or answer =='confirm' or answer == 'continue':
                    resc = ' To make any alteration of your appointments date or time please press the button above written "Pick Date" and change either the date or the time or both...'
                    dates = tags(resc)
                    print('date in funtion ', dates)
                    slots = selectDT(dates)
                    start_dt_tm = slots[0]
                    end_dt_tm = slots[1]
                    print(start_dt_tm, end_dt_tm)
                    while True:
                        status = doc_status(pDoctorNum, start_dt_tm,end_dt_tm).lower()
                        if status == 'booked':
                            resp = ' Seems like youre doctor is booked on the same date and time you want, would you like to change, the booking date or time or both if so please enter "yes" if not please enter "no" to cancel the process '
                            answer = tags(resp).lower()
                            while True:
                                if answer == 'yes' or  answer == 'y':
                                    resc = ' To make any alteration of your appointments date or time please press the button above written "Pick Date" and change either the date or the time or both...'
                                    dates = tags(resc)
                                    slots = selectDT(dates)
                                    start_dt_tm = slots[0]
                                    end_dt_tm = slots[1]
                                    print(start_dt_tm, end_dt_tm)
                                    break
                                elif  answer == 'no' or  answer == 'n' or  answer == 'cancel' or  answer == 'terminate':
                                    resc = ' Appointment alreration process terminated.'
                                    db.collection('Meessage').document('111111').update({'Message': resc})
                                    return
                                else: 
                                    resp = ' Could not understand your input please try again, remember use yes or no'
                                    answer = tags(resp).lower()
                        elif status == 'unavailabe':
                            resp = ' Seems like youre doctor is unavailable on the same date and time you want, would you like to change, the booking date or time or both if so please enter "yes" if not please enter "no" to cancel the process '
                            answer = tags(resp).lower()
                            while True:
                                if answer == 'yes' or  answer == 'y':
                                    resc = ' To make any alteration of your appointments date or time please press the button above written "Pick Date" and change either the date or the time or both...'
                                    dates = tags(resc)
                                    slots = selectDT(dates)
                                    start_dt_tm = slots[0]
                                    end_dt_tm = slots[1]
                                    print(start_dt_tm, end_dt_tm)
                                    break
                                elif  answer == 'no' or  answer == 'n' or  answer == 'cancel' or  answer == 'terminate':
                                    resc = ' Appointment alreration process terminated.'
                                    db.collection('Meessage').document('111111').update({'Message': resc})
                                    return
                                else: 
                                    resp = ' Could not understand your input please try again, remember use yes or no'
                                    answer = tags(resp).lower()
                        else:
                            #update the booking
                            booking_id = Appointments
                            user_doc_ref = db.collection('Appointments').document(booking_id)
                            user_doc_ref.update({
                                u'Start_date': start_dt_tm,
                                u'End_date' : end_dt_tm,
                                })

                            resc = ' You have rescheduled your appointment to the following details'+ '\n\t\t\tBooking Number: '+ str(booking_id)+'\n\t\t\tPatient Name: '+  str(pName) +' '+  str(pSurname) +'\n\t\t\tDoctor: Dr '+  str(pDoctorI) + ' '+ str(pDoctorS) +' '+ '\n\t\t\tDoctor Specialization: ' + str(pDoctorSp) + '\n\t\t\tAppointment Starts: ' + str(start_dt_tm) + '\n\tAppointment ends: ' + str(end_dt_tm) + '\nSee you then ): '
                            #break out of the function
                            db.collection('Meessage').document('111111').update({'Message': resp})
                            time_loop()
                            return
                    ############################Booking Intent, A choice available doctors############
                elif answer == 'no' or answer == 'n' or answer =='stop' or answer == 'cancel':
                    resc = ' Appointment alreration process terminated.'
                    db.collection('Meessage').document('111111').update({'Message': resc})
                    return
                else:
                    resc = ' Sorry could not understand your user input please try again remeber enter yes or no.'
                    answer = tags(resc).lower()

        elif count > 1:
            resc = ' You have the following appointments which you can alter: \n\t'
            user = db.collection('users').where('IdNumber','==',client_ID).get()
            for doc in user:
                pName = u'{}'.format(doc.to_dict()['Name'])
                pSurname = u'{}'.format(doc.to_dict()['Surname'])

            ###Fetch practice number 
            for app in Appointments:
                bkID = db.collection('Appointments').where(u'Booking_ID',u'==',app).get()
                
                for do in bkID:
                    pDoctorNum = u'{}'.format(do.to_dict()['Doctor_Pract_Number'])
                    start_dt_tm = u'{}'.format(do.to_dict()['Start_date'])
                    end_dt_tm = u'{}'.format(do.to_dict()['End_date'])
                    doc_ref = db.collection('Doctors').where('PracticeNumber','==',pDoctorNum).get()
                ####Fetch doctor details   
                    for doc in doc_ref:
                        pDoctorI = u'{}'.format(doc.to_dict()['Initials'])
                        pDoctorS = u'{}'.format(doc.to_dict()['Surname'])
                        pDoctorSp = u'{}'.format(doc.to_dict()['Specialization'])
                
                resc = resc + '\n\t\t\tNumber: '+ str(counter) +'\n\t\t\tBooking Number: '+  str(app) +'\n\t\t\tPatient Name: '+  str(pName) +' '+  str(pSurname) +'\n\t\t\tDoctor: Dr '+  str(pDoctorI) + ' '+ str(pDoctorS) +' '+ '\n\t\t\tDoctor Specialization: ' + str(pDoctorSp) + '\n\t\t\tAppointment Starts: ' + str(start_dt_tm) + '\n\t\t\tAppointment ends: ' + str(end_dt_tm) +'\n\n'
                counter =+ 1

            counter = counter - 1
            resc = resc + ' Please enter the number(1 or 2 or 3 or....) for the appointment youd like to reschedule'
            number = tags(resc)
            while True:
                x = number.isnumeric()
                if x == True and int(number) <= counter:
                    book_id = Appointments[(int(number) -1)]
                    break
                elif number == 'cancel' or number == ' exit' or number == 'terminate':
                    #breaks must call while function to return to main 
                    respo = ' You have choosen to termanate the process you can start a new enquiry with your next input'
                    db.collection('Meessage').document('111111').update({'Message': respo})
                    return
                else:
                    respo = ' Invalid entry please try again, please enter the number(1 or 2 or 3...) of the doctor you would like to pick.'
                    number = tags(respo)
            #SUPPOSE TO REFETCH IT AND DISPLAY 
            bkID = db.collection('Appointments').where(u'Booking_ID',u'==',book_id).get()
            for do in bkID:
                pDoctorNum = u'{}'.format(do.to_dict()['Doctor_Pract_Number'])
                start_dt_tm = u'{}'.format(do.to_dict()['Start_date'])
                end_dt_tm = u'{}'.format(do.to_dict()['End_date'])
            ###Fetch doctor details   
            doc_ref = db.collection('Doctors').where('PracticeNumber','==',pDoctorNum).get()
            for doc in doc_ref:
                pDoctorI = u'{}'.format(doc.to_dict()['Initials'])
                pDoctorS = u'{}'.format(doc.to_dict()['Surname'])
                pDoctorSp = u'{}'.format(doc.to_dict()['Specialization'])
            
            resc = '\n\t\t\t\tBooking Num: '+  str(book_id) +'\n\t\t\t\tPatient Name: '+  str(pName) +' '+  str(pSurname) +'\n\t\t\t\tDoctor: Dr '+  str(pDoctorI) + ' '+ str(pDoctorS) +' '+ '\n\t\t\t\tDoctor Specialization: ' + str(pDoctorSp) + '\n\t\t\t\tAppointment Starts: ' + str(start_dt_tm) + '\n\t\t\t\tAppointment ends: ' + str(end_dt_tm) + '\n\nEnter "Yes" to confirm and reschedule this appointment or "No" to cancel/stop the process.\n\nEnter "Yes" to confirm and reschedule this appointment or "No" to cancel/stop the process'

            answer = tags(resc).lower()
            while True:
                if answer == 'yes' or answer == 'y' or answer =='confirm' or answer == 'continue':
                    resc = ' To make any alteration of your appointments date or time please press the button above written "Pick Date" and change either the date or the time or both...'
                    dates = tags(resc)
                    slots = selectDT(dates)
                    start_dt_tm = slots[0]
                    end_dt_tm = slots[1]
                    print(start_dt_tm, end_dt_tm)
                    while True:
                        status = doc_status(pDoctorNum, start_dt_tm,end_dt_tm).lower()
                        if status == 'booked':
                            resp = ' Seems like youre doctor is booked on the same date and time you want, would you like to change, the booking date or time or both if so please enter "yes" if not please enter "no" to cancel the process '
                            answer = tags(resp).lower()
                            while True:
                                if answer == 'yes' or  answer == 'y':
                                    resc = ' To make any alteration of your appointments date or time please press the button above written "Pick Date" and change either the date or the time or both...'
                                    dates = tags(resc)
                                    slots = selectDT(dates)
                                    start_dt_tm = slots[0]
                                    end_dt_tm = slots[1]
                                    print(start_dt_tm, end_dt_tm)
                                    break
                                elif  answer == 'no' or  answer == 'n' or  answer == 'cancel' or  answer == 'terminate':
                                    return
                                else: 
                                    resp = ' Could not understand your input please try again, remember use yes or no'
                                    answer = tags(resp).lower()
                        elif status == 'unavailabe':
                            resp = ' Seems like youre doctor is unavailable on the same date and time you want, would you like to change, the booking date or time or both if so please enter "yes" if not please enter "no" to cancel the process '
                            answer = tags(resp).lower()
                            while True:
                                if answer == 'yes' or  answer == 'y':
                                        resc = ' To make any alteration of your appointments date or time please press the button above written "Pick Date" and change either the date or the time or both...'
                                        dates = tags(resc)
                                        slots = selectDT(dates)
                                        start_dt_tm = slots[0]
                                        end_dt_tm = slots[1]
                                        print(start_dt_tm, end_dt_tm)
                                        break
                                elif  answer == 'no' or  answer == 'n' or  answer == 'cancel' or  answer == 'terminate':
                                    return
                                else: 
                                    resp = ' Could not understand your input please try again, remember use yes or no'
                                    answer = tags(resp).lower()
                        else:
                            #Then confirm rescheduling
                            user_doc_ref = db.collection('Appointments').document(book_id)
                            user_doc_ref.update({
                                u'Start_date': start_dt_tm,
                                u'End_date' : end_dt_tm,
                                })
                            resc = ' You have rescheduled your appointment to the following details'+ '\n\t\t\tBooking Number: '+ str(booking_id)+'\n\t\t\tPatient Name: '+  str(pName) +' '+  str(pSurname) +'\n\t\t\tDoctor: Dr '+  str(pDoctorI) + ' '+ str(pDoctorS) +' '+ '\n\t\t\tDoctor Specialization: ' + str(pDoctorSp) + '\n\t\t\tAppointment Starts: ' + str(start_dt_tm) + '\n\tAppointment ends: ' + str(end_dt_tm) + '\nSee you then ): '
                            #break out of the function
                            tags(resc)
                            return

                elif answer == 'no' or answer == 'n' or answer =='stop' or answer == 'cancel':
                    resc = ' Appointment alreration process terminated.'
                    db.collection('Meessage').document('111111').update({'Message': resc})
                    return
                else:
                    resc = ' Sorry could not understand your input please try again, remember enter "yes" or "no"...'
                    answer = tags(resc).lower()


        ####################################################################################cancel#################################################################################  
    elif intent.lower() == 'cancel':
        print ('cancel')
        mo = ' You trying to cancel an appointment, please note you can only cancel appointments which are due to happen after or during '+str(today)+ '\nTo allow me to show you all recent appointments that you can cancel please enter "Yes" continue or "No" to cancel the process'
        userID = db.collection('Appointments').where('Patient_ID','==',client_ID).where('Start_date','>=',today).get()
        for doc in userID:
         Appointments.append(u'{}'.format(doc.to_dict()['Booking_ID']))
                    
        input =  tags(mo).lower()
        while True:
            print(input,len(Appointments) )
            if input== 'yes' or input == 'continue' or input == 'y':
            #fetched all user appointments and displays them all and prompt the user to enter the booking id of the appointment he wants to cancel
                if len(Appointments) == 0:
                    mo =' Sorry seems like you dont have any booking still up for show, this means your appointment has already passed due date and now you can just simply book a new appointment with me to do that just enter "Book" or "Book appointment"'
                    db.collection('Meessage').document('111111').update({'Message': mo})
                    return
                elif len(Appointments) == 1:
                    #MUST DISPLAY THE APPOINTMENT,
                    #find out how database returns the values in  the array first then str(Appointments will change)
                    mo = ' Looks like you only have one booking available for cancelation. \n\n\t '+ str(Appointments) +'\n\nPlease enter "yes" to cancel/delete the booking or "no" to stop this process'
                    input =  tags(mo).lower()
                    while True:
                        if input== 'yes' or input == 'continue' or input == 'y':
                            user = db.collection('users').where('IdNumber','==',client_ID).get()
                            for doc in user:
                                pName = u'{}'.format(doc.to_dict()['Name'])
                                pSurname = u'{}'.format(doc.to_dict()['Surname'])
                            ###Fetch practice number 
                            bkID = db.collection('Appointments').where(u'Booking_ID',u'==',Appointments).get()
                            for do in bkID:
                                pDoctorNum = u'{}'.format(do.to_dict()['Doctor_Pract_Number'])
                                start_dt_tm = u'{}'.format(do.to_dict()['Start_date'])
                                end_dt_tm = u'{}'.format(do.to_dict()['End_date'])
                                
                            print(pDoctorNum)
                            ####Fetch doctor details   
                            doc_ref = db.collection('Doctors').where('PracticeNumber','==',pDoctorNum).get()
                            for doc in doc_ref:
                                pDoctorI = u'{}'.format(doc.to_dict()['Initials'])
                                pDoctorS = u'{}'.format(doc.to_dict()['Surname'])
                                pDoctorSp = u'{}'.format(doc.to_dict()['Specialization'])

                            print(pDoctorNum)
                            print(pDoctorI)

                            mo = mo + ' You have only one booking which you can cancel, here are thedetails : \n\t\t\tBooking Number: '+  str(Appointments) +'\n\t\t\tPatient Name: '+  str(pName) +' '+  str(pSurname) +'\n\t\t\tDoctor: Dr '+  str(pDoctorI) + ' '+ str(pDoctorS) +' '+ '\n\t\t\t\tDoctor Specialization: ' + str(pDoctorSp) + '\n\t\t\tAppointment Starts: ' + str(start_dt_tm) + '\n\t\t\tAppointment ends: ' + str(end_dt_tm) +'\nEnter "yes" to cancel this booking or "no" to termanate the whole process'
                            answer = tags(mo).lower()
                            while True:
                                if answer == 'yes' or answer == 'y' or answer == 'continue':
                                    #DELETE STATEMENT FROM DATABASE
                                    db.collection('Appointments').document(Appointments).delete() 
                                    mo = ' Booking canceled. If the is anything else i can help you please type away remember i can also book, reschedule appointment plus give you so addation information about any disease you instead of "googling your sympotms"'
                                    db.collection('Meessage').document('111111').update({'Message': mo})
                                    data()
                                    return
                                elif answer == 'no' or answer == 'n' or answer == 'stop' or answer == 'terminate':
                                    mo = '  Process terminated..."'
                                    db.collection('Meessage').document('111111').update({'Message': mo})
                                    data()
                                    return
                                else:
                                    mo = 'Invalid input please try again remember enter "yes" to cancel the above booking or "no" to stop'
                                    answer = tags()
                            #Database delete appointment gotten
                            
                            
                        elif input== 'no' or input == 'cancel' or input == 'stop' or input == 'n':
                            mo = ' Process stoped, if the is anything else i can help you with please ask away, remember i can also book, reschedule appointment plus give you so addation information about any disease you instead of "googling your sympotms"'
                            db.collection('Meessage').document('111111').update({'Message': mo})
                            return
                        else: 
                            mo = ' Invalid input please try again, \n\tYes or No'
                            input =  tags(mo).lower()
                elif len(Appointments) > 1:
                    #Database fetches the bookings details displays the details
                    mo = ' Here are all the appointments you can cancel, you can only cancel appointments which are not younger than ' + str(today)+'.\nAnd here are your appointments:\n'
                    user = db.collection('users').where('IdNumber','==',client_ID).get()
                    for doc in user:
                        pName = u'{}'.format(doc.to_dict()['Name'])
                        pSurname = u'{}'.format(doc.to_dict()['Surname'])

                    ###Fetch practice number 
                    for app in Appointments:
                        bkID = db.collection('Appointments').where(u'Booking_ID',u'==',app).get()
                        
                        for do in bkID:
                            pDoctorNum = u'{}'.format(do.to_dict()['Doctor_Pract_Number'])
                            start_dt_tm = u'{}'.format(do.to_dict()['Start_date'])
                            end_dt_tm = u'{}'.format(do.to_dict()['End_date'])
                            doc_ref = db.collection('Doctors').where('PracticeNumber','==',pDoctorNum).get()
                        ####Fetch doctor details   
                            for doc in doc_ref:
                                pDoctorI = u'{}'.format(doc.to_dict()['Initials'])
                                pDoctorS = u'{}'.format(doc.to_dict()['Surname'])
                                pDoctorSp = u'{}'.format(doc.to_dict()['Specialization'])
                        
                        mo = mo +'\n\t\t\tNumber: '+ str(counter)+'\n\t\t\tBooking Number: '+  str(app) +'\n\t\t\tPatient Name: '+  str(pName) +' '+  str(pSurname) +'\n\t\t\tDoctor: Dr '+  str(pDoctorI) + ' '+ str(pDoctorS) +' '+ '\n\t\t\tDoctor Specialization: ' + str(pDoctorSp) + '\n\t\t\tAppointment Starts: ' + str(start_dt_tm) + '\n\t\t\tAppointment ends: ' + str(end_dt_tm)+ '\n' +'\nPlease enter the Number (1 or 2 or 3....) of the appointment you want to cancel'
                        counter +=1
                    counter = counter -1
                    app = tags(mo).lower()
                    ####Checks if entered value is in the array cause array has all the stored booking id's
                    while True:
                        x = app.isnumeric()
                        if x == True and int(app) <= counter:
                            book_id = Appointments[(int(app) -1)]
                            break
                        elif number == 'cancel' or number == ' exit' or number == 'terminate':
                            mo =' Process terminated...'
                            db.collection('Meessage').document('111111').update({'Message': mo})
                            return
                        else:
                            mo = ' Invalid input please try again...'
                            app = tags(mo)

                    #Goes to database gets that one bookking
                    bkID = db.collection('Appointments').where(u'Booking_ID',u'==',book_id).get()
                    for do in bkID:
                        pDoctorNum = u'{}'.format(do.to_dict()['Doctor_Pract_Number'])
                        start_dt_tm = u'{}'.format(do.to_dict()['Start_date'])
                        end_dt_tm = u'{}'.format(do.to_dict()['End_date'])
                            
                    print(pDoctorNum)
                    ####Fetch doctor details   
                    doc_ref = db.collection('Doctors').where('PracticeNumber','==',pDoctorNum).get()
                    for doc in doc_ref:
                        pDoctorI = u'{}'.format(doc.to_dict()['Initials'])
                        pDoctorS = u'{}'.format(doc.to_dict()['Surname'])
                        pDoctorSp = u'{}'.format(doc.to_dict()['Specialization'])
                        
                    mo = ' Please confirm: \n\t\t\t\tBooking Number: '+  str(book_id) +'\n\t\t\t\tPatient Name: '+  str(pName) +' '+  str(pSurname) +'\n\t\t\t\tDoctor: Dr '+  str(pDoctorI) + ' '+ str(pDoctorS) + '\n\t\t\t\t\tDoctor Specialization: ' + str(pDoctorSp) + '\n\t\t\t\tAppointment Starts: ' + str(start_dt_tm) + '\n\t\t\t\tAppointment ends: ' + str(end_dt_tm) + '\n\nPlease enter "Yes" to cancel this appointment or enter "No" to terminate this process'
                    answer = tags(mo).lower()
                    #dSelection of the appointments
                    while True:
                        if answer== 'yes' or answer == 'continue' or answer == 'y': 
                            print(answer)
                                #DELETE STATEMENT Database
                            db.collection('Appointments').document(book_id).delete()
                            mo = ' Booking canceled. If the is anything else i can help you please type away remember i can also book, reschedule appointment plus give you so addation information about any disease you instead of just searching your symptoms'
                            db.collection('Meessage').document('111111').update({'Message': mo})
                            return
                        elif answer== 'no' or answer == 'cancel' or answer == 'stop' or answer == 'n':
                            mo = ' Process stoped, if the is anything else i can help you with please ask away, remember i can also book, reschedule appointment plus give you so addation information about any disease you instead of "googling your sympotms"'
                            db.collection('Meessage').document('111111').update({'Message': mo})
                            return
                        else:
                                answer = tags(' Invalid input please try again, remember enter "Yes" to cancel the appointment or "No" to cancel this process')

            elif input== 'no' or input == 'cancel' or input == 'n':
                mo = ' You have termanated the process of canceling an appointment, if the is anything else i can help you with please ask away, remember i can also book, reschedule appointment plus give you so addation information about any disease you instead of "googling your sympotms"'
                db.collection('Meessage').document('111111').update({'Message': mo})
                return
            else: 
                mo = 'Invalid input please try again, \n\tYes or No'
                input =  tags(mo).lower()
      
       #########################################################display####################################################################### 
    elif intent.lower() == 'display':
       #Display all user appointments where Start_Date >= today
        mo = ' You have requested to see all your bookings and i will display for you booking which are not passed due date which is ' + str(today)
        # db.collection('Meessage').document('111111').update({'Message': mo})
        # time.sleep(2)
        userID = db.collection('Appointments').where('Patient_ID','==',client_ID).where('Start_date','>=',today).get()
        for doc in userID:
            Appointments.append(u'{}'.format(doc.to_dict()['Booking_ID']))


        if len(Appointments) == 0:
            count = len(Appointments)
        else:
            count = len(Appointments)

        print(Appointments,count)

        if count == 0:
            print (str(Appointments) + ' plus '+ str(count))
            mo = ' Sorry looks like you do not have any upcoming appointment, either its way past due date or you didnt create an appointment.'
            new = tags(mo)
            return new
        elif count == 1:
              ###Fetch user informatioon
            print (str(Appointments) + ' plus '+ str(count))
            user = db.collection('users').where('IdNumber','==',client_ID).get()
            for doc in user:
                pName = u'{}'.format(doc.to_dict()['Name'])
                pSurname = u'{}'.format(doc.to_dict()['Surname'])
            
            print(Appointments)
            ###Fetch practice number 
            app = Appointments[0]
            bkID = db.collection('Appointments').where(u'Booking_ID',u'==',app).get()
            for do in bkID:
                pDoctorNum = u'{}'.format(do.to_dict()['Doctor_Pract_Number'])
                start_dt_tm = u'{}'.format(do.to_dict()['Start_date'])
                end_dt_tm = u'{}'.format(do.to_dict()['End_date'])
                
            print(pDoctorNum)
            ####Fetch doctor details   
            doc_ref = db.collection('Doctors').where('PracticeNumber','==',pDoctorNum).get()
            for doc in doc_ref:
                pDoctorI = u'{}'.format(doc.to_dict()['Initials'])
                pDoctorS = u'{}'.format(doc.to_dict()['Surname'])
                pDoctorSp = u'{}'.format(doc.to_dict()['Specialization'])

            print(pDoctorNum)
            print(pDoctorI)

            mo = mo + ' You have an upcoming appointment, here are the details of this appointment: \n\t\t\tNumber'+ counter+'\n\t\t\tBooking Number: '+  str(app) +'\n\t\t\tPatient Name: '+  str(pName) +' '+  str(pSurname) +'\n\t\t\tDoctor: Dr '+  str(pDoctorI) + ' '+ str(pDoctorS) + '\n\t\t\t\tDoctor Specialization: ' + str(pDoctorSp) + '\n\t\t\tAppointment Starts: ' + str(start_dt_tm) + '\n\t\t\tAppointment ends: ' + str(end_dt_tm)

            db.collection('Meessage').document('111111').update({'Message': mo})
            return
        elif count > 1:
            print (str(Appointments) + ' plus '+ str(count))
            mo = mo +'Here are your upcoming appointments:  \nYou have an upcoming appointment, here are the details of this appointment: '
            #Dislay 
            user = db.collection('users').where('IdNumber','==',client_ID).get()
            for doc in user:
                pName = u'{}'.format(doc.to_dict()['Name'])
                pSurname = u'{}'.format(doc.to_dict()['Surname'])

            ###Fetch practice number 
            for app in Appointments:
                bkID = db.collection('Appointments').where(u'Booking_ID',u'==',app).get()
                
                for do in bkID:
                    pDoctorNum = u'{}'.format(do.to_dict()['Doctor_Pract_Number'])
                    start_dt_tm = u'{}'.format(do.to_dict()['Start_date'])
                    end_dt_tm = u'{}'.format(do.to_dict()['End_date'])
                    doc_ref = db.collection('Doctors').where('PracticeNumber','==',pDoctorNum).get()
                ####Fetch doctor details   
                    for doc in doc_ref:
                        pDoctorI = u'{}'.format(doc.to_dict()['Initials'])
                        pDoctorS = u'{}'.format(doc.to_dict()['Surname'])
                        pDoctorSp = u'{}'.format(doc.to_dict()['Specialization'])
                
                mo = mo + '\n\n\t\t\tNumber: '+ str(counter) +'\n\t\t\tBooking Number: '+  str(app) +'\n\t\t\tPatient Name: '+  str(pName) +' '+  str(pSurname) +'\n\t\t\tDoctor: Dr '+  str(pDoctorI) + ' '+ str(pDoctorS) +' '+ '\n\t\t\tDoctor Specialization: ' + str(pDoctorSp) + '\n\t\t\tAppointment Starts: ' + str(start_dt_tm) + '\n\t\t\tAppointment ends: ' + str(end_dt_tm) +'\n\n'
                counter = counter + 1
           
            mo = mo + 'Here are all your bookings hope to see you soon...'
            db.collection('Meessage').document('111111').update({'Message': mo})
            #NOTE !! I think (for app in appointments: db.collection('Meessage').document('111111').update({'Message': appointment[app]})
            return

def doc_status(docNum, start,end):
    workDay = db.collection('Operational_Days').where('Doctor_ID','==',docNum).where('operational_type','==','working').get()
    # the where with doc id is useless for any available doctor
    for doc in workDay:
        dat1 = u'{}'.format(doc.to_dict()['start_dt_time'])
        dat2 = u'{}'.format(doc.to_dict()['end_dt_time'])
        #print(dat1 + '  '+dat2)
        if start >= dat1 and end <= dat2:
            #if hes working on that day then we take hes practice number and then 
            availDocDate = db.collection('Appointments').where('Doctor_Pract_Number','==',docNum).get()
            print('step 1 achieved ')
            for i in availDocDate:
                print('step 2')
                date1 = u'{}'.format(i.to_dict()['Start_date'])
                date2 = u'{}'.format(i.to_dict()['End_date'])
                if start == date1 and end == date2:
                    return 'booked'
                    #prompt if the want to change anythingF
                else:
                    return 'free'
        else:
                return 'unavailable'

def all_available(start, end):
    resp = ' Please enter your current location to get the nearest doctor, you can enter the location in the format "Province City Township" for example "Gauteng Johanessburg Soweto Orlando" or just "Soweto Orlando" \nAlternatively, enter the location you want to see a doctor at'
    userloc = tags(resp)
    loc = Nominatim(user_agent="GetLoc")
    
    getLoc = loc.geocode(userloc)
    
    while getLoc ==None:
        resp = ' Could not find your specific location please try entering again. \n\nTry not to use abbriviation like "str" write the word in full, "street", and try write it in the following way: "street number and name, city, zip code" or "Province City Township zip code'
        userloc = tags(resp).lower()
        getLoc = loc.geocode(userloc)
   
    print(getLoc.address)

    resp = ' Please confirm, is this the location you were looking for\n\n' + str(getLoc.address) + ' \n\nPlease enter "yes" to confirm that it is the location or around that area or "no" to this is not the location you were looking for and you want to enter again:'
    answer = tags(resp).lower()
    while True:
        if answer == 'yes' or answer == 'y' or answer == 'it is' or 'continue' or answer =='agree' or answer == 'agree':
            workDay = db.collection('Operational_Days').where('operational_type','==','working').get()
            # the where with doc id is useless for any available doctor
            counter = 1
            #counter is for displaying doctor 

            allDoctors=[]
            distance = []
            
            for z in workDay:
                dat1 = u'{}'.format(z.to_dict()['start_dt_time'])
                dat2 = u'{}'.format(z.to_dict()['end_dt_time'])
                docNum = u'{}'.format(z.to_dict()['Doctor_ID'])
                availDocDate = db.collection('Appointments').where('Doctor_Pract_Number','==',docNum).get()
                # print(docNum)
                if start >= dat1 and end <= dat2:
                    #if hes working on that day then we take hes practice number and then 
                    for i in availDocDate:
                        date1 = u'{}'.format(i.to_dict()['Start_date'])
                        date2 = u'{}'.format(i.to_dict()['End_date'])
                        # print('Start: ' +date1 + ' End ' + date2)
                        if start != date1 and end != date2:
        ########################################################################MUST CALCULATE DISTANCE BETWEEN HERE IF LESS THAN OR == TO 100KM THEN APPEND ELSE NEXT 
                            #read comment above
                            Dr = db.collection('Doctors').where(u'PracticeNumber',u'==',i).get()
                            for do in Dr:
                                docLoc = u'{}'.format(do.to_dict()['Office_Location'])
                            
                            getDocLoc = loc.geocode(docLoc)
                            dis = round((hs.haversine((getLoc.latitude,getLoc.longitude),(getDocLoc.latitude,getDocLoc.longitude),unit=Unit.METERS)/1000),0)
                            check = docNum in allDoctors
                            
                            if check == False and dis <= 200:
                                distance.append(dis)
                                allDoctors.append(docNum)
                                print('Dr: ' + str(docNum) + '\nKM to user: ' + str(dis)) 
            print( len(allDoctors))
            print(allDoctors)
            #Checks if the are doctors available if not it breaks
            if len(allDoctors) == 0:
                    respo = ' Looks like the are no doctors available at the times you, would you like to change maybe the time and date if so please enter yes or enter cancel or no to stop the process.'
                    respond = tags(respo)
                    if respond.lower() == 'yes' or respond.lower() == 'y' or respond.lower() == 'proceed':
                        Booking()
                    elif respond.lower() == 'no' or respond.lower() == 'n':
                        return
                    
            else:
                respo =' Heres a list of doctors available: '
                #sorted by distance between
                for a in allDoctors:
                    avDoc = db.collection("Doctors").where('PracticeNumber','==',a).get()
                    for b in avDoc:
                        Initial = u'{}'.format(b.to_dict()['Initials'])
                        Surname = u'{}'.format(b.to_dict()['Surname'])
                        Spech = u'{}'.format(b.to_dict()['Specialization'])
                        loc = u'{}'.format(b.to_dict()['Office_Location'])
                        # timeslot = u'{}'.format(b.to_dict()['End_date'])
                        respo = respo + '\nNumber: ' + str(counter)+ '\nDoctor: Dr '+ str(Initial) + ' '+ str(Surname)+ '\nSpecialization: ' + str(Spech) + '\nOffice Location: ' + str(loc) + '\nRequested Time: '+ str(start)+ ' to '+ str(end) + '\nDistance to doctor: ' + str(distance[counter-1])
                        counter+=1
                
                counter = counter-1
                respo  = respo + ' Please enter the number(1 or 2 or 3...) of the doctor you would like to pick.'
                print(respo)
                #location shortest , prompt to display close to him/her or enter a provincee
                #must return a practice number\
                select = tags(respo)
                
                while True:
                    x = select.isnumeric()
                    if x == True and int(select) <= counter:
                        prac_num = allDoctors[(int(select) -1)]
                        print(prac_num)
                        #if x is a number and value enter is not greater than the last value count was
                        #display the doctor 
                        avDoc = db.collection("Doctors").where('PracticeNumber','==',prac_num).get()
                        for det in avDoc:
                            Initial = u'{}'.format(det.to_dict()['Initials'])
                            Surname = u'{}'.format(det.to_dict()['Surname'])
                            Spech = u'{}'.format(det.to_dict()['Specialization'])
                            loc = u'{}'.format(det.to_dict()['Office_Location'])
                        respo = '\nDoctor: Dr '+ Initial+ ' '+ Surname+ '\nSpecialization: ' + Spech + '\nOffice Location: ' + loc + '\nDistance From You: ' + str(dis) + '\nRequested Timeslot: ' + str(start) + ' Till ' + str(end)
                        db.collection('Meessage').document('111111').update({'Message': respo})
                        return prac_num
                    elif select == 'cancel' or select == ' exit' or select == 'terminate':
                        #breaks must call while function to return to main 
                        respo = ' You have choosen to termanate the process you can start a new enquiry with your next input'
                        db.collection('Meessage').document('111111').update({'Message': respo})
                        return
                    else:
                        respo = ' Invalid entry please try again, please enter the number(1 or 2 or 3...) of the doctor you would like to pick.'
                        select = tags(respo)
        elif answer == 'no' or answer == 'n' or answer == 'it is not' or 'no its not':
            resp = ' okay lets try get the location. Please enter the location/address at which you are looking for a doctor in: '
            userloc = tags(resp).lower()              
            getLoc = loc.geocode(userloc)
            answer = tags(resp).lower()
            resp = ' Please confirm, is this the location you were looking for\n\n' + str(getLoc.address) + ' \n\nPlease enter "yes" to confirm that it is the location or around that area or "no" to this is not the location you were looking for and you want to enter again:'
            answer = tags(resp).lower()


    # while True:
    #     if getLoc !=None:
    #         resp = ' Please confirm, is this the location you were looking for\n\n' + str(getLoc.address) + ' \n\nPlease enter "yes" to confirm that it is the location or around that area or "no" to this is not the location you were looking for and you want to enter again:'
    #         answer = tags(resp).lower()
    #         if answer == 'yes' or answer == 'y' or answer == 'it is' or 'continue' or answer =='agree' or answer == 'agree':
    #             break
    #         elif answer == 'no' or answer == 'n' or answer == 'it is not' or 'no its not':
    #             resp = ' okay lets try get the location. Please enter the location/address at which you are looking for a doctor in: '
    #             userloc = tags(resp).lower()              
    #             getLoc = loc.geocode(userloc)
    #     else:
    #         resp = ' Could not find your specific location please try entering again. \n\nTry not to use abbriviation like "str" write the word in full, "street", and try write it in the following way: "street number and name, city, zip code" or "Province City Township zip code'
    #         userloc = tags(resp).lower()
    #         getLoc = loc.geocode(userloc)
    #     break
        


def Booking():
    from datetime import datetime
    print('Booking')
    db = firestore.client()
    ###################################################Date
    resp = 'Please be informed that we start booking from 08:00 - 17:00 \n We book based on the availability of the client, then we check the availability of the doctor then we book!!\n'
    resp = resp + '\nWhat date would you like to book for?\nTo enter a date and time slot please press the buttom above writen "Pick Date"...'
    dates = tags(resp)
    slots = selectDT(dates)
    dates =''
    start_dt_tm = slots[0]
    end_dt_tm = slots[1]
    print(start_dt_tm, end_dt_tm)
    ################################################Doctor################################
    resp = ' To see a doctor who is availbale at your selected date and time, and at a location you want please enter "a" or \nDo you have a specific doctor you would like to see whos in our system then enter "s"'
    dec = tags(resp)

    while True:
        if dec.lower() == 'a' or dec.lower() == 'available':
            ##############################################################################
            
            while True:
                print('picked near by')
                #Getting practice number
                while True:
                    prac_num = all_available(start_dt_tm, end_dt_tm)
                    if bool(prac_num) == False:
                        resp = ' I just tried finding a doctor available at the date and time you selected.\nSeems like we cant find a doctor at your specific time frames so would you like to alter the date, if so please enter "yes" or enter "no" or "cancel" to stop the whole process...'
                        answer = tags(resp).lower()
                        while True:
                            if answer == 'yes' or  answer == 'y' or  answer == 'continue' or  answer == 'proceed':
                                resp = ' To change a date or time or both please press the button above written "Pick Date", to select one or the other or both...'
                                dates = tags(resp)
                                slots = selectDT(dates)
                                start_dt_tm = slots[0]
                                end_dt_tm = slots[1]
                                print(start_dt_tm, end_dt_tm)
                                break
                            elif  answer == 'no' or  answer == 'n' or  answer == 'terminate' or  answer == 'cancel':
                                resp = ' looks like you chose to cancel the process...'
                                db.collection('Meessage').document('111111').update({'Message': resp})
                                return
                            else:
                                resp = ' Sorry could not understand your input please try again remember enter "yes" or "no"...'
                                answer = tags(resp)
                    else:
                        break
                #Docstatus
                while True:
                    status = doc_status(prac_num, start_dt_tm,end_dt_tm).lower()
                    if status == 'booked':
                        resp = ' Seems like youre doctor is booked on the same date and time you want, would you like to change, the booking date or time or both if so please enter "yes" if not please enter "no" to cancel the process '
                        answer = tags(resp).lower()
                        while True:
                            if answer == 'yes' or  answer == 'y':
                                resp = ' To change a date or time or both please press the button above written "Pick Date", to select one or the other or both...'
                                dates = tags(resp)
                                slots = selectDT(dates)
                                start_dt_tm = slots[0]
                                end_dt_tm = slots[1]
                                print(start_dt_tm, end_dt_tm)
                                break 
                            elif  answer == 'no' or  answer == 'n' or  answer == 'cancel' or  answer == 'terminate':
                                return
                            else: 
                                resp = ' Could not understand your input please try again, remember use yes or no'
                                answer = tags(resp).lower()
                        break
                    elif status == 'unavailabe':
                        resp = ' Seems like youre doctor is unavailable on the same date and time you want, would you like to change, the booking date or time or both if so please enter "yes" if not please enter "no" to cancel the process '
                        answer = tags(resp).lower()
                        while True:
                            if answer == 'yes' or  answer == 'y':
                                resp = ' To change a date or time or both please press the button above written "Pick Date", to select one or the other or both...'
                                dates = tags(resp)
                                slots = selectDT(dates)
                                start_dt_tm = slots[0]
                                end_dt_tm = slots[1]
                                print(start_dt_tm, end_dt_tm)
                                break
                            elif  answer == 'no' or  answer == 'n' or  answer == 'cancel' or  answer == 'terminate':
                                resp = ' You choose to terminate..'
                                db.collection('Meessage').document('111111').update({'Message': resp})
                                return
                            else: 
                                resp = ' Could not understand your input please try again, remember use yes or no'
                                answer = tags(resp).lower()
                    else:
                        break
                break


        elif dec.lower() == 's' or dec.lower() == 'specific': 
            prac_num = find_doc()
            if bool(prac_num) == False or prac_num == None:
                print('no prac numb ', str(prac_num), ' return')
                return
            ##Check doc status
            while True:
                status = doc_status(prac_num, start_dt_tm,end_dt_tm).lower()
                if status == 'booked':
                    resp = ' Seems like youre doctor is booked on the same date and time you want, would you like to change, the booking date or time or both if so please enter "yes" if not please enter "no" to cancel the process '
                    answer = tags(resp).lower()
                    while True:
                        if answer == 'yes' or  answer == 'y':
                            resp = ' To change a date or time or both please press the button above written "Pick Date", to select one or the other or both...'
                            dates = tags(resp)
                            slots = selectDT(dates)
                            start_dt_tm = slots[0]
                            end_dt_tm = slots[1]
                            print(start_dt_tm, end_dt_tm)
                            break
                        elif  answer == 'no' or  answer == 'n' or  answer == 'cancel' or  answer == 'terminate':
                            return
                        else: 
                            resp = ' Could not understand your input please try again, remember use yes or no'
                            answer = tags(resp).lower()

                elif status == 'unavailabe':
                    resp = ' Seems like youre doctor is unavailable on the same date and time you want, would you like to change, the booking date or time or both if so please enter "yes" if not please enter "no" to cancel the process '
                    answer = tags(resp).lower()
                    while True:
                        if answer == 'yes' or  answer == 'y' or answer == 'continue' or answer == 'proceed':
                            resp = ' To change a date or time or both please press the button above written "Pick Date", to select one or the other or both...'
                            dates = tags(resp)
                            slots = selectDT(dates)
                            start_dt_tm = slots[0]
                            end_dt_tm = slots[1]
                            break
                        elif  answer == 'no' or  answer == 'n' or  answer == 'cancel' or  answer == 'terminate':
                            return
                        else: 
                            resp = ' Could not understand your input please try again, remember use yes or no'
                            answer = tags(resp).lower()
                else:
                    break
            break
        else:
            resp = ' Sorry its either you entered the wrong value, i cant understand you statement please try again.\nRemember enter "s" - to pick a specific doctor or "a" to choose a doctor who is available at the time and slot you selected'
            dec = tags(resp)
    #After this loop it should display the booking cause it has client id, doctor id, start&end date and time  maybe we could add something for adding a reason for booking
    user = db.collection('users').where('IdNumber','==',client_ID).get()
    for doc in user:
        pName = u'{}'.format(doc.to_dict()['Name'])
        pSurname = u'{}'.format(doc.to_dict()['Surname'])
    Dr = db.collection('Doctors').where(u'PracticeNumber',u'==',prac_num).get()
    for do in Dr:
        pDoctorI = u'{}'.format(do.to_dict()['Initials'])
        pDoctorS = u'{}'.format(do.to_dict()['Surname'])
        pDoctorSp = u'{}'.format(do.to_dict()['Specialization'])
        pLocation = u'{}'.format(doc.to_dict()['Office_Location'])
    resp = 'Please confrirm your booking to me.\n\t\t\t\tPatient Name: '+  str(pName) +' '+  str(pSurname) +'\n\t\t\t\tDoctor: Dr '+  str(pDoctorI) + ' '+ str(pDoctorS) +' '+ '\n\t\t\t\tDoctor Specialization: ' + str(pDoctorSp) + '\n\t\t\t\tDoctor Location: '+ str(pLocation)+'\n\t\t\t\tAppointment Starts: ' + str(start_dt_tm) + '\n\t\t\t\tAppointment ends: ' + str(end_dt_tm) + '\nPlease enter "Yes" to accept this booking or "No" to cancel booking process'
    confrim_appnt = tags(resp)
    while True:
        if confrim_appnt.lower()== 'yes' or confrim_appnt.lower() == 'continue' or confrim_appnt.lower() == 'y':
            random_id = ''.join([str(random.randint(0, 999)).zfill(3) for _ in range(2)])

             #Database add a booking into the database,Doctor_ID = prac_num, End_date = end_dt_tm, Start_date = start_dt_tm, patient_ID = client_ID
            sub = pSurname[0:3]
            sub2 = pName[0:1]
            booking_id = sub + random_id + sub2 #Fetch the booking id created from the appointment created above using the client Id
            # #add user to db
            user_doc_ref = db.collection('Appointments').document(booking_id)
            user_doc_ref.set({
                u'Booking_ID' : booking_id,
                u'Doctor_Pract_Number': prac_num,
                u'Patient_ID': client_ID, 
                u'Start_date': start_dt_tm,
                u'End_date' : end_dt_tm,
                })
            resp = ' You have the following appointment:'+ '\n\t\t\tBooking Number: '+ str(booking_id)+'\n\t\t\tPatient Name: '+  str(pName) +' '+  str(pSurname) +'\n\t\t\tDoctor: Dr '+  str(pDoctorI) + ' '+ str(pDoctorS) +' '+ '\n\t\t\tDoctor Specialization: ' + str(pDoctorSp) + '\n\t\t\t\tDoctors Location: '+ str(pLocation)+'\n\t\t\tAppointment Starts: ' + str(start_dt_tm) + '\n\tAppointment ends: ' + str(end_dt_tm) + '\nSee you then ): '
            #break out of the function
            db.collection('Meessage').document('111111').update({'Message': resp})
            time_loop()
            #timeloop oesnt do the right thing try sleep or just return like now
            return
        elif confrim_appnt.lower()== 'no' or confrim_appnt.lower() == 'cancel' or confrim_appnt.lower() == 'stop' or confrim_appnt.lower() == 'n':
            mo = ' Process stoped, if the is anything else i can help you with please ask away, remember i can also book, reschedule appointment plus give you so addation information about any disease you instead of "googling your sympotms"'
            db.collection('Meessage').document('111111').update({'Message': mo})
            return
        else: 
            mo = 'Invalid input please try again, \n\tYes or No'
            confrim_appnt =  tags(mo).lower()
        
 
def selectDT(dates):
    import datetime
    from datetime import datetime, timedelta
    print(dates)
    dates = dates.split('+')
    # print('new date is ' + str(dates))
    # print('the date received is ' + str(dates))
    start_dt_tm = str(dates[0])
    #print ('lets go ' + start_dt_tm)
    start_dt_tm = start_dt_tm[:-3] 
    #print('the start is ' + start_dt_tm)
    end_dt_tm = datetime.strptime(start_dt_tm, '%Y-%m-%d %H:%M') + timedelta(minutes=30)
    end_dt_tm = str(end_dt_tm)
    end_dt_tm = end_dt_tm[:-3]
    #print('start is ' + start_dt_tm + ' end is ' + end_dt_tm)
    
    return [start_dt_tm, end_dt_tm]

def selenium():
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait as WebD
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import NoSuchElementException
    from selenium.common.exceptions import StaleElementReferenceException
    from selenium.webdriver.chrome.options import Options
    import time

    #headles browsing
    def headless_window():
        #install chromedriver or any driver that accommodates the browser that you are using
        #put it in windows C in program files
        PATH = "C:\Program Files (x86)\chromedriver.exe"
        # instance of Options class allows
        # us to configure Headless Chrome
        options = Options()
            
        # this parameter tells Chrome that
        # it should be run without UI (Headless)
        options.headless = True

        # initializing webdriver for Chrome with our options
        tDriver = webdriver.Chrome(PATH,options=options)
        return tDriver

    all_info=[]
    
    def search_results(driver, name):
    
        # getting a website
        driver.get("https://nidirect.gov.uk/campaigns/illnesses-and-conditions")
        #accessing the search bar in the website
        search = driver.find_element(By.ID, 'edit-query-health-az')

        #accepting cookies
        cookie = driver.find_element(By.XPATH,"//*[@id='popup-buttons']/button[1]")
        time.sleep(1)
        cookie.click()

        #searching for a condition on the website
        search.send_keys(name)
        search.send_keys(Keys.RETURN)
        time.sleep(2)


        title =[]
        new=''
        new1=''
        new2=''
        symptoms = []
        # getting the title
        title =driver.find_elements(By.XPATH,"//*[@id='health-conditions-results']/ol/li/h3/a")
        symptoms = driver.find_elements(By.XPATH,"//*[@id='health-conditions-results']/ol/li/div[1]/ul/li")
        for i, s in zip(title, symptoms):
            # try:

            if(i.text == name):
                # clicking a link
                link = driver.find_element(By.XPATH,"//*[@id='health-conditions-results']/ol/li/h3/a")
                time.sleep(1)
                link.click()

                wait = WebD(driver, 100)
                #checks if there's content
                main = wait.until(EC.presence_of_element_located((By.ID,"main-content")))
                #finds the html or css that contains the content
                articles = main.find_elements(By.TAG_NAME,"article")
                
                for article in articles:
                    #getting short description about the condition
                    descrip = article.find_element(By.XPATH,"//*[@id='main-article']/div[2]")
                    all_info.append(descrip.text)

                    #getting the list of symptoms
                    symptom = article.find_element(By.CSS_SELECTOR,"#main-article > p:nth-child(8)")
                    all_info.append(symptom.text)

                    symptoms = article.find_element(By.XPATH,"//*[@id='main-article']/ul[1]")
                    all_info.append(symptoms.text)
                    
                    treatment = article.find_element(By.ID,"toc-2")
                    all_info.append(treatment.text)

                    treat1 = article.find_element(By.XPATH,"//*[@id='main-article']/p[14]")
                    all_info.append(treat1.text)
                    treat2 = article.find_element(By.XPATH,"//*[@id='main-article']/p[15]")
                    all_info.append(treat2.text)
                    treat3 = article.find_element(By.XPATH,"//*[@id='main-article']/p[16]")
                    all_info.append(treat3.text)
                for i in all_info:
                    print('done search')
                    new = new + i
                tags(new)
                return i
                
            elif(s.text == name.lower()):
                # clicking a link
                link = driver.find_element(By.XPATH,"//*[@id='health-conditions-results']/ol/li/h3/a")
                time.sleep(1)
                link.click()

                wait = WebD(driver, 100)
                #checks if there's content
                main = wait.until(EC.presence_of_element_located((By.ID,"main-content")))
                #finds the html or css that contains the content
                articles = main.find_elements(By.TAG_NAME,"article")

                for article in articles:
                    heading = article.find_element(By.CSS_SELECTOR,"#main-article > h1")
                    all_info.append(heading.text)
                    #getting short description about the condition
                    descrip = article.find_element(By.XPATH,"//*[@id='main-article']/div[2]")
                    all_info.append(descrip.text)

                    #getting the list of symptoms
                    symptom = article.find_element(By.CSS_SELECTOR,"#main-article > p:nth-child(8)")
                    all_info.append(symptom.text)

                    symptoms = article.find_element(By.XPATH,"//*[@id='main-article']/ul[1]")
                    all_info.append(symptoms.text)
                    
                    treatment = article.find_element(By.ID,"toc-2")
                    all_info.append(treatment.text)

                    treat1 = article.find_element(By.XPATH,"//*[@id='main-article']/p[14]")
                    all_info.append(treat1.text)
                    treat2 = article.find_element(By.XPATH,"//*[@id='main-article']/p[15]")
                    all_info.append(treat2.text)
                    treat3 = article.find_element(By.XPATH,"//*[@id='main-article']/p[16]")
                    all_info.append(treat3.text)
                for i in all_info:
                    print('done search')
                    new1 = new1 + i
                tags(new1)
                return i

            elif (i.text != name):
                tags("I'm sorry, that term is not available on this website")
                print('done search')
                new2 = new2 + i
                tags(new2) 
                break
        
    sel = "enter condition or symptoms:"
    searchNam = tags(sel).capitalize()  
    sel = 'Please wait as I gather information...'
    db.collection(u'Meessage').document('111111').update({'Message' : sel})
    if (len(searchNam) == 0):
        sel = "Sorry i didnt get that please try again..\nEnter condition: "
        searchNam = tags(sel).capitalize()
        driver = headless_window()
        articles = search_results(driver, searchNam)
    
    else:
        driver = headless_window()
        articles = search_results(driver, searchNam)

def data():
        db = firestore.client()
        user_input =""
        time_loop()
        bot_respon =  db.collection('Meessage').document('123457').get()
        user_input= u'{}'.format(bot_respon.to_dict()['Message']) 

        mo = chatbot_response(user_input)
        db.collection(u'Meessage').document('111111').update({'Message' : mo})
        bot_respon =  db.collection('Meessage').document('123457').update({'Message':""})
        return user_input

def tags(mo):
    db = firestore.client()
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
        bot_respon =  db.collection('Meessage').document('123457').get()
        user_input= u'{}'.format(bot_respon.to_dict()['Message']) 
        if user_input == '' or bool(user_input) == False:
            num += 1
        else:
            print('break')
            break

print('started')

#########This while loop need to be a function
while True:
        #print('Mo: ' + chatbot_response(input('You: ') ))
        #fetch from react native

        #tag = tags()
        # if tag == 'salutation' or  tag == 'booking' or  tag == 'reschedule' or tag == 'cancel' or tag == 'checking' or tag == 'medical':
        #     tags()
        # else:
        #     data()
        data()

        

