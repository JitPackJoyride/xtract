# -*- coding: utf-8 -*-
"""
Created on Sat Nov  2 10:28:09 2019

@author: ydai
"""

# presnetation
# cloud of words
import nltk
import pandas as pd

data_df = pd.read_excel("D:/000 Yilin Resource/myStartUp/FinTech_NLP/output1.xlsx")

data_df2 = data_df[["key_prod","Sector"]]
from wordcloud import WordCloud, STOPWORDS 
stopwords = set(STOPWORDS.words("english")) 

for gp_name,gp_vals in data_df2.groupby("Sector"):
    words = (",".join(gp_vals['key_prod'].dropna())).split(",")
#    freq_words(words, terms = 30)
    wordcloud = WordCloud(max_font_size=50, max_words=100,  background_color="white").generate(" ".join(words))
    plt.figure()
    plt.title(gp_name)
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("on")
    plt.show()

for gp_name,gp_vals in data_df2.groupby("Sector"):
    words = (",".join(gp_vals['key_prod'].dropna())).split(",")
    d1 = freq_words(words, terms = 30)

################################################################################
# mapping from words to Sectors
from sklearn.feature_extraction.text import CountVectorizer
count_vect = CountVectorizer()
for gp_name,gp_vals in data_df2.groupby("Sector"):
    
Y = as.factor(data_df2["Sector"])
X = data_df2["key_prod"]
for x in data_df2["key_prod"]:
    print(len(x))
    
split_wds = [x.split(",") if isinstance(x,str) else np.nan for x in data_df2["key_prod"]]



x.split(",")

data_df3 = data_df2.dropna()
X_train_counts = count_vect.fit_transform(data_df3.key_prod)
X_train_counts.shape

from sklearn.datasets import fetch_20newsgroups
twenty_train = fetch_20newsgroups(subset='train', shuffle=True)


from sklearn.feature_extraction.text import TfidfTransformer
tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
X_train_tfidf.shape


    words = (",".join(gp_vals['key_prod'].dropna())).split(",")
    break

from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score
from sklearn.multiclass import OneVsRestClassifier

from sklearn.naive_bayes import MultinomialNB
clf = MultinomialNB().fit(X_train_tfidf, twenty_train.target)

OneVsRestClassifier(LogisticRegression(solver='sag'), n_jobs=-1))

    