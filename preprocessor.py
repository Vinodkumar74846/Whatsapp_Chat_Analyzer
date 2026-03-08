import re
import pandas as pd
#import nltk
#from nltk.corpus import stopwords
#from nltk.tokenize import word_tokenize


#nltk.download('stopwords')
#nltk.download('punkt')

def preprocess(data):
    pattern = r'(\d{1,2}/\d{1,2}/\d{2,4}, \d{1,2}:\d{2} [APap][Mm]) - (.*?): (.*)'
    messages = re.findall(pattern, data)

    if not messages:
        return pd.DataFrame()

    df = pd.DataFrame(messages, columns=['datetime', 'user', 'message'])
    df['datetime'] = pd.to_datetime(df['datetime'], format='%m/%d/%y, %I:%M %p')

    #stop_words = set(stopwords.words('english'))
   # df['clean_message'] = df['message'].apply(
      #  lambda x: " ".join([word for word in word_tokenize(x) if word.lower() not in stop_words]))

    return df
