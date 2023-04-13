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
    
           


        df = pd.DataFrame(data, columns=["Date", 'Time', 'Contact', 'Message'])# the framing data initilizing to df variable 
        df["Date"] = pd.to_datetime(df["Date"])
        df["month_name "] = df["Date"].dt.month_name()# # fetching the monthname from Date column  in df list and that monthname passing to newcolumn Month
        df['day_name'] = df["Date"].dt.day_name()# fetching the dayname from Date column  in df list and that dayname passing to newcolumn day_name
        df["Month"] = df["Date"].dt.month.astype('int64') # # fetching the monthnumber from Date column  in df list and that monthnumber passing to newcolumn Month
        df["Year"] = df["Date"].dt.year.astype('int64') # fetching the year from Date column  in df list and that year passing to newcolumn Year
        df["only_date"] = df["Date"].dt.date# fetching the Date from Date column  in df list and that date passing to newcolumn only_date
        df["Date"] = df["Date"].dt.date         # fetching the Date from Date column  in df list and that date passing to newcolumn Date

        data = df.dropna() 
        
        
        sentiments = SentimentIntensityAnalyzer()
        
        data1 = data.copy()
        data1.loc[:, 'positive'] = [sentiments.polarity_scores(i)["pos"] for i in data1["Message"]]#neutral
        data1.loc[:, 'negative'] = [sentiments.polarity_scores(i)["neg"] for i in data1["Message"]] # Negative
        data1.loc[:, 'neutral'] = [sentiments.polarity_scores(i)["neu"] for i in data1["Message"]] # Neutral
    
       # calculating overall sentiment and that overall sentiment returning as for positive is 1, negative is -1, neutral is 0
        def sentiment(d):
            if d["positive"] >= d["negative"] and d["positive"] >= d["neutral"]:
                return 1
            if d["negative"] >= d["positive"] and d["negative"] >= d["neutral"]:
                return -1
            if d["neutral"] >= d["positive"] and d["neutral"] >= d["negative"]:
                return 0

        data1.loc[:,'value'] = data1.apply(lambda row: sentiment(row), axis=1)

        x=sum(data1["positive"]) # summation of all values of positive column
        y=sum(data1["negative"])# summation of all values of negative column
        z=sum(data1["neutral"])# summation of all values of neitral column

        def score(a,b,c):
            if (a>b) and (a>c):
                return "Positive "
            if (b>a) and (b>c):
                return "Negative "
            if (c>a) and (c>b):
                return "Neutral"

        
        scr=score(x,y,z)
        



        return data1,scr
       



   