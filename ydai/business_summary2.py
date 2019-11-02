# -*- coding: utf-8 -*-
"""
Created on Sat Nov  2 04:09:20 2019

@author: ydai
"""
from nltk import FreqDist
def freq_words(x, terms = 30):
  all_words = ' '.join([text for text in x])
  all_words = all_words.split()

  fdist = FreqDist(all_words)
  words_df = pd.DataFrame({'word':list(fdist.keys()), 'count':list(fdist.values())})

  # selecting top 20 most frequent words
  d = words_df.nlargest(columns="count", n = terms)
#  plt.figure(figsize=(20,5))
#  ax = sns.barplot(data=d, x= "word", y = "count")
#  ax.set(ylabel = 'Count')
#  plt.show()
  return(d)
# function to remove stopwords
def remove_stopwords(rev):
    rev_new = [i for i in rev if i not in stop_words]
    return rev_new
from nltk.corpus import stopwords
stop_words = stopwords.words('english')
# business summary -> products
in_file = "D:/000 Yilin Resource/myStartUp/FinTech_NLP/SPY_StocksV2.xlsx"
import pandas as pd
in_data = pd.read_excel(in_file)

in_data['Comp_Des1']

import nltk
import pandas as pd
import re
import matplotlib.pyplot as plt
from gensim import corpora
import seaborn as sns
import DrawBox as dr

# identify company name
des_col_name = "Comp_Des1"
def run_feature_extraction(des_col_name):
    name_result = []
    for row_name,row_val in in_data.iterrows():
    #    row_val = in_data.iloc[233,]
        tmp_comp = row_val[des_col_name].split(".")[0].split("Corporation")[0].split(",")[0].split("Inc")[0].split(" is ")[0].split("Company")[0]
        tmp_comp = [x for x in tmp_comp.split(" ") if len(x)>0]
        tagged_wds = nltk.pos_tag(tmp_comp) 
        verbs = [idx for idx,(x,y) in enumerate(tagged_wds) if y[:2] == "VB"]
        if len(verbs)>0:
            if verbs[0]!=0:
                tmp_comp2 = " ".join(tmp_comp[:verbs[0]])
            else:
                tmp_comp2 = " ".join(tmp_comp)
        else:
            tmp_comp2 = " ".join(tmp_comp)
    #    if len(tmp_comp)>20:
    #        tmp_comp = tmp_comp[:30]
        name_result.append(tmp_comp2.strip())
    in_data["Company"] = name_result
    #    row_val["Comp_Des2"]    
    # identify useful verbs
    verb_result = []
    for row_name,row_val in in_data.iterrows():
    #    print(sen)
    #    row_val = in_data.iloc[1]
        words = [x for x in re.sub("[^a-zA-Z#]",' ',row_val[des_col_name]).split(" ") if len(x)>0]
        tagged_wds = nltk.pos_tag(words)
        sel_verbs1 = [(x.lower(),y) for x,y in tagged_wds if y=="VBP" or y=="VBZ"] 
        verb_result += sel_verbs1
    verbs = [x for x,y in verb_result]
    most_freq_verbs = freq_words(verbs, 100)
    
    
    import numpy as np
    key_verb_list = ['provides','offers',"develops","sells","distributes","produces","designs","manufactures","provide","generates","offer","delivers","commercializes",
                     "specializes","refines","operations","operates","serves","engages","processes","makes","focus","focuses","include","owns","manages"]
    key = 'provides'
    row_val = in_data.iloc[77]
    for key in key_verb_list:
        result1 = []
        for row_name,row_val in in_data.iterrows():
            if key in row_val[des_col_name]:
                tmp_list = row_val[des_col_name].split(".")
                tmp_product = []
                for x in tmp_list:
                    if key in x:
                        result_idx = x.find(key)
                        tmp_product.append(x[result_idx+len(key):].strip())
                tmp_prod = "|".join(tmp_product)
            else:
                tmp_prod = np.nan
            result1.append(tmp_prod)
        in_data[key] = result1
    
    #text = (" ".join(in_data["Comp_Des1"])).split(" ")
    #text2 = nltk.Text(text)
    #text2.concordance('provides')
    
    len(verbs)
    result = []
    for row_name,row_val in in_data.iterrows():
    #    print(sen)
        row_val = in_data.iloc[1]
        
        blockresult = []
        sentens = row_val[des_col_name].split(".")
        for i in range(0,len(sentens)):
            words = [x for x in re.sub("[^a-zA-Z#]",' ',sentens[i]).split(" ") if len(x)>0]
            tagged_wds = nltk.pos_tag(words)
            print(tagged_wds)   
            verbs = [idx for idx,(x,y) in enumerate(tagged_wds) if y[:2] == "VB"]
            if len(verbs)>0:
    #            print(words)
    #            assert(False)
                tmpstr = " ".join(words[verbs[0]:])
                blockresult.append([row_val['Company'],tmpstr])
        result += blockresult
    result_df = pd.DataFrame(result)
    coverage_rate = len(key_verb_list) - (in_data[key_verb_list]).isna().sum(axis=1)
    tmp_df = in_data[coverage_rate==0]
    
    # identify useful verbs
    verb_result = []
    for row_name,row_val in tmp_df.iterrows():
    #    print(sen)
    #    row_val = in_data.iloc[1]
        words = [x for x in re.sub("[^a-zA-Z#]",' ',row_val[des_col_name]).split(" ") if len(x)>0]
        tagged_wds = nltk.pos_tag(words)
        sel_verbs1 = [(x.lower(),y) for x,y in tagged_wds if y=="VBP" or y=="VBZ"] 
        verb_result += sel_verbs1
    verbs = set([x for x,y in verb_result])
    use_data = in_data[coverage_rate>0]
    return(use_data)
    
