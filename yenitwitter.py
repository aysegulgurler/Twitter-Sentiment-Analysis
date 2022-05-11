import tweepy
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import nltk 
import re
from wordcloud import WordCloud, STOPWORDS
from PIL import Image
from langdetect import detect
from nltk.stem import SnowballStemmer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import CountVectorizer
from textblob import TextBlob
from os import kill, write
auth=tweepy.OAuthHandler("W5tN9EQDpxSUqGtOiNS2Ye79l","BANGXe8lqQQntLtJztfTtaNnSUE1VCZebFBjgIPSCRWY3M1Dk9")
auth.set_access_token("1193565741510995969-5RJnTZpmBarUTBygJKDUYMb1sjAJRb","8JhbWkqoM6hFSs6FQI5Hdffe5CVICNofXLJVyvV63coOh")
api=tweepy.API(auth)

def percentage(part,whole):
 return 100 * float(part)/float(whole)
keyword = input("Lütfen hesap adı veya hashtag giriniz:  ")
noOfTweet = int(input("Lütfen tweet sayısını giriniz:  "))
tweets = tweepy.Cursor(api.search, q=keyword).items(noOfTweet)
positive = 0
negative = 0
neutral = 0
polarity = 0
tweet_list = []
neutral_list = []
negative_list = []
positive_list = []
for tweet in tweets:
 
 print(tweet.text)
 tweet_list.append(tweet.text)
 analysis = TextBlob(tweet.text)
 score = SentimentIntensityAnalyzer().polarity_scores(tweet.text)
 neg = score['neg']
 neu = score['neu']
 pos = score['pos']
 comp = score['compound']
 polarity += analysis.sentiment.polarity
 
 if neg > pos:
  negative_list.append(tweet.text)
  negative += 1
 elif pos > neg:
  positive_list.append(tweet.text)
  positive += 1
 
 elif pos == neg:
  neutral_list.append(tweet.text)
  neutral += 1
positive = percentage(positive, noOfTweet)
negative = percentage(negative, noOfTweet)
neutral = percentage(neutral, noOfTweet)
polarity = percentage(polarity, noOfTweet)
positive = format(positive, ".1f")
negative = format(negative, ".1f")
neutral = format(neutral, ".1f")

neutral_list = pd.DataFrame(neutral_list)
negative_list = pd.DataFrame(negative_list)
positive_list = pd.DataFrame(positive_list)

print("toplam tweet: ",len(tweet_list))
print("pozitif tweet sayısı: ",len(positive_list))
print("negatif tweet sayısı: ", len(negative_list))
print("nötr tweet sayısı: ",len(neutral_list))


tw_list = pd.DataFrame(tweet_list)
tw_list["text"] = tw_list[0]

remove_rt = lambda x: re.sub('RT @\w+: '," ",x)
rt = lambda x: re.sub("@[^\w\.@-]", " ", x)
tw_list["text"] = tw_list.text.map(remove_rt).map(rt)
tw_list["text"] = tw_list.text.str.lower()
tw_list[["polarity", "subjectivity"]] = tw_list["text"].apply(lambda Text: pd.Series(TextBlob(Text).sentiment))
tw_list.head(10)
tw_list.drop_duplicates(inplace = True)

print("**********************************************************")
print(tw_list)
print("**********************************************************")


tw_list.to_csv('twitter.csv')
csvokunan = pd.read_csv("twitter.csv", encoding='UTF8')
csvokunan.to_excel("twitter.xlsx")
os.remove('twitter.csv')

labels = ["Pozitif ["+str(positive)+"%]" , "Nötr ["+str(neutral)+"%]","Negatif ["+str(negative)+"%]"]
sizes = [positive, neutral, negative]
colors = ["yellowgreen", "blue","red"]
patches, texts = plt.pie(sizes,colors=colors, startangle=90)
plt.style.use("default")
plt.legend(labels)
plt.title("Duygu Analizi Sonucu= "+keyword+"" )
plt.axis("equal")
plt.show()


