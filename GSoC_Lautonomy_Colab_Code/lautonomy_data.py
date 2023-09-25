# -*- coding: utf-8 -*-
"""Lautonomy Data.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/16h2nkBkdmvpOJL1U7-AJ6BU3eeCpH6YX

# **Intro: Loading Data and Tokenizing**
Here we load the raw data and prepare it for analysis. This includes


*   Removing non-ascii characters
*   Changing all characters to lowercase
*   Eliminating all numbers
*   Removing all punctuation
"""

import pandas as pd
import numpy as np
import re

df = pd.read_csv('/content/unres_docs_raw_text.csv')
df = df.dropna(subset=['text', 'date']).reset_index()
df_clean = df

df

df['session_id'].unique()

df['date'].unique()

import string
from string import digits
'''
Tokenizing and cleaning the raw text
'''
for i in range(0, len(df['text'])):
    temp = re.sub(r'[^\x00-\x7F]+','', df['text'][i]).split()
    temp = [''.join(i for i in x if not i.isdigit()) for x in temp]
    temp = [''.join(c for c in s if c not in string.punctuation) for s in temp] # remove all punctuation
    temp = [x.lower() for x in temp] # make everything lower case
    temp = list(filter(None, temp))
    df['text'][i] = temp

import itertools
a = df['text']
all_words = list(set(list(itertools.chain.from_iterable(a))))
len(all_words)

# 3 million words -> 14k when we remove duplicates!!

"""# **Creating the meta-main.txt file**
Here we simply create a txt file whose first line contains 0 and all lines below contain the word index and the word itself.
"""

with open('meta-mai-3n.txt', 'w') as the_file:
    the_file.write('0\n')
    for i in range(0, len(all_words)):
        the_file.write(str(i) + ' ' + all_words[i] + '\n')

"""# **Preparing to Compute the 3D Embedding**
In this section, we format the data to plus it into the Clip as Service (CAS) tool, which uses the CLiP model to embed our data into a 512 dimensional space.

Then, we use UMAP to embed this into a 3 dimensional space, and send those coordinates into Polyglot.
"""

filename = "/content/embeddings.csv"
with open(filename, "r") as fic:
    content = fic.read().replace('\n', ' ')
    content = content.replace('\",\"', '\"')

sentences = list(map(str.strip, content.split("\"")))
len(sentences)

# drop first and last rows
del sentences[-1]
del sentences[0]

sentences[2]

for i in range(0, len(sentences)):
    sentences[i] = eval(re.sub("\d\s+", ",", sentences[i]))

for i in range(0, len(sentences)):
    if len(sentences[i]) != 512:
        print('oops')

sentences[0:1]

df = pd.DataFrame(sentences)

df

# df.to_csv('embedding_df.csv')
# !cp embedding_df.csv "/content/drive/MyDrive"

"""# **UMAP Embedding to 3D**
Here we use UMAP to reduce the dimensionality of the CLiP embedding to only 3.
"""

!pip install umap-learn
import umap

clip_embed = pd.read_csv('/content/embedding_df.csv')
clip_embed

clip_embed.reset_index(drop=True, inplace=True)
del clip_embed['Unnamed: 0']

raw_embeddings = clip_embed[[str(x) for x in range(0, 512)]].values

reducer = umap.UMAP(n_components=3, n_neighbors = 6, n_epochs = 20000, init = "spectral", densmap = True, dens_lambda = 4)
embedding = reducer.fit_transform(raw_embeddings)
embedding.shape

three_d = pd.DataFrame(embedding)
three_d

three_d_embedding.to_csv('three_dim_embed.csv')

"""# **Computing Similarity Metrics**
Here we need to compute a temporary distance metric (until PolyPhy is ready). We will use the Euclidean distance metric.
"""

three_d = pd.read_csv('/content/three_dim_embed.csv')

'''
To choose anchor points, we look for those words with the highest if-idf scores
We will choose the 200 highest scoring words
'''
years = pd.read_csv('/content/if_idf_scores_fill_with_zeros.csv')
years = years.iloc[:, ::-1]
first_cols = ['polyglot_index','word']
last_cols = [col for col in years.columns if col not in first_cols]
years = years[first_cols+last_cols]
years
#temp1.join(temp_years)
#years['max_if_idf'] = years.iloc[:, 2:].max(axis=1)
#years

years.to_csv('years_fixed.csv', index = False)

years['max_if_idf'] = years.iloc[:, 2:].max(axis=1)

years.sort_values(['max_if_idf'], ascending=False).head(400)

anchor_points = years.sort_values(['max_if_idf'], ascending=False).head(400).index.tolist()

three_d.drop("Unnamed: 0", axis = 1, inplace = True)

three_d

three_d.loc[1,:].tolist()

euclidean_sim_list = [[] * i for i in range(0, len(anchor_points))]
len(euclidean_sim_list)

anchor_points

'''
Computing the Euclidean similarities
'''
from numpy import dot
from numpy.linalg import norm
count = 0
for point in anchor_points:
    anchor = np.asarray(three_d.loc[point,:].tolist(), dtype=np.float32)
    for index in range(0, 14654):
        other = np.asarray(three_d.loc[index,:].tolist(), dtype=np.float32)
        euclidean_sim = np.linalg.norm(anchor-other, ord = 2)
        euclidean_sim_list[count].append(euclidean_sim)
    count += 1

euclidean_sim_list[0][3383]

euc_scores = pd.DataFrame(euclidean_sim_list)

euc_scores.iloc[:, :].max(axis=1).tolist()

import math

temp_euc_list = euclidean_sim_list.copy()
for i in range(0, len(anchor_points)):
    for j in range(0, 14654):
        temp_euc_list[i][j] = 1000/math.exp(euclidean_sim_list[i][j])

