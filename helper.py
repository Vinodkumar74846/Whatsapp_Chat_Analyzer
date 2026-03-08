import pandas as pd
import emoji
from collections import Counter
from wordcloud import WordCloud



# Fetch basic statistics
def fetch_stats(user, df):
    if user != "Overall":
        df = df[df['user'] == user]

    num_messages = df.shape[0]
    words = df['message'].apply(lambda x: len(x.split())).sum()
    num_media = df[df['message'] == '<Media omitted>'].shape[0]
    num_links = df['message'].apply(lambda x: x.count("http")).sum()

    return num_messages, words, num_media, num_links

# Monthly Timeline
def monthly_timeline(user, df):
    if user != "Overall":
        df = df[df['user'] == user]

    df['month'] = df['datetime'].dt.to_period("M").astype(str)
    timeline = df.groupby('month')['message'].count().reset_index()
    timeline.rename(columns={'message': 'message_count'}, inplace=True)

    return timeline

# Daily Timeline
def daily_timeline(user, df):
    if user != "Overall":
        df = df[df['user'] == user]

    df['date'] = df['datetime'].dt.date
    daily_counts = df.groupby('date')['message'].count().reset_index()
    daily_counts.rename(columns={'message': 'message_count'}, inplace=True)

    return daily_counts


# Activity Heatmap
def activity_heatmap(user, df):
    if user != "Overall":
        df = df[df['user'] == user]

    df['day'] = df['datetime'].dt.day_name()
    heatmap = df.groupby('day')['message'].count().reset_index()
    heatmap.rename(columns={'message': 'message_count'}, inplace=True)

    return heatmap.pivot(index='day', columns='message_count', values='message_count').fillna(0)


# Most Busy Users
def most_busy_users(df):
    return df['user'].value_counts().head(5)


# Create Word Cloud
def create_wordcloud(user, df):
    if user != "Overall":
        df = df[df['user'] == user]

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white').generate(" ".join(df['message']))
    return wc


# Most Common Words
def most_common_words(user, df):
    if user != "Overall":
        df = df[df['user'] == user]

    words = " ".join(df['message']).split()
    common_words = pd.DataFrame(Counter(words).most_common(10), columns=['Word', 'Count'])

    return common_words


# Emoji Analysis
def emoji_analysis(user, df):
    if user != "Overall":
        df = df[df['user'] == user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(10), columns=['Emoji', 'Count'])

    return emoji_df
