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

# for i in workDay:
#         db_date = u'{}'.format(i.to_dict()['start_dt_time'])
#         db_date2 = u'{}'.format(i.to_dict()['end_dt_time'])
     
dt1 = '2022-12-24 11:00'
dt2 = '2022-12-24 11:30'
#################Specific###################
workDay = db.collection('Operational_Days').where('Doctor_ID','==','219958065').where('operational_type','==','working').get()
# the where with doc id is useless for any available doctor
for doc in workDay:
    dat1 = u'{}'.format(doc.to_dict()['start_dt_time'])
    dat2 = u'{}'.format(doc.to_dict()['end_dt_time'])
    print(dat1 + '  '+dat2)
    if dt1>=dat1 and dt2<=dat2:
        #if hes working on that day then we take hes practice number and then 
        availDocDate = db.collection('Appointments').where('Doctor_Pract_Number','==','219958065').get()
        print('step 1 achieved ')
        for i in availDocDate:
            print('step 2')
            date1 = u'{}'.format(i.to_dict()['Start_date'])
            date2 = u'{}'.format(i.to_dict()['End_date'])
            if dt1 == date1 and dt2 == date2:
                print('booked')
            else:
                print('doc is free')
    else:
            print('hade')
#################All Available doctors###################
print('all avail start here')
workDay = db.collection('Operational_Days').where('operational_type','==','working').get()
# the where with doc id is useless for any available doctor
counter = 1
for z in workDay:
    dat1 = u'{}'.format(z.to_dict()['start_dt_time'])
    dat2 = u'{}'.format(z.to_dict()['end_dt_time'])
    docNum = u'{}'.format(z.to_dict()['Doctor_ID'])

    if dt1>=dat1 and dt2<=dat2:
        #if hes working on that day then we take hes practice number and then 
        availDocDate = db.collection('Appointments').where('Doctor_Pract_Number','==',docNum).get()
        print('step 1 achieved ')
        for i in availDocDate:
            date1 = u'{}'.format(i.to_dict()['Start_date'])
            date2 = u'{}'.format(i.to_dict()['End_date'])
            if dt1 == date1 and dt2 == date2:
                print('next')
            else:
                print(docNum)

    else:
            print('hade')
#######################################################################
# if dt1>=db_date and dt2<=db_date2:
    





def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence

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


