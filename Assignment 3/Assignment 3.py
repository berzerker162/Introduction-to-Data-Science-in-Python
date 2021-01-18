#!/usr/bin/env python
# coding: utf-8

# In[3]:


#Question 1
#Join the three datasets: GDP, Energy, and ScimEn into a new dataset (using the intersection of country names). 
#Use only the last 10 years (2006-2015) of GDP data and only the top 15 countries by Scimagojr 'Rank' (Rank 1 through 15).
import pandas as pd
import numpy as np
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
# Filter all warnings. If you would like to see the warnings, please comment the two lines below.
import warnings
warnings.filterwarnings('ignore')
    
def answer_one():




    #def answer_one():
    # YOUR CODE HERE
    #    raise NotImplementedError()

    #load energy data
    Energy = pd.read_excel('assets/Energy Indicators.xls',
                  skiprows=18,
                  skipfooter=38,
                  usecolsint=[2,3,4,5],
                   header=None,
                   na_values=['...'],
                  names=['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable'])

    #convert energy supply to gigajoules
    Energy['Energy Supply'] = Energy['Energy Supply'].apply(lambda x: x*1000000)

    #clean footnotes from country names
    Energy['Country'] = Energy['Country'].str.replace(r'\d*','')#replace numbers with nothing

    #clean paranthesis from names
    Energy['Country'] = Energy['Country'].str.replace(r' \(.*\)','') #replace parenthesis with nothing

    #rename countries
    Energy['Country'] = Energy['Country'].replace({"Republic of Korea": "South Korea",
          "United States of America": "United States",
          "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
          "China, Hong Kong Special Administrative Region": "Hong Kong"})
    #Energy.iloc[:]

    #Iran (Islamic Republic of)	

    #load GDP data
    GDP = pd.read_csv('assets/world_bank.csv', skiprows=4)

    #rename countries
    GDP['Country Name'] = GDP['Country Name'].replace({"Korea, Rep.": "South Korea",
                                               "Iran, Islamic Rep.": "Iran",
                                               "Hong Kong SAR, China": "Hong Kong"})
    #rename column in GDP
    GDP.rename(columns = {'Country Name':'Country'},inplace=True)

    #last 10 years of GDP data
    GDP=GDP[['Country', 'Country Code', 'Indicator Name', 'Indicator Code',
    '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014','2015']]

    #read in data
    ScimEn = pd.read_excel('assets/scimagojr-3.xlsx')


    #join datasets
    join_1 = GDP.merge(Energy, how='inner',on='Country')
    join_2 = join_1.merge(ScimEn, how='inner', on='Country')
    join_2 = join_2[join_2['Rank']<=15] #only top 15
    join_2 = join_2.sort_values(by='Rank') #sort the rank
    join_2 = join_2.set_index('Country')
    join_2 = join_2[['Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations', 'Citations per document', 
             'H index', 'Energy Supply', 'Energy Supply per Capita', '% Renewable', 
             '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']] #only desired columns
    return join_2


# In[189]:





# In[1]:


def answer_two():

    # YOUR CODE HERE
    #    raise NotImplementedError()

    #load energy data
    Energy = pd.read_excel('assets/Energy Indicators.xls',
                  skiprows=18,
                  skipfooter=38,
                  usecolsint=[2,3,4,5],
                   header=None,
                   na_values=['...'],
                  names=['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable'])

    #convert energy supply to gigajoules
    Energy['Energy Supply'] = Energy['Energy Supply'].apply(lambda x: x*1000000)

    #clean footnotes from country names
    Energy['Country'] = Energy['Country'].str.replace(r'\d*','')#replace numbers with nothing

    #clean paranthesis from names
    Energy['Country'] = Energy['Country'].str.replace(r' \(.*\)','') #replace parenthesis with nothing

    #rename countries
    Energy['Country'] = Energy['Country'].replace({"Republic of Korea": "South Korea",
          "United States of America": "United States",
          "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
          "China, Hong Kong Special Administrative Region": "Hong Kong"})

    #load GDP data
    GDP = pd.read_csv('assets/world_bank.csv', skiprows=4)

    #rename countries
    GDP['Country Name'] = GDP['Country Name'].replace({"Korea, Rep.": "South Korea",
                                               "Iran, Islamic Rep.": "Iran",
                                               "Hong Kong SAR, China": "Hong Kong"})

    #read in data
    ScimEn = pd.read_excel('assets/scimagojr-3.xlsx')

    #rename column in GDP
    GDP.rename(columns = {'Country Name':'Country'},inplace=True)


    #count records in full join all three tables
    j1 = pd.merge(GDP, Energy, how='outer',left_on='Country',right_on='Country')
    j2 = pd.merge(j1,ScimEn, how='outer', left_on='Country',right_on='Country')
    #all_count = len(j2.index)
    #print(all_count)

    #count records in intersection of all three tables
    i1 = pd.merge(GDP,Energy, how='inner',left_on='Country',right_on='Country')
    i2 = pd.merge(i1,ScimEn, how='inner',left_on='Country',right_on='Country')
    #inner_count = len(i2.index)
    #print(inner_count)

    #subtract intersection from full join
    # return 
    return(len(j2) - len(i2))


