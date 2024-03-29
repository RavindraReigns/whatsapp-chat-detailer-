import streamlit as st
import helper
import preprocessor
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="WhatsApp Chat Detailer",page_icon=":chart_with_upwards_trend:")

st.sidebar.title("WhatsApp Chat Detailer")

guide_message="""
## Welcome to WhatsApp Chat Detailer                                                   

##### Quick Steps to Analyze your Chat Data:

###### 1. Export 

- Open the WhatsApp chat you wish to analyze.
- Tap the three-dot menu icon in the top-right corner.
- Select "More" > "Export chat" > "Without media".
- Save the exported .txt file in the file system.
- Exporting Group chat make take little while to initialize.

###### 2. Upload 

- Click on the "Browse files" button on the left side of this page.
- Select the exported .txt file from the file system.

###### 3. Analyze 

- After uploading the file, select the user or group chat from the dropdown menu with respect to whom you want the analysis.
- Click on the "Show Analysis" button to view detailed statistics, timelines and visualizations.

##### Note:

- Prefer switching to desktop mode when opening this web app on phone.
- Zip file is not valid, make sure to extract it before uploading.
- Group chat analysis may take few seconds depending on the chat data. 

"""
guide_placeholder=st.empty()
guide_placeholder.markdown(guide_message)
uploaded_file = st.sidebar.file_uploader("Choose a file")

if uploaded_file is not None:
    if uploaded_file.name.lower().endswith('.txt'):
        data = uploaded_file.getvalue().decode("utf-8")
        if " - " in data and ": " in data:
            df=preprocessor.preprocess(data)
            user_list=df['user'].unique().tolist()
            user_list.remove('group_notification')
            user_list.sort()
            user_list.insert(0,"Overall")

            selected_user=st.sidebar.selectbox("Show Analysis for:",user_list)

            if st.sidebar.button("Show Analysis"):
                guide_placeholder.empty()
                num_messages, words, num_media_messages, num_links= helper.fetch_stats(selected_user,df)
                st.title("Top Statistics")
                col1,col2,col3,col4=st.columns(4)
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

                st.title("Monthly Timeline")
                monthly_timeline=helper.monthly_timeline(selected_user,df)
                fig,ax=plt.subplots()
                ax.plot(monthly_timeline['time'],monthly_timeline['message'],color="green")
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

                st.title("Daily Timeline")
                daily_timeline = helper.daily_timeline(selected_user, df)
                fig, ax = plt.subplots()
                ax.plot(daily_timeline['only_date'], daily_timeline['message'], color="black")
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

                st.title("Activity Map")
                col1, col2 = st.columns(2)
                with col1:
                    st.header('Most Busy Day')
                    busy_day = helper.week_activity_map(selected_user, df)
                    fig, ax = plt.subplots()
                    ax.bar(busy_day.index, busy_day.values)
                    plt.xticks(rotation='vertical')
                    st.pyplot(fig)
                with col2:
                    st.header('Most Busy Month')
                    busy_month = helper.month_activity_map(selected_user, df)
                    fig, ax = plt.subplots()
                    ax.bar(busy_month.index, busy_month.values, color='orange')
                    plt.xticks(rotation='vertical')
                    st.pyplot(fig)

                st.title('Weekly Activity Map')
                user_heatmap = helper.activity_heatmap(selected_user, df)
                fig, ax = plt.subplots()
                ax = sns.heatmap(user_heatmap)
                st.pyplot(fig)

                if selected_user=='Overall':
                    st.title('Most Busy Users')
                    x,new_df=helper.most_busy_users(df)
                    fig,ax=plt.subplots()
                    col1,col2=st.columns(2)
                    with col1:
                        ax.bar(x.index,x.values,color='red')
                        plt.xticks(rotation='vertical')
                        st.pyplot(fig)
                    with col2:
                        st.dataframe(new_df)
                else:
                    st.title('Most Active Users')
                    st.markdown("<p style='font-size:24px;'>This analysis is only applicable"
                                " for Overall Users and not for a specific user!!!</p>", unsafe_allow_html=True)

                st.title("WordCloud")
                df_wc=helper.create_wordcloud(selected_user,df)
                fig,ax=plt.subplots()
                ax.imshow(df_wc)
                st.pyplot(fig)

                st.title('Most Common Words')
                most_common_df=helper.most_common_words(selected_user,df)
                fig,ax=plt.subplots()
                ax.barh(most_common_df[0],most_common_df[1])
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

                emoji_df=helper.emoji_helper(selected_user,df)
                if emoji_df.empty and selected_user=="Overall":
                    st.title("Emoji Analysis")
                    st.markdown("<p style='font-size:30px;'>No emoji has been sent among this chat!!!</p>",
                                unsafe_allow_html=True)
                elif emoji_df.empty and selected_user!="Overall":
                    st.title("Emoji Analysis")
                    st.markdown(f"<p style='font-size:30px;'>{selected_user} has not sent any emoji!!!</p>",
                                unsafe_allow_html=True)
                else:
                    st.title("Emoji Analysis")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.dataframe(emoji_df)
                    with col2:
                        fig, ax = plt.subplots()
                        ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f")#autopct gives the percentage
                        st.pyplot(fig)

        else:
            st.markdown("<p style='font-size:30px; color:red; font-family:Times New Roman;'>The uploaded text does not appear to be in a valid chat format.Please upload a file containing chat messages in a valid '.txt' format!!!</p>",unsafe_allow_html=True)

    else:
        st.markdown("<p style='font-size:30px; color:red; font-family:Times New Roman;'>This is not a valid chat format! Please upload a valid '.txt' chat format!!!</p>",unsafe_allow_html=True)





