from nltk.sentiment import SentimentIntensityAnalyzer

def get_sentiment(text):
    sia = SentimentIntensityAnalyzer()
    score = sia.polarity_scores(text)
    return score['compound']