prod1 = run_feature_extraction("Comp_Des1").set_index("FS_Ticker")
prod2 = run_feature_extraction("Comp_Des2").set_index("FS_Ticker")
#prod1["BBG_Ticker","FS_Ticker"], 

prod_df = pd.concat([prod1[key_verb_list],prod2[key_verb_list]],axis=1)
key_prod= []
for row_name,row_val in prod_df.iterrows():
    all_strs = " ".join(row_val.dropna())
    words = [x for x in re.sub("[^a-zA-Z#]",' ',all_strs).split(" ") if len(x)>2 and x!="and"]
    kwords = freq_words(words, 20)
    tmp_prods = ",".join(kwords[kwords["count"]>1]["word"])
    key_prod.append(tmp_prods)
prod_df["key_prod"] = key_prod    
check_df = pd.concat([prod_df["key_prod"],prod1[["BBG_Ticker","Company"]]],axis=1)
check_df.to_excel("D:/000 Yilin Resource/myStartUp/FinTech_NLP/output1.xlsx")
#    d1 = sorted(set(words))
    
#    sel_verbs1 = [(x.lower(),y) for x,y in tagged_wds if y=="VBP" or y=="VBZ"] 
#    words2 = [x for x in re.sub("[^a-zA-Z#]",' ',row_val['Comp_Des2']).split(" ") if len(x)>2]
##    d2 = sorted(set(words))
#    tagged_wds2 = nltk.pos_tag(words2)
#    sel_verbs2 = [(x.lower(),y) for x,y in tagged_wds2 if y=="VBP" or y=="VBZ"] 
#
#    tmp_vbs = sorted(list(set([x for x,y in (sel_verbs1+sel_verbs2)])))
#    print(tmp_vbs)
#    print(words)
#    all_verbs += sel_verbs1
#    all_verbs += sel_verbs2
#verbs = sorted(set(all_verbs))
#    nltk.pos_tag(verbs)
#words_matrix_df = pd.concat(words_matrix,axis=1)          
                             