# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 19:52:20 2018

@author: ETsham
"""

import gensim
import codecs
import numpy as np
import os
import pickle
from gensim.models.word2vec import Word2Vec
from sklearn.pipeline import Pipeline, FeatureUnion
from collections import defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import metrics
import functools
from nltk.util import skipgrams
#from pyfasttext import FastText
from sklearn.multiclass import OneVsRestClassifier
from sklearn import svm
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import FunctionTransformer
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import KFold, cross_val_score, cross_val_predict, cross_validate, GridSearchCV
from pathlib import Path


#import sys
#sys.path.insert(0, "E:/Project/")
#print (sys.path)


#testing_file = "Data/data/eth_test" 
features = "charngrams"
dirname = "Hate Category"
label="LR"
w2v_file = "w2v/w2v_300.bin"
ft_file = "w2v/ft_300_wn2.bin"    
    
encoding="utf-8"
        
def load_model(outputdir,modelname):
    with open(outputdir+'/'+modelname+'.p', 'rb') as fid:
        loaded_model = pickle.load(fid)
    return loaded_model


def predict_label(sentence):
    
    #p = Path(__file__).parents[2]
    #prev_dir=os.path.abspath('../..')
    outputdir=os.path.join(os.path.dirname(__file__),"Results/"+label+"/"+dirname+"/"+features)
    #outputdir="Results/"+label+"/"+dirname+"/"+features
    """if not os.path.exists(outputdir):
        print ("\nOutput dir ",outputdir, " doesn't exist. Creating it")
        os.makedirs(outputdir)"""
        
        
    modelname=label+"_"+dirname+"_"+features        
    
    clf=load_model(outputdir, modelname)
    
    #print ("sentence =  ",sentences_test[2]["text"])
    #sentence=["قادیانی کافر ہیں"]
    predicted = clf.predict(sentence)
    #bin_predicted=label_binarize(predicted, classes=[0,1,2,3])
    if predicted==0:
        predicted="Ethnicity"
    elif predicted==1:
        predicted="National Origin"
    elif predicted==2:
        predicted="Religion"
    elif predicted==3:
        predicted="Not Hate Speech"
    return predicted


"""sentence = input("Enter the sentence")
sentence=[sentence]"""
sentence="قادیانی کافر ہیں"
sentence=[sentence]
p=predict_label(sentence)
print (p)