def doc_status(number,start_dt_time ,end_dt_time):
    ########################This functions other paremeter is LOCATION
    #this takes the doc PracticeNumber and the requested start time and end time dte of the user and compare if doctor is working on the day and if yes
    ##theen it goes to the appointment database and checks if he is not already book for that specific time slot if not it books the client boi
    ##if no he has an appointment at that day and time slot then ill say hes booked and display the date and time when the doctor is available on that day the the user picks another time slot


    #####START
    db = firestore.client()

    workDay = db.collection('Operational_Days').where('Doctor_ID','==',number).get()
    for i in workDay:
        db_date = u'{}'.format(i.to_dict()['start_dt_time'])
        db_date2 = u'{}'.format(i.to_dict()['end_dt_time'])
     
   
     

    #####END
    print('check doc status')
    db = firestore.client()
    workDay = db.collection('Opertaionl_Day.').document(number).collection('working').where('operational_type','==','working').get()
    for doc in workDay:
        db_date = u'{}'.format(doc.to_dict()['start_dt_time'])
        db_date2 = u'{}'.format(doc.to_dict()['end_dt_time'])
    #Nathi this takes the number which is the doctors practice number and goes to operational days and checks his time slots are within the users range
    #db_date is the doctors operational day start_time_date and db_date2 is end_dt_time
    #    userID = db.collection('Appointments').where('Patient_ID','==',client_ID).where('Start_date','>=',today).get()
            #compare with appointments USER (start_dt_time and end_dt_time) AND DOCTORUSER (start_dt_time and end_dt_time) in that database to see if hes not booked or not already
            #db_ap_date is the doctors appointment date actually start_date_time and db_ap_date2 is  end_date_time 
            # date = start_dt_time[0]
    #         chkslot = db.collection('Appoinments').document(number).collection('Booking_ID').get()
    #         for doc in chkslot:
    #             db_ap_date = u'{}'.format(doc.to_dict()['Start_date'])
    #             db_ap_date2 = u'{}'.format(doc.to_dict()['End_date'])
    #         if start_dt_time==db_ap_date and end_dt_time==db_ap_date2:
    #             mo = ' Your doctor is booked for the same time slot you want.\nWould you like to see all the time slots this doctor is available on for this day (' + str(date) + ') then enter "Yes". \nIf you would like to change and book for a different date and time slot then enter "change" or enter "No" to stop or cancel this whole process...'
    #             y_or_n = tags(mo)
    #             while True:
    #                 if y_or_n.lower() =='yes' or y_or_n.lower() =='y':
    #                     mo = ' Please select a time slot.'
    #                     #react native avaible slots
    #                     slot = tags(mo)
    #                     slots= slots.split('-')
    #                     start_time_date= date + ' ' + slots[0]
    #                     end_time_date = date + ' ' + slots[1]
    #                     return [start_time_date, end_time_date]
    #                 elif y_or_n.lower() =='no' or y_or_n.lower() =='n':
    #                     #take them
    #                     mo =' Look like you wouldnt like an appointment on this day....\nIf the is annything else i can help you with please type away, remember i can also book, cancel, reschedule and display appointments, and give you some information about any virus'
    #                     db.collection('Meessage').document('111111').update({'Message': mo})
    #                     return
    #                 elif y_or_n.lower() =='change' or y_or_n.lower() =='new' or y_or_n.lower() =='c':
    #                     Booking()
    #                     return
    #                 else:
    #                     mo = ' Sorry did not understand your input please try again remeber: \n\t"Yes"  to see your specified doctors free time slots on ('+ str(date)+') \n\t"No" to termanate this whole process and \n\t"change" for selecting a new date and different time slot of need be'
    #                     y_or_n = tags(mo)
    #         else:
    #             print ('Your doctor is  free and we can continue to completing the booking')
    #             return[start_dt_time, end_dt_time]
    # else:
    #        print('This means your doctor is not working that day so, pick a different doctor or pick a different  date and time slot')

        #I got it this is suppose to return the start date and time as confirmation
        
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
                prac_num = u'{}'.format(doc.to_dict()['PracticeNumber'])

                # print(prac_num)
            #This all can be redudant if we display all the doctors the useer picks on and by picking one hes send the doctor name to us and we taking the practice number but
            if len(prac_num.split())>1:
                mo2 = ' Oooh seems like there are too many doctors who share that  Name.\nPlease enter a different input for a more accurate output'
                #pract_num = tage(moPractice Number2)
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
                        prac_num = u'{}'.format(doc.to_dict()['PracticeNumber'])
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
                    prac_num = u'{}'.format(doc.to_dict()['PracticeNumber'])
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
                prac_num = u'{}'.format(doc.to_dict()['PracticeNumber'])

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
    db = firestore.client()
    from datetime import date, datetime, timedelta
    today = datetime.now().date().strftime("%Y-%m-%d %H:%M" )
    yesterday = (datetime.now()- timedelta(days=1)).strftime("%Y-%m-%d %H:%M")
    print (yesterday)
    Appointments = []

    if intent.lower() == 'reschedule':
        ##############add code calculates date between today and date of appointment if dates greter than 2 days that means he cant chnge the appointment figure it out


        resc = ' Please be informed you are entering the process of altering details of an existing booking, this means after making this change your old booking will no longer exist...\nPlease hold on while I fetch all bookings that can be altered.\nThe only bookings that can be altered are bookings no later than yesterday ('+ str(yesterday) + ')'
        db.collection('Meessage').document('111111').update({'Message': resc})
        time.sleep(2)
        #fetch all bookings whereby start_date_time is of the appointment >= today
        #store all in appointment[]

        if len(Appointments) == 0:
            count = len(Appointments)
        else:
            count = len(Appointments.split())

        userID = db.collection('Appointments').where('Patient_ID','==',client_ID).get()
        for doc in userID:
            newID = userID.where('Start_date','>=',yesterday).get()
        for doc in newID:
            Appointments = u'{}'.format(doc.to_dict()['Booking_ID'])
        count = len(Appointments.split())


        if count == 0:
            resc = ' Oops sorry seems like there are no available bookings for you to alter, if your booking is older than yesterday then booking has already been removed from the system please try booking a new appointment...'
            db.collection('Meessage').document('111111').update({'Message':resc})
            time_loop()
            return
        elif count == 1:
            resc = ' Looks like you only have one appointment which you can alter, here are the details:\n'
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
                    #Prompt for the date and time slot 
                    resc = ' Please select a new date and time slot or either one: '
                    date = tags(resc)
                    resc = ' Please enter a new time slot or enter the old one if you dont want to change it:'
                    slots = tags(resc)
                    #react native display actually
                    #now we automatically need to check if the same doctor he order for first is available in the new time slot then confirm to book with him again same day if not free, ask to dispay the doctor free time slots that day or pick any available doctor on the new time date


                    ############################Booking Intent, A choice available doctors############
                elif answer == 'no' or answer == 'n' or answer =='stop' or answer == 'cancel':
                    resc = ' Appointment alreration process terminated.'
                    db.collection('Meessage').document('111111').update({'Message': resc})
                    return
        elif count > 1:
            resc = ' You have the following appointments which you can alter: \n\t'
             #Display the appointments which can be changed
             #pick appointment and get booking_ID
            booking_id = tags(resc)
             #Display the booking alone
            Appointments
            resc = ' Enter "Yes" to confirm and cancel this appointment or "No" to cancel/stop the process'
            answer = tags(resc).lower()
            while True:
                if answer == 'yes' or answer == 'y' or answer =='confirm' or answer == 'continue':
                    #Prompt for the date and time slot 
                    resc = ' Please select a new date and time slot or either one: '
                    #react native display actually
                    #now we automatically need to check if the same doctor he order for first is available in the new time slot then confirm to book with him again same day if not free, ask to dispay the doctor free time slots that day or pick any available doctor on the new time date
                    ############################Booking Intent, A choice available doctors############
                elif answer == 'no' or answer == 'n' or answer =='stop' or answer == 'cancel':
                    resc = ' Appointment alreration process terminated.'
                    db.collection('Meessage').document('111111').update({'Message': resc})
                    return

        else:
            resc = ' Please pick the booking you would like to change or enter the booking id of that booking'
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
                        
                        mo = mo + '\n\t\t\tBooking Number: '+  str(app) +'\n\t\t\tPatient Name: '+  str(pName) +' '+  str(pSurname) +'\n\t\t\tDoctor: Dr '+  str(pDoctorI) + ' '+ str(pDoctorS) +' '+ '\n\t\t\tDoctor Specialization: ' + str(pDoctorSp) + '\n\t\t\tAppointment Starts: ' + str(start_dt_tm) + '\n\t\t\tAppointment ends: ' + str(end_dt_tm)+ '\n' +'\nPlease enter the booking id if the appointment you want to cancel'
                        app = tags(mo).lower()
                        ####Checks if entered value is in the array cause array has all the stored booking id's
                        for a in Appointments:
                            if a.loweer() == app:
                                print('correct booking id was entered')
                                break
                            elif a.lower() == 'cancel' or a.lower() == 'c' or a.lower() == 'stop':
                                mo = ' You have choosen to cancel this process'
                                db.collection('Meessage').document('111111').update({'Message': mo})
                                break
                            else:
                                print('booking id not there loop and try enter th right one')
                                mo = ' Oops Booking id entered was incorrect please try again:'
                                app = tags(mo).lower()

                        #Goes to database gets that one bookking
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
                        
                    mo = ' Please confirm: \n\t\t\t\tBooking Number: '+  str(app) +'\n\t\t\t\tPatient Name: '+  str(pName) +' '+  str(pSurname) +'\n\t\t\t\tDoctor: Dr '+  str(pDoctorI) + ' '+ str(pDoctorS) + '\n\t\t\t\t\tDoctor Specialization: ' + str(pDoctorSp) + '\n\t\t\t\tAppointment Starts: ' + str(start_dt_tm) + '\n\t\t\t\tAppointment ends: ' + str(end_dt_tm) + '\n\nPlease enter "Yes" to cancel this appointment or enter "No" to terminate this process'
                    answer = tags(mo).lower()
                    #dSelection of the appointments
                    while True:
                        if answer== 'yes' or answer == 'continue' or answer == 'y': 
                            print(answer)
                                #DELETE STATEMENT Database
                            db.collection('Appointments').document(app).delete()
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
            db.collection('Meessage').document('111111').update({'Message': mo})
            time.sleep(2)
            return
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

            mo = mo + ' You have an upcoming appointment, here are the details of this appointment: \n\t\t\tBooking Number: '+  str(app) +'\n\t\t\tPatient Name: '+  str(pName) +' '+  str(pSurname) +'\n\t\t\tDoctor: Dr '+  str(pDoctorI) + ' '+ str(pDoctorS) + '\n\t\t\t\tDoctor Specialization: ' + str(pDoctorSp) + '\n\t\t\tAppointment Starts: ' + str(start_dt_tm) + '\n\t\t\tAppointment ends: ' + str(end_dt_tm)

            new = tags(mo)
            return new
        elif count > 1:
            print (str(Appointments) + ' plus '+ str(count))
            mo = 'Here are your upcoming appointments:  \nYou have an upcoming appointment, here are the details of this appointment: '
            #Dislay out of line mybe use SLEEP.time
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
                
                mo = mo + '\n\t\t\tBooking Number: '+  str(app) +'\n\t\t\tPatient Name: '+  str(pName) +' '+  str(pSurname) +'\n\t\t\tDoctor: Dr '+  str(pDoctorI) + ' '+ str(pDoctorS) +' '+ '\n\t\t\tDoctor Specialization: ' + str(pDoctorSp) + '\n\t\t\tAppointment Starts: ' + str(start_dt_tm) + '\n\t\t\tAppointment ends: ' + str(end_dt_tm) +'\n\n'
            mo = mo + 'Here are all your bookings hope to see you soon...'
            db.collection('Meessage').document('111111').update({'Message': mo})
            data()
            #NOTE !! I think (for app in appointments: db.collection('Meessage').document('111111').update({'Message': appointment[app]})
            return


