# -*- coding: utf-8 -*-
"""
Created on Fri Nov  2 15:03:44 2018

@author: ETsham
"""

import unicodedata
import pycrfsuite
import re
import codecs
import os

def checkdigit(char):
    digits = [u'۱',u'۲',u'۳',u'۴',u'۵',u'۶',u'۷',u'۸',u'۹',u'۰']
    if char in digits:
        return "true"
    return "false"

def isnonjoiner(char):
    non_joiners = [u'ا', u'د', u'ڈ', u'ز', u'ذ', u'ر', u'ڑ', u'ژ', u'و', u'ے']
    if char in non_joiners:
        return "true"
    return "false"

def create_char_features(sentence, i):
    features = [
        'bias',
        'char=' + sentence[i][0],
        'char.isdigit=' + checkdigit(sentence[i][0]),
        'char.isnonjoiner=' + isnonjoiner(sentence[i][0]),
        'char.category=' + unicodedata.category(sentence[i][0]),
        'char.direction=' + unicodedata.bidirectional(sentence[i][0]),
    ]
    
    if i >= 1:
        features.extend([
            'char-1=' + sentence[i-1][0],
            'char-1:0=' + sentence[i-1][0] + sentence[i][0],
        ])
    else:
        features.append("BOS")
        
    if i >= 2:
        features.extend([
            'char-2=' + sentence[i-2][0],
            'char-2:0=' + sentence[i-2][0] + sentence[i-1][0] + sentence[i][0],
            'char-2:-1=' + sentence[i-2][0] + sentence[i-1][0],
        ])
        
    if i >= 3:
        features.extend([
            'char-3:0=' + sentence[i-3][0] + sentence[i-2][0] + sentence[i-1][0] + sentence[i][0],
            'char-3:-1=' + sentence[i-3][0] + sentence[i-2][0] + sentence[i-1][0],
        ])
        
        
    if i + 1 < len(sentence):
        features.extend([
            'char+1=' + sentence[i+1][0],
            'char:+1=' + sentence[i][0] + sentence[i+1][0],
        ])
    else:
        features.append("EOS")
        
    if i + 2 < len(sentence):
        features.extend([
            'char+2=' + sentence[i+2][0],
            'char:+2=' + sentence[i][0] + sentence[i+1][0] + sentence[i+2][0],
            'char+1:+2=' + sentence[i+1][0] + sentence[i+2][0],
        ])
        
    if i + 3 < len(sentence):
        features.extend([
            'char:+3=' + sentence[i][0] + sentence[i+1][0] + sentence[i+2][0]+ sentence[i+3][0],
            'char+1:+3=' + sentence[i+1][0] + sentence[i+2][0] + sentence[i+3][0],
        ])
    
    return features

def create_sentence_features(prepared_sentence):
    return [create_char_features(prepared_sentence, i) for i in range(len(prepared_sentence))]
    
    



def segment_sentence(sentence):
    tagger = pycrfsuite.Tagger()
    segmenter_file=os.path.join(os.path.dirname(__file__),'Word_Segmentation_Model/urdu-word-segmentation.crfsuite')
    tagger.open(segmenter_file)
    
    sentence = sentence.replace(" ", "")
    sentence = sentence.replace(u"\u200C", "") 
    
    prediction = tagger.tag(create_sentence_features(sentence))
    #print (prediction)
    complete = ""
    for i, p in enumerate(prediction):
        if p == "1":
            complete += " " + sentence[i]
            
            #print ("co = ", complete)
        elif p == "2":
            complete += u"\u200C" + sentence[i]
            
            
        else:
            complete += sentence[i]
            
    
    
     

    return complete

def lex_segment_sentence(sentence):

    
    lexicon_file=os.path.join(os.path.dirname(__file__),'lexicon.txt')
    f=codecs.open(lexicon_file, 'r', encoding='utf-8')
    reader=f.read()
    lex_words=reader.split('\r\n')

    seg_word_dict={}
    lex_seg=[]
    for word in lex_words:
        word=re.sub("\ufeff","",word)
        #print ("word = ", word)
        seg=segment_sentence(word)
        lex_seg.append(seg)
        #print ("seg = ", seg)
        seg_word_dict[seg]=word
    

    s=segment_sentence(sentence)
    #print ("s in =", s)
    for seg in lex_seg:
        if seg in s:
            s=s.replace(seg," "+seg_word_dict[seg]+" ")
    for word in lex_words:
        if word in s:
            s=s.replace(word," "+word+" ")
    
    s=s.replace(u"\u200C"," ")
            

    s=s.split()
    
    segmented_sentence=" ".join(s)
    return segmented_sentence
    