# In[239]:


j2


# In[149]:


#Question 3
#What are the top 15 countries for average GDP over the last 10 years?
#This function should return a Series named avgGDP with 15 countries and their average GDP sorted in descending order.

def answer_three():
    df = answer_one()
    
    #create 10 year avg column
    df = df[['2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']]
    avgGDP = df.mean(axis=1).sort_values(ascending=False).nlargest(15)
    
    return avgGDP


# In[58]:


answer_three()


# In[37]:


#Question 4
#By how much had the GDP changed over the 10 year span for the country with the 6th largest average GDP?
#This function should return a single number.
def answer_four():
    
    df = answer_one()
    
    #create 10 year avg column
    df = df[['2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']]
    df['avgGDP'] = df.mean(axis=1)
    df = df.sort_values('avgGDP',ascending=False)
    #.sort_values(ascending=False).nlargest(15)
    
     
    final = df['2015'][5]
    initial = df['2006'][5]
    
    return final - initial


# In[38]:


answer_four()


# In[45]:


#Question 5
#What is the mean energy supply per capita?
#This function should return a single number.
def answer_five():
    df = answer_one()
    
    return df['Energy Supply per Capita'].mean()


# In[46]:


answer_five()


# In[67]:


#Question 6
#What country has the maximum % Renewable and what is the percentage?
#This function should return a tuple with the name of the country and the percentage.
def answer_six():
    df = answer_one()
    
    maximum = df['% Renewable'].max()
    country = df['% Renewable'].idxmax()
    
    #ans = (country,maximum)
    return (country, maximum)


# In[68]:


answer_six()


# In[78]:


#Question7
#Create a new column that is the ratio of Self-Citations to Total Citations. 
#What is the maximum value for this new column, and what country has the highest ratio?
#This function should return a tuple with the name of the country and the ratio.
def answer_seven():
    df = answer_one()
    
    df['Ratio'] = df['Self-citations'] / df['Citations']
    
    maximum = df['Ratio'].max()
    country = df['Ratio'].idxmax()
    
    return (country,maximum)


# In[79]:


answer_seven()


# In[103]:


#Question 8
#Create a column that estimates the population using Energy Supply and Energy Supply per capita.
#What is the third most populous country according to this estimate?
#This function should return the name of the country

def answer_eight():
    
    df = answer_one()
    
    df['Estimate'] = df['Energy Supply'] / df['Energy Supply per Capita']
    
    country = df.nlargest(3,'Estimate').iloc[2].name
    
    
    return country


# In[104]:


answer_eight()


# In[140]:


#Question 9
#Create a column that estimates the number of citable documents per person. What is the correlation between 
#the number of citable documents per capita and the energy supply per capita? 
#Use the .corr() method, (Pearson's correlation).
#This function should return a single number.

#(Optional: Use the built-in function plot9() to visualize the relationship between 
#Energy Supply per Capita vs. Citable docs per Capita)

def answer_nine():
    import matplotlib.pyplot as plt
    
    df = answer_one()
    
    df['Pop'] = df['Energy Supply'] / df['Energy Supply per Capita']
    
    df['Citable per capita'] = df['Citable documents'] / df['Pop']
    
    #correlation
    ans = df['Citable per capita'].corr(df['Energy Supply per Capita'],method='pearson')
    
    #plot
    df.plot('Citable per capita','Energy Supply per Capita', kind = 'scatter',xlim=[0, 0.00055]);
    
    return ans


# In[141]:


answer_nine()


# In[196]:


#Question 10
#Create a new column with a 1 if the country's % Renewable value is at or above the median for all countries in the top 15, 
#and a 0 if the country's % Renewable value is below the median.
#This function should return a series named HighRenew whose index is the country name sorted in ascending order of rank.
def answer_ten():
    
    df = answer_one()
    
    benchmark = df['% Renewable'].median()
    
    df['HighRenew'] = df['% Renewable'].apply(lambda x: 1 if x>= benchmark else 0)
    
    return df['HighRenew'] # HighRenew


