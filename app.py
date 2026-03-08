import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import preprocessor
import helper

st.sidebar.title("📊 WhatsApp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file", type=["txt"])

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    if df.empty:
        st.error("⚠ Chat file is empty or in incorrect format. Please check and re-upload.")
    else:
        user_list = df['user'].unique().tolist()
        user_list.sort()
        user_list.insert(0, "Overall")

        selected_user = st.sidebar.selectbox("Show analysis with respect to", user_list)

        if st.sidebar.button("Analyze"):
            num_messages, words, num_media, num_links = helper.fetch_stats(selected_user, df)

            st.subheader("🔢 Top Statistics")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Messages", num_messages)
            col2.metric("Total Words", words)
            col3.metric("Media Shared", num_media)
            col4.metric("Links Shared", num_links)

            # Monthly Timeline
            st.subheader("📅 Monthly Timeline")
            timeline = helper.monthly_timeline(selected_user, df)
            fig, ax = plt.subplots()
            ax.plot(timeline['month'], timeline['message_count'], marker='o', color='blue')
            plt.xticks(rotation=90)
            st.pyplot(fig)

            # Daily Timeline
            st.subheader("📆 Daily Timeline")
            daily_timeline = helper.daily_timeline(selected_user, df)
            fig, ax = plt.subplots()
            ax.plot(daily_timeline['date'], daily_timeline['message_count'], color='green')
            plt.xticks(rotation=90)
            st.pyplot(fig)

            # Activity Heatmap
            st.subheader("🔥 Activity Heatmap (Most Busy Days & Most Busy Months)")
            heatmap = helper.activity_heatmap(selected_user, df)
            fig, ax = plt.subplots()
            sns.heatmap(heatmap, annot=True, cmap="coolwarm", ax=ax)
            st.pyplot(fig)

            # Most Busy Users
            st.subheader("👥 Most Busy Users")
            most_busy = helper.most_busy_users(df)
            st.bar_chart(most_busy)

            # Word Cloud
            st.subheader("☁ Word Cloud")
            wordcloud = helper.create_wordcloud(selected_user, df)
            st.image(wordcloud.to_array())

            # Most Common Words
            st.subheader("📌 Most Common Words")
            common_words = helper.most_common_words(selected_user, df)
            st.table(common_words)

            # Emoji Analysis
            st.subheader("😊 Emoji Analysis")
            emoji_df = helper.emoji_analysis(selected_user, df)
            st.table(emoji_df)
