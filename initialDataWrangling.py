
import pandas as pd
import collections
from random import *

fileName = "athletic student data for study UPDATE.csv"
df = pd.read_csv(fileName)
df.head()
withheldStudent = {}
useableStudent = {}
students = collections.defaultdict(lambda: collections.defaultdict(dict))
semesters = dict()
sport = []
housing = []
homeState = []
missing = set()
for index, row in df.iterrows():
    term = row['Term'] % 100
    year = int(row['Term']/100)
    if (term == 40):
        academicYear = str(year)+"_"+str(year+1)
    else:
        academicYear = str(year-1)+"_"+str(year)
    courseCode = str(row['Subject'])+"-"+str(row['Course Number'])+"-"+str(term)
    if courseCode not in students[row['Unique Student Key']][academicYear]:
        students[row['Unique Student Key']][academicYear][courseCode+"-G"] = row['Grade']
        if "total-credits-"+str(term) in students[row['Unique Student Key']][academicYear]:
            students[row['Unique Student Key']][academicYear]["total-credits-"+str(term)] += row['Credits']
        else:    
            students[row['Unique Student Key']][academicYear]["total-credits-"+str(term)] = row['Credits']
            
        if "Quality Points" in students[row['Unique Student Key']][academicYear]:
            if (row['Grade'] != 'P' and row['Grade'] != "W"):
                students[row['Unique Student Key']][academicYear]["Quality Points"] += row['Grade Points'] * row['Credits']
        else:    
            students[row['Unique Student Key']][academicYear]["Quality Points"] = row['Grade Points'] * row['Credits']
    if "sport-"+str(term) in students[row['Unique Student Key']][academicYear]:
        if row['Sport'] not in students[row['Unique Student Key']][academicYear]['sport-'+str(term)]:
            students[row['Unique Student Key']][academicYear]['sport-'+str(term)]+= [row['Sport']]
            sport+=[row['Unique Student Key']]
    else:
        students[row['Unique Student Key']][academicYear]["sport-"+str(term)] = [row['Sport']]
        
        
    if "housing" in students[row['Unique Student Key']][academicYear]:
         if row['Living'] not in students[row['Unique Student Key']][academicYear]['housing']:
            students[row['Unique Student Key']][academicYear]['housing']+= [row['Living']]
            housing+=[row['Unique Student Key']]
    else:
        students[row['Unique Student Key']][academicYear]["housing"] = [row['Living']]
        
    if "homeState" in students[row['Unique Student Key']][academicYear]:
        if row['Home State'] != students[row['Unique Student Key']][academicYear]['homeState']:
            if pd.isnull(row['Home State']):
                students[row['Unique Student Key']][academicYear]['homeState'] = "none"
                if row['Unique Student Key'] not in missing:
                    missing.add(row['Unique Student Key'])
            else:
                students[row['Unique Student Key']][academicYear]['homeState'] = row['Home State']
    else:
        students[row['Unique Student Key']][academicYear]["homeState"] = row['Home State']
        
    if "seasons" in students[row['Unique Student Key']][academicYear]:
        if term == "40" and "FA" not in students[row['Unique Student Key']][academicYear]["seasons"]:
            students[row['Unique Student Key']][academicYear]["seasons"]+=["FA"]

        if term == "10" and "SP" not in students[row['Unique Student Key']][academicYear]["seasons"]:
            students[row['Unique Student Key']][academicYear]["seasons"]+=["SP"]
            
        if row['Season'] == "WI" and "WI" not in students[row['Unique Student Key']][academicYear]["seasons"]:
             students[row['Unique Student Key']][academicYear]["seasons"]+=["WI"]
for student in students:
    if ((random()*10) <= 1):
        withheldStudent[student] = student
    else:
        useableStudent[student] = student

df3 = df[df['Unique Student Key'].isin(useableStudent)]
df3.to_csv('yearByYearUsable.csv')
#
df = df[df['Unique Student Key'].isin(withheldStudent)]
df.to_csv('yearByYearWitheld.csv')