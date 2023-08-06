# Import Libraries
# print("Loading mental health detector...")
import re
from bs4 import BeautifulSoup
import string
import wordninja as wn
from nltk.stem import WordNetLemmatizer
from textblob import TextBlob
import pickle as pk
import os

path = os.path.abspath(os.path.dirname(__file__))

# Load TFIDF Vector For Feature Extraction from text purpose...
with open(f"{path}/TfIdf_Vectorizer.pk", "rb") as f:
    TfIdf_Vectorizer = pk.load(f)

# Load Model...
with open(f"{path}/svc_linear.pk", "rb") as f:
    svc_linear = pk.load(f)

# Declear Lemmatizer
lm = WordNetLemmatizer()

# Detect Mental Health Function
def detect_mental_health(sentence):

    # make smallercase
    sentence = sentence.lower()
        
    # remove emails
    sentence = re.sub(r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", '', sentence)

    # remove mentions
    sentence = re.sub(r"@[A-Za-z0-9]+","", sentence)
    
    # Remove html
    sentence = BeautifulSoup(sentence, 'html.parser').get_text().strip()
    
    # Remove URL
    sentence = re.sub(r'https?://\S+|www\.\S+', '', sentence)
        
    # Removing punctutation, string.punctuation in python consists of !"#$%&\'()*+,-./:;<=>?@[\\]^_
    sentence = sentence.translate(str.maketrans('', '', string.punctuation))
    
    # Remove non-alphabetic characters
    sentence = re.sub(r'[^a-zA-Z ]', '', sentence)

    # Spliting words into two meaningful word
    sentence = ' '.join(wn.split(str(sentence)))

    # Correct the sentence
    sentence =  str(TextBlob(sentence).correct())
    
    # decontracted
    
    ## specific
    sentence = re.sub(r"wont", "will not", sentence)
    sentence = re.sub(r"wouldnt", "would not", sentence)
    sentence = re.sub(r"shouldnt", "should not", sentence)
    sentence = re.sub(r"couldnt", "could not", sentence)
    sentence = re.sub(r"cudnt", "could not", sentence)
    sentence = re.sub(r"cant", "can not", sentence)
    sentence = re.sub(r"dont", "do not", sentence)
    sentence = re.sub(r"doesnt", "does not", sentence)
    sentence = re.sub(r"didnt", "did not", sentence)
    sentence = re.sub(r"wasnt", "was not", sentence)
    sentence = re.sub(r"werent", "were not", sentence)
    sentence = re.sub(r"havent", "have not", sentence)
    sentence = re.sub(r"hadnt", "had not", sentence)

    ## general
    sentence = re.sub(r"n\ t", " not", sentence)
    #sentence = re.sub(r"\re", " are", sentence)
    sentence = re.sub(r"\ s ", " is ", sentence) 
    sentence = re.sub(r"\ d ", " would ", sentence)
    sentence = re.sub(r"\ ll ", " will ", sentence)
    sentence = re.sub(r"\dunno", "do not ", sentence)
    sentence = re.sub(r"ive ", "i have ", sentence)
    sentence = re.sub(r"im ", "i am ", sentence)
    sentence = re.sub(r"i m ", "i am ", sentence)
    sentence = re.sub(r" w ", " with ", sentence)


    # Lemmatize
    snt = ' '.join([lm.lemmatize(i) for i in sentence.split()])
    
    return svc_linear.predict(TfIdf_Vectorizer.transform([snt]))[0]

detect_mental_health("I am very much happy today")

# print("Mental Health Detector Loaded...")