def Booking():
    print('Booking')
    db = firestore.client()
    ###################################################Date
    resp = 'Please be informed that we start booking from 08:00 - 17:00 \n We book based on the availability of the client, then we check the availability of the doctor then we book!!\nWhat date would you like to book for?\n Please enter the date in the format: YYYY-MM-DD, for example 2022-05-24'
    
    bot_respon = db.collection(u'Meessage').document('111111').update({'Message' : resp})
    user_input= ''
    date = tags(resp) 
    print(date)  
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
             ################################################################################opperationaldays -> working -> where start_date<=start_dt_tm and end_date>=end_dt_tm
            ##########CREATE A FUNCTION FOR THIS CAUSE RESCHEDULE uses it as well
            break #after getting a doctor
        elif dec.lower() == 's' or dec.lower() == 'specific': 
            prac_num = find_doc()
            #################MERGER DOC_STATUS WITH FIND DOCTOR
            #################################################################DOC_STATUS FUNCTION
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

    resp = 'Please confrirm your booking to me.\n\t\t\t\tPatient Name: '+  str(pName) +' '+  str(pSurname) +'\n\t\t\t\tDoctor: Dr '+  str(pDoctorI) + ' '+ str(pDoctorS) +' '+ '\n\t\t\t\tDoctor Specialization: ' + str(pDoctorSp) + '\n\t\t\t\tAppointment Starts: ' + str(start_dt_tm) + '\n\t\t\t\tAppointment ends: ' + str(end_dt_tm) + '\nPlease enter "Yes" to accept this booking or "No" to cancel booking process'
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
            resp = ' You have the following appointment:'+ '\n\t\t\tBooking Number: '+ str(booking_id)+'\n\t\t\tPatient Name: '+  str(pName) +' '+  str(pSurname) +'\n\t\t\tDoctor: Dr '+  str(pDoctorI) + ' '+ str(pDoctorS) +' '+ '\n\t\t\tDoctor Specialization: ' + str(pDoctorSp) + '\n\t\t\tAppointment Starts: ' + str(start_dt_tm) + '\n\tAppointment ends: ' + str(end_dt_tm) + '\nSee you then ): '
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
    #DATABASE UPDATES APPPOINTMENTS DATABASE
