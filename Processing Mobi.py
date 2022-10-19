from calendar import calendar
import email
from enum import auto
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


firestore_db = firestore.client()

#get user data
print("Please enter details")
ID_Num_User = input("ID Number: ")
Name_User = input("Name: ")
Surname_User = input("Surname: ")
Email_User = input("Email: ")
Phone_Num_User = input("Phone Number: ")
Med_Aid_User = input("Medical-Aid, yesor no? ")


#add user to db
user_doc_ref = firestore_db.collection(u'Patients').document(ID_Num_User)
user_doc_ref.set({
    u'ID Number' : ID_Num_User,
    u'Name': Name_User,
    u'Surname': Surname_User,
    u'Email' : Email_User,
    u'Phone Number': Phone_Num_User,
    u'Medical aid': Med_Aid_User

})


## deleting from db
# firestore_db.collection(u'Patients').document(u'new').delete()

##reading of db, testing
# patients_ref = firestore_db.collection(u'Patients')
# Patients_docs = patients_ref.stream()

# for doc in Patients_docs:
#     print(f'{doc.id} => {doc.to_dict()}')

##doctors_ref = firestore_db.collection(u'Doctors')
#Doctors_docs = doctors_ref.stream()

# for doc in Doctors_docs:
#     print(f'{doc.id} => {doc.to_dict()}')
    



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

def getResponse(ints, intents_json):
    #this is the function whos if statement must be modified for scheduling and rescheduling and booking and medical inquries
    #These functions work but im not sure cause my pc is acting up
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    #This is how we need to code the pop-ups but we need this whole entire function to save inputed data
    for i in list_of_intents:
        #Now we can add functions in the if statements that will take from the next user input
        if(i['tag']== 'booking' and i['tag']== tag):
            #needs calender and after will take user input through a function
            #Must check if date is not before today, if doctor will be availble and if time is fine
     
            import datetime
            import mysql.connector
            ''' ..*. 
            def avail_docs(date): 
                date=date.split()
                day = date[0]
                time = date[1]
                sql= """ SELECT  name, surname, specialization, DISTINCT office_phone, DISTINCT office_email FROM doctors, operational_days WHERE operation_type ='working' AND :time BETWEEN start_time AND end_time AND :day BETWEEN start_date AND end_date AND doctor_id = practice_num"""
                mycursor.execute(sql, {'date': date, 'time': time})
                pra_num = mycursor.fetchal()

            def doc_status(practice_num):
                sql= """ SELECT operation_type FROM operational_days WHERE doctor_id = :num"""
                mycursor.execute(sql, {'num': practice_num})
                doc_status = mycursor.fetchall()
                return doc_status

            def build_booking(doctor_num):
                select p.name, p.surname, booking_id, d.surname, start_date, end_date, reason
                from patients p,appointments a, doctors d
                where doctor_num = 

            def browse_booking():
                #all old bookings must be deleted after 4 hours 

              '''
    
            ''' ..*.      
            def validate_doc():
                #this takes the users input of the doctors name or surname or name and surname
                print('Mo: Please enter the surname of the doctor you want to book. e.g) "van der merwe" or "zulu"...')
                doc_input = input('You: ')
                sql= """ SELECT practice_num FROM doctors WHERE LOWER(surname) = :surname"""
                mycursor.execute(sql, {'surname': doc_input})
                pra_num = mycursor.fetchall()
                if len(pra_num.split())>1:
                    print('Mo: oooh seems like the is too many doctors who share that surname.\nPlease enter the name AND surname of the doctor for a more accurate response. \n If you dont know the following information please type "n" for next.')
                    doc_input = input('You: ')
                    if doc_input =='n' or doc_input == 'N':
                        print('Mo: please enter the doctors office email address to help my find your specific doctor.)
                        doc_input = input('You: ')
                        sql ="""SELEC practice_num FROM doctors WHERE LOWER(office_email = :email"""
                        mycursor.execute(sql, {'email': doc_input})
                        pra_num = mycursor.fetchall()
                        if len(pra_num.split())>1 or len(pra_num.split())<1:
                            print('Mo: Seems like i can not find the specific doctor in our system, I do apologies. \n Is there anything else i can help you with')
                            print('Mo: ' + chatbot_response(input('You: ') ))
                            break
                        else:
                            return pra_num
                    else:
                        doc_input = doc_input.split()
                        sql= """ SELECT practice_num FROM doctors WHERE LOWER(name) IN :surname AND LOWER(surname) IN :surname"""
                        mycursor.execute(sql, {'surname': doc_input})
                        pra_num = mycursor.fetchall()
                            if len(pra_num.split())>1 or len(pra_num.split())<1:
                                print('Mo: Seems like i can not find the specific doctor in our system, I do apologies. \n Is there anything else i can help you with')
                                print('Mo: ' + chatbot_response(input('You: ') ))
                                break
                            else:
                                return pra_num
                                break
                                
                elif len(pra_num.split())<1:
                    print('Mo: Sorry seems like we dont have such a doctor in our system. \n Is there anything else i can help you with.')
                    print('Mo: ' + chatbot_response(input('You: ') ))
                    break
                    #find option out
                else:
                    return pra_num
                    break
            '''   
            def check_date(user_date):
                right_date = False
                try:
                    datetime.datetime.strptime(user_date, '%Y/%m/%d %H:%M')
                    right_date = True
                except ValueError:
                    print('Mo: Incorrect date format please enter the date in the format: YYYY/MM/DD HH:MM, (e.g 2022/05/24:09:300)')
                    right_date=False
                
                return right_date
            correctDate = False
            print('Mo: Please be informed that we start booking from 08:00 - 17:00 \n We book based on the availability of the client, then we check the availability of the doctor then we book!!')
            print('Mo: What date would you like to book for\n Please enter the date in the format: YYYY/MM/DD HH:MM, for example 2022/05/24:09:30')
            while correctDate == False:
                book_date = input('You: ')
                correctDate = check_date(book_date)
            # result will me confirmation of booking
            print('Mo: Do you have a specific doctor you want to see whos in our system or \nWould you like me to display all the doctors available on your specific date ('+book_date+')')
            choice = False
            while choice==False:
                print('Mo: If you have a specific doctor please type "s" \nand if you would like to pick from available doctor on the day please type "d"')
                doctor_name=input('You: ')
                if doctor_name.lower() =='s' or doctor_name.lower() =='specific':
                    #validate_doc()
                    break
            break
        
        elif(i['tag']== 'cancel' and i['tag']== tag):
            #will use a function to determine if the is any booking anytime soon and will ask if you want to cancel this booking
            result = 'are you sure you want to cancel booking'
            break
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

# while True:
#     print('Mo: ' + chatbot_response(input('You: ') ))