# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 19:52:20 2018

@author: ETsham
"""

import sys



import datasets
import numpy as np
import os
import pickle
from sklearn import metrics
import save_results

#from Embedding_Generator import TfidfEmbeddingVectorizer
#from SkipgramGenerator import SkipGramVectorizer
#from slurs import get_slurterms

import matplotlib.pyplot as plt
from itertools import cycle
from sklearn.metrics import roc_curve, auc
from scipy import interp
from sklearn.preprocessing import label_binarize

dirname="ethnicity"
testing_file="Data/Test/eth_test"
features="wordngrams"

    
label="LR"
w2v_file = "w2v/w2v_300.bin"
ft_file = "w2v/ft_300_wn2.bin"
    
    
encoding="utf-8"

def loaddata(filename):
    text, sentences,vocab, labels = datasets.build_data(filename)
    
    tokenized_text=[]

    for sent in text:
        sent=sent.split()
        tokenized_text.append(sent)
  
    actual_label_ids=[]
    actual_labels=[]

    for i in range(len(sentences)):
        actual_label_ids.append(sentences[i]['y'])
    
        
    for i in actual_label_ids:
        actual_labels.append(labels[i])
            
    X, y = np.array(tokenized_text), np.array(actual_labels)
    print ("total examples %s" % len(y))
    return X, y, text, actual_label_ids, vocab, labels, sentences

        
def load_model(outputdir,modelname):
    with open(outputdir+'/'+modelname+'.p', 'rb') as fid:
        loaded_model = pickle.load(fid)
    return loaded_model

def results(model, outputdir, sentences_test, predicted, probability):
    
    if not os.path.exists(outputdir):
        print ("Output dir ",outputdir, " doesn't exist")
        
    data=[]
    for i in range(len(predicted)):
        sent=sentences_test[i]["text"]
        actual_label = sentences_test[i]['y']
        predicted_label = predicted[i]
        predicted_class_prob = probability[i][predicted_label]
        original_sentence = sentences_test[i]["orig_sentence"]
        data.append([predicted_class_prob, labels_test[predicted_label],labels_test[actual_label],sent,original_sentence])
        
    save_results.evaluate(data,outputdir,testing_file,labels_test, model)

X_test, y_test, text_test, actual_label_ids_test, vocab_test, labels_test,sentences_test=loaddata(testing_file)

print ("labels_test=", labels_test)
outputdir="Results/"+label+"/"+dirname+"/"+features
"""if not os.path.exists(outputdir):
    print ("\nOutput dir ",outputdir, " doesn't exist. Creating it")
    os.makedirs(outputdir)"""
    
    
modelname=label+"_"+dirname+"_"+features        

clf=load_model(outputdir, modelname)
    
predicted = clf.predict(text_test)

print ("\nAccuracy = ", np.mean(predicted == actual_label_ids_test),"\n" )
probability=clf.predict_proba(text_test)
  
print(metrics.classification_report(actual_label_ids_test, predicted, target_names = labels_test))
        
#Save results
#results(modelname, outputdir, sentences_test, predicted, probability)
#print ("\nResults saved at Implementation/",outputdir)