def selenium():
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait as WebD
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    import time
    print('spopo function comes here edit it of course')
    sel = ' Are you trying to enquire or get some information about common diseases and or viruse, if so enter "Yes" if not enter "No"'
    answer = tags(sel).lower()     
    if answer == 'yes' or answer == 'y' or answer =="continue":
        print('continue to seleinuem function of spopo')

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


        #array to hold all the content
        all_videos_title = []


        def getting_info(driver, name):
            # getting a website
            driver.get("https://nidirect.gov.uk/campaigns/illnesses-and-conditions")
            #accessing the search bar in the website
            search = driver.find_element(By.ID, 'edit-query-health-az')

            #accepting cookies
            acept = driver.find_element(By.XPATH,"//*[@id='popup-buttons']/button[1]")
            time.sleep(1)
            acept.click()

            #searching for a condition on the website
            search.send_keys(name)
            search.send_keys(Keys.RETURN)
            # clicking a link
            ele = driver.find_element(By.XPATH,"//*[@id='health-conditions-results']/ol/li[1]/h3/a")
            time.sleep(1)
            ele.click()


            wait = WebD(driver, 100)
            #checks if there's content
            main = wait.until(EC.presence_of_element_located((By.ID,"main-content")))
            #finds the html or css that contains the content
            articles = main.find_elements(By.TAG_NAME,"article")
            return articles

        def get_info(arti):
            #prints all content on that page
            for article in arti:
                dea = article.find_element(By.CSS_SELECTOR,"#main-article > h1")
                all_videos_title.append(dea.text)
                #getting short description about the condition
                header = article.find_element(By.XPATH,"//*[@id='main-article']/div[2]")
                all_videos_title.append(header.text)

                #getting the list of symptoms
                sympMains = article.find_element(By.CSS_SELECTOR,"#main-article > p:nth-child(8)")
                all_videos_title.append(sympMains.text)

                symptoms = article.find_element(By.XPATH,"//*[@id='main-article']/ul[1]")
                all_videos_title.append(symptoms.text)
                
                treatment = article.find_element(By.ID,"toc-2")
                all_videos_title.append(treatment.text)

                treat1 = article.find_element(By.XPATH,"//*[@id='main-article']/p[14]")
                all_videos_title.append(treat1.text)
                treat2 = article.find_element(By.XPATH,"//*[@id='main-article']/p[15]")
                all_videos_title.append(treat2.text)
                treat3 = article.find_element(By.XPATH,"//*[@id='main-article']/p[16]")
                all_videos_title.append(treat3.text)
            for i in all_videos_title:
                print(i)
                #Ithink this is where selenium prints in the terminal so
                db.collection('Meessage').document('111111').update({'Message': i})
                time_loop()
            return


        sel = 'I can display to you information about a certain viruse, disease or infection you might want to know, like its symptoms and treatments, for me to do so: \nplease enter the either the virus/diseas name: or symptom or condition: '
        searchNam = tags(sel)

        if (len(searchNam) == 0):
            #searchNam = input("enter condition or symptoms: ")
            driver = headless_window()
            articles = getting_info(driver, searchNam)
            info = get_info(articles)
        else:
            driver = headless_window()
            articles = getting_info(driver, searchNam)
            info = get_info(articles)
            return
    elif answer == 'no' or answer == 'n' or answer =="cancel" or answer == 'stop':
        sel = 'Okay, if the is anything else i can help you with please ask away, remember i can also book, cancel and reschedule appointments with any doctor in our system...'
        #update databse and app
        return


