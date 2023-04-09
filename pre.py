import re
import pandas as pd
import nltk
nltk.downloader.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def date_time(s):
    pattern='^([0-9]+)(\/)([0-9]+)(\/)([0-9]+), ([0-9]+):([0-9]+)[ ]?(AM|PM|am|pm)? -'
    pattern1='^([0-9]+)\/([0-9]+)\/([0-9]+),\s*([0-9]+):([0-9]+)\s*(AM|PM|am|pm)?\s*-\s*(.*)'
    result=re.match(pattern1, s)
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
        df["month_name "] = df["Date"].dt.month_name()
        df["Year"] = df["Date"].dt.year
        df["only_date"] = df['Date'].dt.date
        df['day_name'] = df['Date'].dt.day_name()
        
        data = df.dropna() 
        
        
        sentiments = SentimentIntensityAnalyzer()
        
     
        data["positive"] = [sentiments.polarity_scores(i)["pos"] for i in data["Message"]] # Positive
        data["negative"] = [sentiments.polarity_scores(i)["neg"] for i in data["Message"]] # Negative
        data["neutral"] = [sentiments.polarity_scores(i)["neu"] for i in data["Message"]] # Neutral
    
       
        def sentiment(d):
            if d["positive"] >= d["negative"] and d["positive"] >= d["neutral"]:
                return 1
            if d["negative"] >= d["positive"] and d["negative"] >= d["neutral"]:
                return -1
            if d["neutral"] >= d["positive"] and d["neutral"] >= d["negative"]:
                return 0

        data['value'] = data.apply(lambda row: sentiment(row), axis=1)

        x=sum(data["positive"])
        y=sum(data["negative"])
        z=sum(data["neutral"])

        def score(a,b,c):
            if (a>b) and (a>c):
                return "Positive "
            if (b>a) and (b>c):
                return "Negative "
            if (c>a) and (c>b):
                return "Neutral"

        
        scr=score(x,y,z)
        



        return data,scr
       



   