from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import emoji
import pandas as pd

extract=URLExtract()
def fetch_stats(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    num_messages=df.shape[0]
    words=[]
    for message in df['message']:
        words.extend(message.split())
    num_media_messages=df[df['message']=='<Media omitted>\n'].shape[0]
    links=[]
    for message in df['message']:
        links.extend(extract.find_urls(message))
    return num_messages,len(words),num_media_messages,len(links)
def monthly_timeline(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    timeline['time'] = time
    return timeline

def most_busy_users(df):
    filtered_df = df[df['user'] != 'group_notification']
    x=filtered_df['user'].value_counts().head()
    new_df = (round((filtered_df['user'].value_counts() / filtered_df.shape[0]) * 100, 2).reset_index()
              .rename(columns={'index': 'Name', 'user': 'Percent'}))
    return x,new_df
def create_wordcloud(selected_user,df):
    f=open('stop_hinglish.txt','r')
    stop_words=f.read()
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    temp=df[df['user']!='group_notification']
    temp=temp[temp['message']!='<Media omitted>\n']
    temp = temp[~temp['message'].str.contains('This message was deleted')]

    def remove_stop_words(message):
        y=[]
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc=WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    temp['message']=temp['message'].apply(remove_stop_words)
    df_wc=wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc
def most_common_words(selected_user,df):
    f=open('stop_hinglish.txt','r')#reading stop_hinglish words
    stop_words=f.read()
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    temp=df[df['user']!='group_notification']#preventing group notification messages
    temp=temp[temp['message']!='<Media omitted>\n']#preventing media messages
    temp = temp[~temp['message'].str.contains('This message was deleted')]#preventing deleted messages
    words=[]
    for message in temp['message']:#loop is passed for the message column in temp
        for word in message.lower().split():#the message is converted in lowercase and is splitted
            if word not in stop_words:#if the words are not stop words then append it in the "word" list
                words.append(word)
    most_common_df=pd.DataFrame(Counter(words).most_common(20))#"Counter" function helps to find how many times a paticular word is used i.e 20 in this case
    return most_common_df
def emoji_helper(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    emojis=[]
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])
    emoji_df=pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))#gives the no. of emoji counts
    return emoji_df
def daily_timeline(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    daily_timeline = df.groupby('only_date').count()['message'].reset_index()
    return daily_timeline
def week_activity_map(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    return df['day_name'].value_counts()
def month_activity_map(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    return df['month'].value_counts()
def activity_heatmap(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    user_heatmap=df.pivot_table(index='day_name',columns='period',values='message',aggfunc='count').fillna(0)
    return user_heatmap



