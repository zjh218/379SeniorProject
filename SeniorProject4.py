from IPython.display import Image
import matplotlib as mlp
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import sklearn
import operator
import collections
import pickle 
import re

from sklearn.model_selection import *
from sklearn import datasets
from sklearn import tree
from sklearn import svm
from sklearn import ensemble
from sklearn import neighbors
from sklearn import linear_model
from sklearn import metrics
from sklearn import preprocessing
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_selection import VarianceThreshold
from sklearn.metrics import mean_squared_error
from timeit import default_timer as timer

import seaborn as sns

featuresToThreshold = pickle.load(open("featuresToThreshold.p", "rb"))
featuresToNotTouch = pickle.load(open("featuresToNotThreshold.p", "rb"))
vec = picle.load(open("dictionaryVectorizer.p","rb"))