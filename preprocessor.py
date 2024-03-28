import re
import pandas as pd
def preprocess(data):
    pattern_12_hour = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[APap][Mm]\s-\s'
    pattern_24_hour = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    pattern_additional = r'\d{1,2}/\d{1,2}/\d{4},\s\d{1,2}:\d{2}\s[APap][Mm]\s-\s'

    matches_12_hour = re.findall(pattern_12_hour, data)
    matches_24_hour = re.findall(pattern_24_hour, data)
    matches_additional = re.findall(pattern_additional, data)

    if len(matches_12_hour) > len(matches_24_hour) and len(matches_12_hour) > len(matches_additional):
        pattern = pattern_12_hour
        date_format = '%m/%d/%y, %I:%M %p - '
    elif len(matches_24_hour) > len(matches_12_hour) and len(matches_24_hour) > len(matches_additional):
        pattern = pattern_24_hour
        date_format = '%m/%d/%y, %H:%M - '
    else:
        pattern = pattern_additional
        date_format = '%d/%m/%Y, %I:%M %p - '

    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    df['message_date'] = pd.to_datetime(df['message_date'],format=date_format)
    df.rename(columns={'message_date': 'date'}, inplace=True)

    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])
    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)
    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period=[]
    for hour in df[['day_name','hour']]['hour']:
        if hour==23:
            period.append(str(hour)+"-"+str('00'))
        elif hour==0:
            period.append(str('00')+"-"+str(hour+1))
        else:
            period.append(str(hour)+"-"+str(hour+1))
    df['period']=period
    return df

