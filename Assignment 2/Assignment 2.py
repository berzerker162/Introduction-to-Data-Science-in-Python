#Assignment 2
#For this assignment you'll be looking at 2017 data on immunizations from the CDC.
#Your datafile for this assignment is in assets/NISPUF17.csv. 
#A data users guide for this, which you'll need to map the variables in the data to the questions being asked, 
#is available at assets/NIS-PUF17-DUG.pdf. Note: you may have to go to your Jupyter 
#tree (click on the Coursera image) and navigate to the assignment 2 assets folder to see this PDF file).

#Question 1
#Write a function called proportion_of_education which returns the proportion of 
#children in the dataset who had a mother with the education levels equal to less than 
#high school (<12), high school (12), more than high school but not a college graduate (>12) and 
#college degree.

#This function should return a dictionary in the form of (use the correct numbers, do not round numbers):

#   {"less than high school":0.2,
#    "high school":0.4,
#    "more than high school but not college":0.2,
#    "college":0.2}

import pandas as pd
def proportion_of_education():
    df = pd.read_csv('assets/NISPUF17.csv')

    #count all moms
    moms = df['EDUC1'].count()

    #less than high school
    less_than_hs = df[df['EDUC1'] == 1].count()

    #less than high school
    hs = df[df['EDUC1'] == 2].count()

    #less than high school
    more_than_hs = df[df['EDUC1'] == 3].count()

    #less than high school
    college = df[df['EDUC1'] == 4].count()


    #proportions
    lt_hs = less_than_hs['EDUC1'] / moms
    eq_hs = hs['EDUC1'] / moms
    mt_hs = more_than_hs['EDUC1'] / moms
    coll = college['EDUC1'] / moms

    edu_dict = {'less than high school':lt_hs,
                 'high school':eq_hs,
                 'more than high school but not college':mt_hs,
                 'college':coll}

    return(edu_dict)


#Question 2
#Let's explore the relationship between being fed breastmilk as a child and getting a seasonal influenza 
#vaccine from a healthcare provider. Return a tuple of the average number of influenza vaccines for 
#those children we know received breastmilk as a child and those who know did not.

#This function should return a tuple in the form (use the correct numbers:

#(2.5, 0.1)

def average_influenza_doses():
    df = pd.read_csv('assets/NISPUF17.csv')
       
        #avg number of flu shots, fed breast milk 1
    breast = df[df['CBF_01'] == 1]['P_NUMFLU'].mean()
    breast

        #avg number of flu shoots, no breast milk 2
    no_breast = df[df['CBF_01'] == 2]['P_NUMFLU'].mean()

    results = (breast, no_breast)
    return(results)


#Question 3
#It would be interesting to see if there is any evidence of a link between 
#vaccine effectiveness and sex of the child. Calculate the ratio of the 
#number of children who contracted chickenpox but were vaccinated against it (at least one varicella dose)
# versus those who were vaccinated but did not contract chicken pox. Return results by sex.

#This function should return a dictionary in the form of (use the correct numbers):

#    {"male":0.2,
#    "female":0.4}
#Note: To aid in verification, the chickenpox_by_sex()['female'] value the autograder is looking for starts with the digits 0.0077.

def chickenpox_by_sex():
    df = pd.read_csv('assets/NISPUF17.csv')
    


    #had vaccine and male and got pox
    had_vac_male_got_pox = ((df['SEX']== 1) & (df['P_NUMVRC'] >= 1) & (df['HAD_CPOX']==1)).sum()
    had_vac_male_got_pox
    
    #had vaccine and male and no pox
    had_vac_male_no_pox = ((df['SEX']== 1) & (df['P_NUMVRC'] >= 1) & (df['HAD_CPOX']==2)).sum()
    had_vac_male_no_pox

    #had vaccine and female and got pox
    had_vac_female_got_pox = ((df['SEX']== 2) & (df['P_NUMVRC'] >= 1) & (df['HAD_CPOX']==1)).sum()
    had_vac_female_got_pox
    
    #had vaccine and female
    had_vac_female_no_pox = ((df['SEX']== 2) & (df['P_NUMVRC'] >= 1) & (df['HAD_CPOX']==2)).sum()
    had_vac_female_no_pox

    male_ratio = had_vac_male_got_pox / had_vac_male_no_pox
    female_ratio = had_vac_female_got_pox / had_vac_female_no_pox

    vax_dict = {'male':male_ratio, 'female':female_ratio}
    vax_dict

    return(vax_dict)




#Question 4¶
#A correlation is a statistical relationship between two variables. 
#If we wanted to know if vaccines work, we might look at the correlation between the use of the vaccine 
#and whether it results in prevention of the infection or disease [1]. In this question, you are to see if there 
#is a correlation between having had the chicken pox and the number of chickenpox vaccine doses given (varicella).
#Some notes on interpreting the answer. If the had_chickenpox_column is either 1 (for yes) or 2 for no, and that 
#the num_chickenpox_vaccine_column is the number of doses a child has been given of the varicella vaccine, then 
#a positive correlation (e.g. corr > 0) would mean that an increase in had_chickenpox_column (which means more 
#no's) would mean an increase in the num_chickenpox_vaccine_column (which means more doses of vaccine). 
#If corr < 0 then there is a negative correlation, indicating that having had chickenpox is related to an increase
# in the number of vaccine doses. Also, pval refers to the probability the relationship observed is significant. In this case pval should be very very small (will end in e-18 indicating a very small number), which means the result unlikely to be by chance.

#[1] This isn't really the full picture, since we are not looking at when the dose was given. It's possible that 
#children had chickenpox and then their parents went to get them the vaccine. Does this dataset have the data we would need to investigate the timing of the dose?

def corr_chickenpox():
    import scipy.stats as stats
    import numpy as np
    import pandas as pd

    df = pd.read_csv('assets/NISPUF17.csv')

    #df = pd.DataFrame(df['HAD_CPOX'], df['P_NUMVRC'])
    df = df[['HAD_CPOX','P_NUMVRC']]
    
    #clean data
    df.dropna(inplace=True)
    df = df[df['HAD_CPOX'] <=2]
    
    # here is some stub code to actually run the correlation
    corr, pval=stats.pearsonr(df['HAD_CPOX'],df['P_NUMVRC'])

    # just return the correlation
    return (corr)



