# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 19:52:20 2018

@author: ETsham
"""

import os
import pickle
from pathlib import Path

#import sys
#sys.path.insert(0, "E:/Project/")
#from . import SkipgramGenerator 
#from SkipgramGenerator import SkipGramVectorizer

#testing_file = "Data/data/eth_test" 
features = "wordngrams+charngrams"
dirname = "Religion"
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
    #print (p)
    #prev_dir=os.path.abspath('../..')
    #print (prev_dir)
    outputdir=os.path.join(os.path.dirname(__file__),"Results/"+label+"/"+dirname+"/"+features)
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
        predicted="Not Hate Speech"
    elif predicted==1:
        predicted="Attribution"
    elif predicted==2:
        predicted="Insult"
    elif predicted==3:
        predicted="Symbolization"
    return predicted


"""sentence = input("Enter the sentence")
sentence=[sentence]"""
sentence="قادیانی کافر ہیں"
sentence=[sentence]
p=predict_label(sentence)
print (p)