inv_euc = pd.DataFrame(temp_euc_list)
inv_euc.iloc[:, :].max(axis=1).tolist()

inv_euc

anchor_points[0]
euclidean_sim_list[0][3383].sort()

# temp
temp.sort_values([0], ascending=False).head(200)
temp.iloc[3383,:]
#len(euclidean_sim_list[0])

import os
!mkdir updatedAnchorsFINAL2
os.chdir('updatedAnchorsFINAL2')
!pwd

temp_euc_list[0][3383]

os.chdir('..')
!pwd

from google.colab import files
from numpy import inf
count = 0
for anchor in anchor_points:
    temp = pd.DataFrame(temp_euc_list[count]).sort_values([0], ascending=False)
    temp.to_csv(str(anchor) + '.txt', header=False)
    files.download(str(anchor) + '.txt')
    count += 1

!cp -r "updatedAnchorsFINAL2" "drive/MyDrive/"

"""# **Creating the full_data file**
Here we must specify the 3D coords of each point and whether or not it is an anchor point.
"""

words = []
with open('/content/full_data', 'r') as the_file:
    count = 0
    index = 0
    for line in the_file:
        if count % 2 == 0:
            words.append(str(index) + ' ' + line.rstrip())
            index += 1
        count += 1

words

df.loc[0,:].tolist()

with open('full_data', 'w') as the_file:
    for i in range(0, len(words)):
        if i >= 0:
            coords = three_d.loc[i,:].tolist()
            idx_word = words[i].split()
            if int(idx_word[0]) in anchor_points:
                is_anchor = 1
            else:
                is_anchor = 0
            the_file.write(idx_word[1] + '\n')
            the_file.write(str(coords[0]) + ' ' + str(coords[1]) + ' ' + str(coords[2]) + ' ' + str(is_anchor) + ' \n')

with open('meta-main-redo.txt', 'w') as the_file:
    for i in range(0, len(words)):
        if i >= 0:
            coords = df.loc[i,:].tolist()
            idx_word = words[i].split()
            if int(idx_word[0]) in anchor_points:
                the_file.write(idx_word[0] + ' ' + idx_word[1] + '\n')
            else:
                pass

"""# **Computing Timeline Importances**
Here we compute the word importances to each of their documents (this section uses code from another notebook). We need to format the importances as a CSV, with the header <polyglot_index, word, year_1, ..., year_n>
"""

'''
First we have to extract the years associated with each document.
Note that from this point on we treat the row index as the document index.
'''
df['date'] = df['date'].str[-4:].astype(int)

'''
For each document, we compute all of the tf-idf scores of each word in that document
tf-idf = (frequency of w in d)/(number of words in d) * log(size of corpus * number of documents containing w)
'''
# set size of corpus
corpus_size = df.shape[0]

# cache the number of words in each document
num_words_per_doc = {}
for i in range(0, corpus_size):
    num_words_per_doc[i] = len(df['text'][i])

# making temp df
temp = []
for i in range(0, corpus_size):
    temp.append(df['text'][i])

# cache the number of documents each word is in
num_docs_per_word = {}
for i in range(0, len(all_words)):
    word = all_words[i]
    count = 0
    for j in range(0, corpus_size):
        if word in temp[j]:
            count += 1
    num_docs_per_word[all_words[i]] = count
    count = 0

# Need a list of years and all the documents in that year
years = df['date'].unique().tolist()
docs_in_years= {}
for year in years:
    docs_in_years[int(year)] = []
docs_in_years

for i in range(0, corpus_size):
    year = int(df['date'][i])
    if year in years:
        docs_in_years[year].append(i)
docs_in_years

df2 = pd.DataFrame(all_words, columns=['word'])
df2 = df2.reindex(columns=['word'] + [str(x) for x in years])

temp_list = [[0 for i in range(0, 23)] for j in range(0, 14654)]
len(temp_list[0])

len(years)

import math
# need to use the index of each word
for year in years:
    print('CURRENT YEAR: ', year)
    for doc in docs_in_years[year]:
        for word in df['text'][doc]:
            num_times_word_in_doc = df['text'][doc].count(word)
            num_words_in_doc = num_words_per_doc[doc]
            num_docs_word_in = num_docs_per_word[word]
            if_idf = (num_times_word_in_doc/num_words_in_doc) * math.log(corpus_size * num_docs_word_in)
            word_index = all_words.index(word)
            year_index = year - 2000 - 1
            temp_list[word_index][year_index] += if_idf
            #df2.loc[df2['word'] == word, str(year)] += if_idf
            # # compute if-df of word, add to (word, year) index

len(temp_list[0])

import csv
# data rows of csv file
with open('years_no_words.csv', 'w') as f:
    # using csv.writer method from CSV package
    header = ['2022', '2021', '2020', '2019', '2018', '2017', '2016', '2015', '2014', '2013', '2012', '2011', '2010', '2009', '2008', '2007', '2006', '2005', '2004', '2003', '2002', '2001', '2000']
    header = [[int(x)] for x in header]
    #header = [int(x) for x in header]
    write = csv.writer(f)
    write.writerows(header)
    write.writerows(temp_list)

len(temp_list[0])

temp_list[0]

temp = pd.DataFrame(temp_list,columns=years)
temp['word']= all_words
temp

cols = temp.columns.tolist()
cols = cols[-1:] + cols[:-1]
temp = temp[cols]

temp.index.tolist()

temp
temp['polyglot_index'] = temp.index.tolist()

temp

temp.to_csv('years_FINAL.csv', index = False)
!cp years_FINAL.csv "/content/drive/MyDrive"