def getResponse(ints, intents_json):
    #this is the function whos if statement must be modified for scheduling and rescheduling and booking and medical inquries
    #These functions work but im not sure cause my pc is acting up
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    
    print(tag)
    #This is how we need to code the pop-ups but we need this whole entire function to save inputed data
    for i in list_of_intents:
        #Now we can add functions in the if statements that will take from the next user input
        
            ##########################################################################################################################################################################
            ####################Showing Appointments starts here######################################
        if(i['tag']== 'checking' and i['tag']== tag):
            display_booking(client_ID, 'display')
            print ('display')
            break
            ##########################################################################################################################################################################
            ####################Meddical issues start here######################################
        elif(i['tag']== 'medical' and i['tag']== tag):
            print ('med')
            selenium()
            break
        elif(i['tag']== 'booking' and i['tag']== tag):
            #needs calender and after will take user in3/put through a function
            #Must check if date is not before today, if doctor will be availble and if time is fine
            print ('book')
     
       
            ##########################################################################################################################################################################
            ####################Booking Appointments starts here######################################
            #This must possibly be initialised as an array
            Booking()
            ##########################################################################################################################################################################
            ####################Canciling Appointments starts here######################################
        elif(i['tag']== 'cancel' and i['tag']== tag):
            print ('cancel')
            #will use a function to determine if the is any booking anytime soon and will ask if you want to cancel this booking
            display_booking(client_ID, 'cancel')
            break
            ##########################################################################################################################################################################
            ####################Rescheduling Appointments starts here######################################
        elif(i['tag']== 'reschedule' and i['tag']== tag):
            print ('reschedu;l')
            #will have anothe if statement to determine if user has any booking still open to rebook for
            #this will show current booking and display a calender of when next youd like to book
            display_booking(client_ID,'reschedule')
            break
    
            ##########################################################################################################################################################################
            ####################Any other tag######################################
        elif(i['tag']== tag):
            print ('default')
            #this is for any other intent like greetings, goodbyes and so on
            result = random.choice(i['responses'])
            break
            #########################################################################################################################################################################
            ###################UNKOWN INTENT######################################
        else:
            #this is for an unrecognised intent
            result = "Please ask the right questions or statement"
    return result

def chatbot_response(msg):
    msg = msg.lower()
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
        return user_input

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

        

