import streamlit as st
import pre

from io import StringIO
import helper
import matplotlib.pyplot as plt
from PIL import Image
st.sidebar.title("whatsapp chat analyzer")
docx_file = st.sidebar.file_uploader("Upload Document") 
a=False
if docx_file is not None:
   bytes_data=docx_file.getvalue()
   file_like_object = StringIO(bytes_data.decode("utf-8"))
   data,scr = pre.preprocess(file_like_object)
   st.dataframe(data) #displaying the chat data in different columns in streamlit
	   
   # getting  unique users
   user_list = data['Contact'].unique().tolist()
   
   imagename=scr+".jpg"

   image = Image.open(imagename)

   user_list.sort()
   user_list.insert(0,"Overall")
   selected_user = st.sidebar.selectbox("Show analysis wrt",user_list)
   

   if st.sidebar.button("Show Analysis"):
        st.subheader("Overall Sentiment is")
        st.subheader(scr)
        image=image.resize((110,90))
        st.image(image)
        a=True
        # Stats Area
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user,data)
        st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)
        with col4:
            st.header("Links Shared")
            st.title(num_links)
if a:
    if selected_user == 'Overall':
            # its generate most buy users in graphically

            st.title('Most Busy Users')
            x,new_df = helper.most_busy_users(data)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)
            col3,col4,col5= st.columns(3)

            with col1:
                ax.bar(x.index, x.values,color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)
            with col3:
                st.markdown("<h3 style='text-align: center; color: white;'>Most Positive Contribution</h3>",unsafe_allow_html=True)
                x = helper.percentage(data,1)
                st.dataframe(x)
            with col4:
                st.markdown("<h3 style='text-align: center; color: white;'>Most Neutral Contribution</h3>",unsafe_allow_html=True)
                y = helper.percentage(data, 0)
                st.dataframe(y)
            with col5:
                st.markdown("<h3 style='text-align: center; color: white;'>Most Negative Contribution</h3>",unsafe_allow_html=True)
                z = helper.percentage(data, -1)    
                st.dataframe(z)
    # its generate word cloud

    st.title("Wordcloud")
    df_wc = helper.create_wordcloud(selected_user,data)
    fig,ax = plt.subplots()
    ax.imshow(df_wc)
    st.pyplot(fig)
    most_common_df = helper.most_common_words(selected_user,data)

    fig,ax = plt.subplots()

    ax.barh(most_common_df[0],most_common_df[1])
    plt.xticks(rotation='vertical')

   # its generate collection of most common words used in the chat

    st.title('Most commmon words')
    st.pyplot(fig)
    emoji_df = helper.emoji_helper(selected_user,data)
    st.title("Emoji Analysis")

    col1,col2 = st.columns(2)

    with col1:
            st.dataframe(emoji_df)
    with col2:
            fig,ax = plt.subplots()
            ax.pie(emoji_df[1].head(),labels=emoji_df[1].head(),autopct="%0.2f")
            st.pyplot(fig)

    #generate dailt timeline graph

    st.title("Daily Timeline")
    daily_timeline = helper.daily_timeline(selected_user, data)
    fig, ax = plt.subplots()
    ax.plot(daily_timeline['only_date'], daily_timeline['Message'], color='black')
    plt.xticks(rotation='vertical')
    st.pyplot(fig)
    st.title('Activity Map')
    col1,col2 = st.columns(2)

    with col1:
        # its generate most busy day in graphically

        st.header("Most busy day")
        busy_day = helper.week_activity_map(selected_user,data)
        fig,ax = plt.subplots()
        ax.bar(busy_day.index,busy_day.values,color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
    with col2:
        # its generate most busy month in graphically

        st.header("Most busy month")
        busy_month = helper.month_activity_map(selected_user, data)
        fig, ax = plt.subplots()
    
        ax.bar(busy_month.index, busy_month.values,color='blue')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)