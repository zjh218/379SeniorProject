import pickle 
from sklearn import svm
from sklearn import linear_model
from sklearn.feature_extraction import DictVectorizer
from timeit import default_timer as timer
from sklearn.model_selection import cross_validate
start = timer()
arrayOfYears = pickle.load(open("arrayOfYears.p", "rb"))
arrayOfGrades = pickle.load(open("arrayOfGrades.p", "rb"))
featuresToRemove = pickle.load(open("featuresToRemove.p", "rb"))
arrayOfGraduation = pickle.load(open("arrayOfGraduation.p", "rb"))
arrayOfJustGrades = []
for studYear in arrayOfYears:
    arrayOfJustGrades+=[[studYear["GPA"]]]
vec = DictVectorizer()
vectorizedArrayOfYears = vec.fit_transform(arrayOfYears).toarray()

reg2 = linear_model.BayesianRidge()
reg2.fit(vectorizedArrayOfYears,arrayOfGrades)
a = zip(reg2.coef_,vec.get_feature_names())
gpaFeatures = list(a)
gpaFeatures.sort()


clf2 = svm.SVC(kernel="linear")
clf2.fit(vectorizedArrayOfYears, arrayOfGraduation)
b = zip(clf2.coef_[0],vec.get_feature_names())
gradFeatures = list(b)
gradFeatures.sort()

#regr = linear_model.BayesianRidge()
#clf = svm.SVC(kernel="linear")
clf2 = linear_model.LogisticRegression()
#clf3 = naive_bayes.GaussianNB()
scoring = ['precision', 'recall','accuracy','f1']
scores = cross_validate(clf2, vectorizedArrayOfYears, arrayOfGraduation, cv=10, scoring=scoring)
scores2 = cross_validate(clf2, arrayOfJustGrades, arrayOfGraduation, cv=10, scoring=scoring)
print("run time = "+str(timer()-start))