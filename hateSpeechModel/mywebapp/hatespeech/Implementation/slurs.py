#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 23 07:16:44 2019

@author: ramsha
"""
import codecs
import numpy as np

def get_slurterms(x):
    with codecs.open ("lexicon.txt", "r", encoding="utf=8") as f:
        reader=f.read()
        words=reader.split("\r\n")
        slur_terms_count=[]
        for sent in x:
            count=0
            for w in words:
                if w in sent:
                    count+=1
                    
            if (count>=1 ):      
                slur_terms_count.append(1)
            else:
                slur_terms_count.append(0)
        
        return np.array(slur_terms_count).reshape(-1,1)