# -*- coding: utf-8 -*-
"""
Created on Mon May  2 20:52:02 2022

@author: dharm
"""

"""
Project Notes

Analysis of the Gitub history of the scala programming language. Uses 4 datasets
1) pulls_2011-2013 - Contains basic information about the pull requests from 2011 to 2013. 
   pid, user and date of each pull request
2) pulls_2014-2018 - Same information as the first dataset but from 2011 to 2013
3) pull_files - Contains all the files that were modified by the pull requests. Pid and file name

"""

import pandas as pd
import matplotlib.pyplot as plt
pd.set_option('display.max_columns',None)

# 1. Read all four files into variables

pull_files = pd.read_csv(r'C:\Users\dharm\OneDrive\Desktop\Training\Python project - Github history of scala language\pull_files.csv')
pulls_13 = pd.read_csv(r'C:\Users\dharm\OneDrive\Desktop\Training\Python project - Github history of scala language\pulls_2011-2013.csv')
pulls_18 = pd.read_csv(r'C:\Users\dharm\OneDrive\Desktop\Training\Python project - Github history of scala language\pulls_2014-2018.csv')

# 2. Cleaning the data

    # Print the datatypes of the variables

print(pull_files.dtypes)
print(pulls_13.dtypes)
print(pulls_18.dtypes)

    # Append the pulls_13 and pulls_18 files into one file called pulls

pulls = pulls_13.append(pulls_18,ignore_index=False)

    # Convert the date column of the pulls file to datetime

pulls["date"] = pd.to_datetime(pulls["date"],utc=True)

    # Merge the pulls dataframe with pulls_files on pid

pulls_data = pulls.merge(pull_files, on='pid')

#3. Count and plot the number of pull requests and users of the project by month and year

    # Create two new columns for month and year from the date column
pulls_data["month"] = pd.DatetimeIndex(pulls_data["date"]).month
pulls_data["year"] = pd.DatetimeIndex(pulls_data["date"]).year
pulls_data["date_monthly"] = pulls_data["year"].astype(str) +"-"+ pulls_data["month"].astype(str)


    # Count the number of pull requests by month and year
pulls_count = pulls_data.groupby(["date_monthly"])["pid"].count().reset_index()
users_count = pulls_data.groupby(["date_monthly"])["user"].nunique().reset_index()


fig,ax = plt.subplots(2,1)
fig.figsize=(15,4)

# pulls_count.plot(kind='bar',figsize=(12,4),title="Number of pulls")
# users_count.plot(kind='bar',figsize=(12,4))

ax[0].bar(x = pulls_count["date_monthly"],height = pulls_count["pid"])
ax[0].set_xticklabels(pulls_count["date_monthly"],rotation=90)
ax[0].set_xlabel("Month")
ax[0].set_ylabel("Number of pulls")

ax[1].bar(x = users_count["date_monthly"],height = users_count["user"])
ax[1].set_xticklabels(users_count["date_monthly"],rotation=90)
ax[1].set_xlabel("Month")
ax[1].set_ylabel("Number of users")

print(pulls_data)

#4. Identify the users who made the most number of contributions by each year

num_contr_count = pulls_data.groupby(["user","year"])["pid"].count().reset_index()
num_contr_count = num_contr_count.sort_values(by=["year","pid"],ascending=False)

print(num_contr_count)


year = num_contr_count["year"].iloc[0]

print(num_contr_count.iloc[0,0],num_contr_count.iloc[0,1],num_contr_count.iloc[0,2])

for i in range(len(num_contr_count)):
    if num_contr_count["year"].iloc[i]==year:
           continue
    else:
        print(num_contr_count.iloc[i,0],num_contr_count.iloc[i,1],num_contr_count.iloc[i,2]) 
        year = num_contr_count["year"].iloc[i]

#5. What were the files that were changed in the last 300 pull requests and the
# number of times each file has been changed. Identify the file that has been changed
# the most number of times

last_300 = pulls_data.nlargest(300,'date')
last_300_count = last_300.groupby("file")["pid"].count().reset_index()
last_300_count = last_300_count.sort_values(by="pid",ascending=False)
last_300_count_top = last_300_count.iloc[0]['file']
print(last_300_count_top)

#6. Who made the last 10 pull requests of the file we identified in the previous 
#question (file that was changed the most number of times in the last 300 pull requests)

top_file_requests = pulls_data[pulls_data['file']==last_300_count_top]
top_file_users = list(top_file_requests.nlargest(10,'date')['user'])
print(top_file_users)

#7. To asess the contribution of each of the users identified in the above question, 
# plot the number of pull requests by user by year

top_users_extract = pulls_data[pulls_data['user'].isin(top_file_users)]
top_users_count = top_users_extract.groupby(['year','user'])['pid'].count().reset_index()
top_users_count = top_users_count.sort_values(by='year',ascending = True)
top_users_wide = top_users_count.pivot_table(index='year',columns='user',values='pid',fill_value=0)
print(top_users_wide)
top_users_wide.plot(kind='bar')
        



    







        



    











        


    
    





