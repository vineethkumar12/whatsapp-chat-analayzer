from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

extract = URLExtract()

def fetch_stats(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['Contact'] == selected_user]

    # fetch the number of messages
    num_messages = df.shape[0]

    # fetch the total number of words
    words = []
    for message in df['Message']:
        words.extend(message.split())

    # fetch number of media messages
    num_media_messages = df[df['Message'] == '<Media omitted>\n'].shape[0]

    # fetch number of links shared
    links = []
    for message in df['Message']:
        links.extend(extract.find_urls(message))

    return num_messages,len(words),num_media_messages,len(links)
# fetching the most busy users in the chat file and that users returning to app file

def most_busy_users(df):
    x = df['Contact'].value_counts().head()
    df = round((df['Contact'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'Contact': 'percent'})
    return x,df
 
 # creating word cloud ant that words returning  to app file

def create_wordcloud(selected_user,df):

    f = open('stopwords.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['Contact'] == selected_user]

    temp = df[df['Contact'] != 'group_notification']
    temp = temp[temp['Message'] != '<Media omitted>\n']

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    temp['Message'] = temp['Message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['Message'].str.cat(sep=" "))
    return df_wc
# calculating percentage of positive ,negative and neutral sentiment of users messages and that returning to app file percentage funcnction 

def percentage(df,k):
    df = round((df['Contact'][df['value']==k].value_counts() / df[df['value']==k].shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'Contact': 'percent'})
    return df
# most common words are used in the chat file, that words are fetching and returning to app file most common words function
def most_common_words(selected_user,df):

    f = open('stopwords.txt','r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['Contact'] == selected_user]

    temp = df[df['Contact'] != 'group_notification']
    temp = temp[temp['Message'] != '<Media omitted>\n']

    words = []

    for message in temp['Message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df
# collecting number of emojis  in the chat file and that returning to app file  emoji helper fuction

def emoji_helper(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['Contact'] == selected_user]

    emojis = []
    for message in df['Message']:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df

  # daily time line of users

def daily_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['Contact'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['Message'].reset_index()

    return daily_timeline
  # calculating most busy day according 
def week_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['Contact'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['Contact'] == selected_user]

    return df['Month'].value_counts()
