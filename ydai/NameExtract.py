# -*- coding: utf-8 -*-
"""
Created on Sat Nov  2 19:09:45 2019

@author: ydai
"""

# importing all the required modules
import PyPDF2

# find names in page 52 of report1
# find names in page 19 of report2
# creating an object 
result = []
file = open('D:/000 Yilin Resource/myStartUp/FinTech_NLP/ann_report1.pdf', 'rb')
# creating a pdf reader object
fileReader = PyPDF2.PdfFileReader(file)
# print the number of pages in pdf file
print(fileReader.numPages)

page1 = fileReader.getPage(52)
txt1 = page1.extractText()

import re
idxs = [m.start() for m in re.finditer("Beneficial", txt1)]
#    idx = txt1.find("Beneficial")
#    idx2 = txt1.rfind('Beneficial')
#    txt1.rfind('Beneficial')
#    txt1.rfind('Beneficial')
names =[]
for idx in idxs:
    name1 = txt1[idx-100:idx].split("\n")[-1]
    names.append(name1)

result.append(names)
# creating an object 
num_page = 19
file = open('D:/000 Yilin Resource/myStartUp/FinTech_NLP/ann_report2.pdf', 'rb')
fileReader = PyPDF2.PdfFileReader(file)
page1 = fileReader.getPage(num_page)
txt1 = page1.extractText()
import re
idxs = [m.start() for m in re.finditer("Beneficial", txt1)]
names =[]
for idx in idxs:
    name1 = txt1[idx-100:idx].split("\n")[-1]
    names.append(name1.split("%")[-1])
result.append(names)
num_page = 18
file = open('D:/000 Yilin Resource/myStartUp/FinTech_NLP/ann_report3.pdf', 'rb')
fileReader = PyPDF2.PdfFileReader(file)
page1 = fileReader.getPage(num_page)
txt1 = page1.extractText()

import re
idxs = [m.start() for m in re.finditer("beneficial", txt1)]
names =[]
for idx in idxs:
    name1 = txt1[idx-100:idx].split("\n")[-1]
    names.append(name1.split("%")[-1])
    
num_page = 22
file = open('D:/000 Yilin Resource/myStartUp/FinTech_NLP/ann_report3.pdf', 'rb')
fileReader = PyPDF2.PdfFileReader(file)
page1 = fileReader.getPage(num_page)
txt1 = page1.extractText()
idxs = [m.start() for m in re.finditer("Beneficial", txt1)]
for idx in idxs:
    name1 = txt1[idx-100:idx].strip().split("\n")[-1]
    names.append(name1.split("%")[-1])
result.append(names)