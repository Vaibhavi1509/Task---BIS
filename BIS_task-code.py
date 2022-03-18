#!/usr/bin/env python
# coding: utf-8

# In[6]:


import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import wget
import zipfile
import os
from datetime import datetime


# In[7]:


response =  requests.get('https://www.bis.org/statistics/full_data_sets.htm','https://www.bis.org/statistics/full_credit_gap_csv.zip')
print(response.status_code)


# In[8]:


soup = BeautifulSoup(response.text, "html.parser")


# In[9]:


all_text = []
for text in soup.find_all('a'):
    all_text.append(text)
string = list(map(str, all_text))
print(string)


# In[10]:


all_links = []
for link in string:
    if '<a href="/statistics/full_' in link:
        word = link[link.index('/'):link.rindex('"')]
        url = "https://www.bis.org"+word
        all_links.append(url)
print(all_links)


# In[11]:


name = []
for s in string:
    if '<a href="/statistics/full_' in s:
        word = s[s.index('>')+1:s.rindex('<')]
        name.append(word)
print(name)


# In[12]:


dataset = []
for data in name:
    if '\xa0' in data:
        data = data.replace('\xa0','')
    dataset.append(data)
print(dataset)


# In[13]:


df = pd.DataFrame({'DATA':dataset ,'LINKS':all_links})
df.to_csv('BIS statistics.csv', index = False)


# In[14]:


BIS = pd.read_csv('BIS statistics.csv')
BIS


# In[23]:


class Scrapper:
    
    @classmethod
    def credit_gap_dataset(self):
        
        credit_gap_url = BIS['LINKS'][4]
        print("File link =", credit_gap_url )
        file = wget.download(credit_gap_url)
        print("Downloaded the zip file=",file)
        
        ##Download the zip file and extract the csv file
        path = os.getcwd()+"\\"+file
        zip_download = zipfile.ZipFile(path).extractall
        
        #Convert the file to a dataframe
        zip_download = pd.DataFrame()
        
        #As now the file is downloaded in the downloads section of the PC , I can read the file
        credit_gap = pd.read_csv(r'C:\Users\sanat\Downloads\WS_CREDIT_GAP_csv_col.csv')
        
        
        #BASIC DATA CLEANING 
        
        #Removing the unnecessary columns which have one unique value and the year wise columns that have no frequency values
        credit_gap = credit_gap.drop(axis = 0, columns = ['Frequency','Borrowing sector','Lending sector','Title (tseries level)'])
        credit_gap = credit_gap.dropna(axis = 1)
        
        #Removing the codes for the country and the credit gap data type. Making the Time Period column blank.
        credit_gap["Borrowers' country"] = credit_gap["Borrowers' country"].str.split(':').str[1]
        credit_gap["Credit gap data type"] = credit_gap["Credit gap data type"].str.split(':').str[1]
        credit_gap["Time Period"]= ''
        credit_gap = credit_gap.set_index(["Borrowers' country", 'Credit gap data type', 'Time Period'])
        credit_gap = credit_gap.T
        
        #Creating the timestamp column 
        credit_gap["TimeStamp"]= datetime.now()
        print('''We can see from the resulting dataset that the time series data starts from the 
        year 2009 as we have removed the other columns to improve the consistency. 
        Have also divided countries in separate columns as Multi Index column containing 
        the three credit gap data type for each country. Made the time period column also 
        index to represent year-quarterly range. A separate column with all the timestamps''')
        print(credit_gap)
        
        credit_gap.to_csv('Credit_To_Gdp_Gaps.csv')
        
Scrapper.credit_gap_dataset()
              


# In[ ]:




