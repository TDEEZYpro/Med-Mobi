from tabnanny import check
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

while True:
    print('Mo: ' + chatbot_response(input('You: ') ))