# In[197]:


answer_ten()


# In[222]:


#Question 11
#Use the following dictionary to group the Countries by Continent, then create a DataFrame that displays the sample size (the number of countries in each continent bin),
#and the sum, mean, and std deviation for the estimated population of each country.
def answer_eleven():
    
    ContinentDict  = {'China':'Asia', 
                  'United States':'North America', 
                  'Japan':'Asia', 
                  'United Kingdom':'Europe', 
                  'Russian Federation':'Europe', 
                  'Canada':'North America', 
                  'Germany':'Europe', 
                  'India':'Asia',
                  'France':'Europe', 
                  'South Korea':'Asia', 
                  'Italy':'Europe', 
                  'Spain':'Europe', 
                  'Iran':'Asia',
                  'Australia':'Australia', 
                  'Brazil':'South America'}
    
    df = answer_one()
    df.reset_index(inplace=True)
    
    #population
    df['Pop'] = df['Energy Supply'] / df['Energy Supply per Capita']

    
    #add continent column
    df['Continent'] = df['Country'].map(ContinentDict)
    
    #sample size (the number of countries in each continent bin), and the sum, mean, and std deviation for the estimated population of each country.
    df.groupby('Continent')['Pop'].agg('sum')
    
    
    
    return df.groupby('Continent')['Pop'].agg(['size','sum','mean','std'])


# In[223]:


answer_eleven()


# In[233]:


#Question 12
#Cut % Renewable into 5 bins. Group Top15 by the Continent, as well as these new % Renewable bins.
#How many countries are in each of these groups?
#This function should return a Series with a MultiIndex of Continent, then the bins for % Renewable.
#Do not include groups with no countries.
def answer_twelve():
    
    ContinentDict  = {'China':'Asia', 
                  'United States':'North America', 
                  'Japan':'Asia', 
                  'United Kingdom':'Europe', 
                  'Russian Federation':'Europe', 
                  'Canada':'North America', 
                  'Germany':'Europe', 
                  'India':'Asia',
                  'France':'Europe', 
                  'South Korea':'Asia', 
                  'Italy':'Europe', 
                  'Spain':'Europe', 
                  'Iran':'Asia',
                  'Australia':'Australia', 
                  'Brazil':'South America'}
    
    df = answer_one()
    df.reset_index(inplace=True)

    #map continents
    df['Continent'] = df['Country'].map(ContinentDict)
    
    #put renewable in bins    
    df['% Renewable'] = pd.cut(df['% Renewable'],5)
    
    ans = df.groupby(['Continent','% Renewable']).agg('size')
    
    
    return ans  
    


# In[234]:


answer_twelve()


# In[257]:


#Question 13
#Convert the Population Estimate series to a string with thousands separator (using commas). 
#Use all significant digits (do not round the results).e.g. 12345678.90 -> 12,345,678.90
#This function should return a series PopEst whose index is the country name and whose values
#are the population estimate string
def answer_thirteen():
    
    df = answer_one()
    
    #population
    df['PopEst'] = df['Energy Supply'] / df['Energy Supply per Capita']
    
    ans = df['PopEst'].apply('{:,}'.format)
    
    return ans


# In[258]:


answer_thirteen()


# In[259]:


def plot_optional():
    import matplotlib as plt
    get_ipython().run_line_magic('matplotlib', 'inline')
    Top15 = answer_one()
    ax = Top15.plot(x='Rank', y='% Renewable', kind='scatter', 
                    c=['#e41a1c','#377eb8','#e41a1c','#4daf4a','#4daf4a','#377eb8','#4daf4a','#e41a1c',
                       '#4daf4a','#e41a1c','#4daf4a','#4daf4a','#e41a1c','#dede00','#ff7f00'], 
                    xticks=range(1,16), s=6*Top15['2014']/10**10, alpha=.75, figsize=[16,6]);

    for i, txt in enumerate(Top15.index):
        ax.annotate(txt, [Top15['Rank'][i], Top15['% Renewable'][i]], ha='center')

    print("This is an example of a visualization that can be created to help understand the data. This is a bubble chart showing % Renewable vs. Rank. The size of the bubble corresponds to the countries' 2014 GDP, and the color corresponds to the continent.")


# In[260]:


plot_optional()


# In[ ]:




