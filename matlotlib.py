import re
import pandas as pd
import numpy as np
from io import StringIO
from collections import Counter
import matplotlib.pyplot as plt
from PIL import Image
import streamlit as st
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def date_time(s):
    pattern='^([0-9]+)(\/)([0-9]+)(\/)([0-9]+), ([0-9]+):([0-9]+)[ ]?(AM|PM|am|pm)? -'

    result=re.match(pattern, s)
    if result:
        return True
    return False 


def find_contact(s):
    s=s.split(":")
    if len(s)==2:
        return True
    else:
        return False
    
# Extract Message
def getMassage(line):
    splitline=line.split(' - ')
    datetime= splitline[0]
    date, time= datetime.split(', ')
    message=" ".join(splitline[1:])
    
    if find_contact(message):
        splitmessage=message.split(": ")
        author=splitmessage[0]
        message=splitmessage[1]
    else:
        author=None
    return date, time, author, message
    
def preprocess(a):
        
        data=[]
        collection='chat1.txt'
        with a as fp:

            fp.readline()
            messageBuffer=[]
            date, time, author= None, None, None
            while True:
                line=fp.readline()
                if not line:
                    break
                line=line.strip()
                if date_time(line):
                    if len(messageBuffer) >0:
                         data.append([date, time, author, ''.join(messageBuffer)])
                    messageBuffer.clear()
                    date, time, author, message=getMassage(line)
                    messageBuffer.append(message)
                else:
                    messageBuffer.append(line)
    
           


        df = pd.DataFrame(data, columns=["Date", 'Time', 'Contact', 'Message'])
        df['Date'] = pd.to_datetime(df['Date'])
        df["Month"] = df["Date"].dt.month
        df["MonthName "] = df["Date"].dt.month_name()
        df["Year"] = df["Date"].dt.year
        df["only_date"] = df['Date'].dt.date
        df['day_name'] = df['Date'].dt.day_name()
        
        data = df.dropna() 
        
        
        sentiments = SentimentIntensityAnalyzer()
        data["Positive"] = [sentiments.polarity_scores(i)["pos"] for i in data["Message"]]
        data["Negative"] = [sentiments.polarity_scores(i)["neg"] for i in data["Message"]]
        data["Neutral"] = [sentiments.polarity_scores(i)["neu"] for i in data["Message"]]
        x=sum(data["Positive"])
        y=sum(data["Negative"])
        z=sum(data["Neutral"])

        def score(a,b,c):
            if (a>b) and (a>c):
                return "Positive "
            if (b>a) and (b>c):
                return "Negative "
            if (c>a) and (c>b):
                return "Neutral"

       
        scr=score(x,y,z)
    



        return data,scr
       



   