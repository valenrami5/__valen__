import os
import string
from nltk.corpus import stopwords
from collections import OrderedDict
import re
import numpy as np
import dataframe_image as dfi

#Path with the words bank
path='/home/valentina/SOFKA/raw_texts'

#Open all the .txt and create a new file called merge

inputs = []
for file in os.listdir(path):
    if file.endswith(".txt"):
        inputs.append(os.path.join(path, file))
with open('merged_file.txt', 'w') as outfile:
    for fname in inputs:
        with open(fname, encoding="utf-8", errors='ignore') as infile:
            for line in infile:
                outfile.write(line)
#Reading the text

filename = 'merged_file.txt'
file = open(filename, 'rt')
text = file.read()
file.close()

#Removing some accents.

text=re.sub('á', 'a', text)
text=re.sub('é', 'e', text)
text=re.sub('í', 'i', text)
text=re.sub('ó', 'o', text)
text=re.sub('ú', 'u', text)

# Changing characters for space

text_without_characters= re.sub('[\-\/\(\)\)\[\]\'\"\:\;\,\.\n]', ' ', text)

#Just making sure that we remove most of the characters.

text_without_characters=re.sub('['+string.punctuation+']', ' ', text_without_characters)

#Now we want to extract the letters of the spanish alphabeth

text_letter_spanish = list(re.findall('[\s]*([A-Za-zñ]{4,100})[\s]*', text_without_characters))

#Removing Stop words

stop_words = stopwords.words('spanish')
text_without_stopwords = [w for w in text_letter_spanish if not w in stop_words]

#Removing words with more than two UpperCases

text_without_uppercase =[letter for letter in text_without_stopwords if len(re.findall('[A-Z]', letter))<=1]

#Converting all the remaining words in lowercase

text_lowercase = [letter.lower() for letter in text_without_uppercase]

#Removing duplicates

words_bank = list(OrderedDict.fromkeys(text_lowercase))

#Converting the list into a csv

np.savetxt("words_bank.csv", words_bank, delimiter=", ", fmt="%s")


print(len(words_bank))