'''import opennre
model = opennre.get_model('wiki80_cnn_softmax')
result = model.infer({'text': 'The car cause the traffic jam outside my home', 'h': {'pos': (4, 7)}, 't': {'pos': (18, 29)}})
print(result)
test = 'The car cause the traffic jam outside my home'
print(test[:20])'''

def append_to_csv(items, file):
    with open(file, 'a', newline="", encoding="utf-8") as fp:
        writer = csv.writer(fp)
        for item in items:
            writer.writerow(item)

def save_to_csv(items, file):
    with open(file, "w+", newline="", encoding="utf-8") as fp:
        writer = csv.writer(fp)
        for item in items:
            writer.writerow(item)


# Read pdf into text
import PyPDF2
file = open('ann_report1.pdf', 'rb')
fileReader = PyPDF2.PdfFileReader(file)

text = ""
for i in range(fileReader.numPages):
    page = fileReader.getPage(i)
    page = page.extractText()
    text = text + page
    text = text.replace('\n',' ')
print(text)
print("Length of text: " + str(len(text)))

# Name entity recognition
import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm

nlp = en_core_web_sm.load()
whole_list = [(X.text, X.label_) for X in nlp(text).ents]

# Extract ORG only, PERSON only, ORG and PERSON
org_list = []
for word in whole_list:
    if word[1] == 'ORG':
        org_list.append(word[0].strip())
        
person_list = []
for word in whole_list:
    if word[1] == 'PERSON':
        person_list.append(word[0].strip())

both_list = []
for word in whole_list:
    if word[1] == 'ORG' or word[1] == 'PERSON':
        both_list.append(word[0].strip())
        
print("org_list: " + str(org_list))
print("person_list: " + str(person_list))
print("both_list: " + str(both_list))

# Find the positions of words and turn into dictionary
org_dict = []
for word in org_list:
    position = {'pos':(text.find(word), text.find(word) + len(word))}
    org_dict.append({word:position})

person_dict = []
for word in person_list:
    position = {'pos':(text.find(word), text.find(word) + len(word))}
    person_dict.append({word:position})

both_dict = []
for word in both_list:
    position = {'pos':(text.find(word), text.find(word) + len(word))}
    both_dict.append({word:position})

print("org_dict: " + str(org_dict))
print("person_dict: " + str(person_dict))
print("both_dict: " + str(both_dict))

#for i in range(40):
    #print(text[27555+i])

# Relationship extraction
import opennre
model = opennre.get_model('wiki80_cnn_softmax')

result = []
subsidiary_list = []
for i in range(len(org_dict)):
    for j in range(5):
        if i + j + 1 == len(org_dict):
            break
        else:
            one_result = []
            decision = model.infer({'text': text[org_dict[i][org_list[i]]['pos'][0]:org_dict[i + j + 1][org_list[i + j + 1]]['pos'][1]], 'h': org_dict[i][org_list[i]], 't': org_dict[i + j + 1][org_list[i + j + 1]]})
            
            one_result.append(org_list[i])
            one_result.append(org_list[i + j + 1])
            one_result.append(decision)
            result.append(one_result)
            
            # Get subsidiary
            if decision[0] == 'subsidiary':
                subsidiary = []
                subsidiary.append(org_list[i])
                subsidiary.append(org_list[i + j + 1])
                subsidiary.append(decision)
                subsidiary_list.append(subsidiary)

print("result: " + str(result))
print("subsidiary_list: " + str(subsidiary_list))

import csv
save_to_csv(result, "all_relation.csv")
save_to_csv(subsidiary_list, "subsidiary_relation.csv")

'''
import opennre
model = opennre.get_model('wiki80_cnn_softmax')
result = model.infer({'text': 'He was the son of Máel Dúin mac Máele Fithrich, and grandson of the high king Áed Uaridnach (died 612).', 'h': {'pos': (18, 46)}, 't': {'pos': (78, 91)}})
print(result)
'''
