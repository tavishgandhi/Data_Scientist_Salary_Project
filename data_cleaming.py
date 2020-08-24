# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 02:38:53 2020

@author: Tavish Gandhi
"""


import pandas as pd
df1 = pd.read_csv("glassdoor_jobs.csv")

# Parsing the salary data

x= df1[df1['Salary Estimate'] == '-1']
df1 = df1[df1['Salary Estimate'] != '-1']

x = df1["Salary Estimate"]
Salary = x.apply(lambda x:x.split("(")[0])
minus_k = Salary.apply(lambda x:x.replace('K'," ").replace("$", " "))

df1["Employer_provided"] = df1["Salary Estimate"].apply(lambda x: 1 if 'employer provided salary' in x.lower() else 0)
df1["Hourly"] = df1["Salary Estimate"].apply(lambda x: 1 if 'per hour' in x.lower() else 0)

min_hr = minus_k.apply(lambda x: x.lower().replace('per hour'," ").replace("employer provided salary:", " "))
xx = min_hr.str.strip()

df1['Min_Salary'] = xx.apply(lambda x : x.split("-")[0])
df1['Max_Salary'] = xx.apply(lambda x : x.split("-")[1])
df1["Avg_Salary"] = (df1["Min_Salary"].astype(int) + df1["Max_Salary"].astype(int))/2

# Company name text only

df1["company_txt"] = df1.apply(lambda x: x['Company Name'] if x['Rating'] <0 else x["Company Name"][:-3], axis= 1)

#state field

df1["Job_state"] = df1["Location"].apply(lambda x : x.split(",")[1])
df1.Job_state.value_counts()
df1["same state"] = df1.apply(lambda x: 1 if x.Location == x.Headquarters else 0 ,axis  = 1)

#Age of company
df1["Age"] = df1.Founded.apply(lambda x : x if x <0 else 2020-x)

# Parsing Job description

df1["Python"] = df1["Job Description"].apply(lambda x : 1 if 'python' in x.lower() else 0)
df1.Python.value_counts()

df1["R_studio"] = df1["Job Description"].apply(lambda x : 1 if 'r studio' in x.lower() or 'r-studio' in x.lower() else 0)
df1.R_studio.value_counts()

df1["AWS"] = df1["Job Description"].apply(lambda x : 1 if 'aws' in x.lower() else 0)
df1.AWS.value_counts()

df1["spark"] = df1["Job Description"].apply(lambda x : 1 if 'spark' in x.lower() else 0)
df1.spark.value_counts()

df1["excel"] = df1["Job Description"].apply(lambda x : 1 if 'excel' in x.lower() else 0)
df1.excel.value_counts()


df1.drop(["Unnamed: 0"], axis = 1, inplace=True)
df1.to_csv("Salary_Data_Cleaned.csv", index=False)


df = pd.read_csv("Salary_Data_Cleaned.csv")
