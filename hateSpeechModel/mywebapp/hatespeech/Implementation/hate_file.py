# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 19:52:20 2018

@author: ETsham
"""


import os
import pickle

import datasets
import numpy as np
import os
import pickle
from sklearn import metrics
import save_results
#import sys
#sys.path.insert(0, "E:/Project/")
#print (sys.path)


testing_file = "Data/Test/comb_test" 
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

def predict_label(sentence):
    

    outputdir=os.path.join(os.path.dirname(__file__),"Results/"+label+"/"+dirname+"/"+features)

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

"""sentence = input("Enter the sentence")
sentence=[sentence]"""
"""sentence="قادیانی کافر ہیں"
sentence=[sentence]
p=predict_label(sentence)
print (p)"""