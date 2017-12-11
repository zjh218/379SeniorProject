
import pandas as pd

import collections
import pickle 

df = pd.read_csv("YearByYearUsable.csv")
df.head()
df = df.sort_values(by=['Unique Student Key','Term'])
previousStudentId=0
currentStudentId=0
change = 0
students = collections.defaultdict(lambda: collections.defaultdict(dict))
studentsGrades = collections.defaultdict(lambda: collections.defaultdict(dict))
semesters = dict()
sport = []
housing = []
homeState = []
season = ""
missing = set()
courses = set()
arrayOfGraduate = []
studentsInGraduate = set()
for index, row in df.iterrows():
    
    term = row['Term'] % 100
    year = int(row['Term']/100)
    if (term == 40):
        academicYear = str(year)+"_"+str(year+1)
    else:
        academicYear = str(year-1)+"_"+str(year)
    if row['Graduated'] == "Y":
        students[row['Unique Student Key']]["G"] = 1
    elif row['Graduated'] == "N":
        students[row['Unique Student Key']]["G"] = 0
    else:
        print("error")
    courseCode = str(row['Subject'])+"-"+str(row['Course Number'])
    courses.add(courseCode)
    if courseCode not in students[row['Unique Student Key']][academicYear]:
        gradePoints = row['Grade Points']
        if "W" in row['Grade']:
            students[row['Unique Student Key']][academicYear][courseCode] = "W"
        elif "R" in row['Grade']:
            students[row['Unique Student Key']][academicYear][courseCode] = "CR"
        elif "P" in row['Grade']:
            students[row['Unique Student Key']][academicYear][courseCode] = "P"
        elif "F" in row['Grade']:
            students[row['Unique Student Key']][academicYear][courseCode] = "F"
        elif "D" in row['Grade']:
            students[row['Unique Student Key']][academicYear][courseCode] = "D"
        elif "C" in row['Grade']:
            students[row['Unique Student Key']][academicYear][courseCode] = "C"
        elif "B" in row['Grade']:
            students[row['Unique Student Key']][academicYear][courseCode] = "B"
        elif "A" in row['Grade']:
            students[row['Unique Student Key']][academicYear][courseCode] = "A"
      #  students[row['Unique Student Key']][academicYear][courseCode] = row['Grade']
        if "total-credits-"+str(term) in students[row['Unique Student Key']][academicYear]:
            students[row['Unique Student Key']][academicYear]["total-credits-"+str(term)] += row['Credits']
        else:    
            students[row['Unique Student Key']][academicYear]["total-credits-"+str(term)] = row['Credits']
            
        if "Quality Points" in studentsGrades[row['Unique Student Key']][academicYear]:
            if (row['Grade'] != 'P' and row['Grade'] != "W"):
                studentsGrades[row['Unique Student Key']][academicYear]["Quality Points"] += row['Grade Points'] * row['Credits']
        else:    
            studentsGrades[row['Unique Student Key']][academicYear]["Quality Points"] = row['Grade Points'] * row['Credits']
    
    students[row['Unique Student Key']][academicYear]["housing-"+str(term)] = row['Living']
   
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
    if "season-"+str(term) not in students[row['Unique Student Key']][academicYear]:
         students[row['Unique Student Key']][academicYear]["season-"+str(term)] = "none"
    if "season-WI" not in students[row['Unique Student Key']][academicYear]:
         students[row['Unique Student Key']][academicYear]["season-WI"] = "none"
    if term == 40 and  row["Season"] == "IN":
        students[row['Unique Student Key']][academicYear]["season-"+str(term)] = row["Sport"]
    elif  term == 10 and  row["Season"] == "IN" :
        students[row['Unique Student Key']][academicYear]["season-"+str(term)] = row["Sport"]
    elif row["Season"] == "WI":
        students[row['Unique Student Key']][academicYear]["season-WI"] = row["Sport"]

arrayOfYears = []
arrayOfGrades= []
halfYearNoFall = set()
halfYearNoSpring = set()
for student in students:
    for year in students[student].keys():
        if year != "G":
            thisYear = int(year[:4])
            for nextsem in students[student].keys():
                if nextsem != "G":
                    nextYear = int(nextsem[:4])
                    if (thisYear+1 == nextYear):
                        #skrt skrt
                        #calculate GPA
                        fallCredits = 0 if "total-credits-40" not in students[student][nextsem] else students[student][nextsem]["total-credits-40"]
                        if fallCredits == 0 :
                            halfYearNoFall.add(student)
                        springCredits = 0 if "total-credits-10" not in students[student][nextsem] else students[student][nextsem]["total-credits-10"]
                        if springCredits == 0:
                            halfYearNoSpring.add(student)
                        nextYearGPA = studentsGrades[student][nextsem]['Quality Points'] /(fallCredits+springCredits)
                        thisFall = 0 if "total-credits-40" not in students[student][year] else students[student][year]["total-credits-40"] 
                        thisSpring = 0 if "total-credits-10" not in students[student][year] else students[student][year]["total-credits-10"]
                        thisYearGPA = studentsGrades[student][year]['Quality Points'] / (thisFall+thisSpring)
                        students[student][year]["GPA"] = thisYearGPA
                        arrayOfYears += [students[student][year]]
                        arrayOfGrades+= [nextYearGPA]
                        arrayOfGraduate+=[students[student]["G"]]

#accumulate a list of all the features, and their values.
totalFeaturesYbY = {}
for student in students:
   for year in students[student].keys():
       if year != "G":
        for key in students[student][year].keys():
            if key in totalFeaturesYbY:
                totalFeaturesYbY[key]+=1
            else:
                totalFeaturesYbY[key]=1
'''
#an attempt at critical mass thresholding. 
#did not help to use it.
twoPercent = int(len(students)*.15)
featuresToRemove = []
for feature in totalFeaturesYbY.keys():
    if totalFeaturesYbY[feature] <= twoPercent:
        featuresToRemove+=[feature]
'''
#for entry in arrayOfYears:
#    for key in entry.keys():
 #       totalFeaturesYbY.add(key)
#pickle.dump(featuresToRemove, open("featuresToRemove.p","wb"))
pickle.dump(arrayOfYears, open("arrayOfYears.p", "wb"))
pickle.dump(arrayOfGrades, open("arrayOfGrades.p", "wb"))
pickle.dump(arrayOfGraduate, open("arrayOfGraduation.p",'wb'))