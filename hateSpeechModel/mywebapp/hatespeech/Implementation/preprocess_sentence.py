# -*- coding: utf-8 -*-
"""
Created on Fri Apr 13 15:45:32 2018

@author: ETsham
"""

from collections import defaultdict
import re
import codecs
import string
import pandas as pd
import os
from . import segmenter
    

def build_data(s):
    vocab = defaultdict(float)
    
    
    word_stem_dict=stemmer()
    
    orig_rev = clean_str(s)
    
    orig_rev=" ".join(orig_rev.split())

    #tokenize text
    tokens = tokenize(orig_rev)
    
    #print ("tokens = ", tokens)
    for index, token in enumerate (tokens):
        if len(token)>7:
            #print ("long token = ", token)
            seg_token=segmenter.lex_segment_sentence(token)
            #print ("seg_token = ", seg_token)
            tokens[index]=seg_token
            
    
    orig_rev=" ".join(tokens)
    
    orig_rev=orig_rev.split()
    
    orig_rev=" ".join(orig_rev)
    orig_rev=remove_stopwords(orig_rev)
    orig_rev=stem(orig_rev, word_stem_dict)
    text=orig_rev
    words = set(orig_rev.split())
    for word in words:
        vocab[word] += 1
    
    print ("Text Preprocessing Done!")
    #print ("text = ", text)
    return text
def clean_str(s):
    """
    Tokenization/string cleaning. This is specific to tweets, but can be applied for other texts as well.
    """
    s=s+" "
    #print ("s = ",s)
    s=s.replace('\n',' ')
    #print ("line br = ",s)
    #Remove emojis
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F910-\U0001F928"
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U0001F100-\U0001FFFF"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
                           "]+")
    
    """emoji_pattern = re.compile("["
        u"\U0001F100-\U0001FFFF"  
                           "]+")"""
    

    s=emoji_pattern.sub(r'', s)

    #Remove English usernames
 
    s=re.sub("(@[A-Za-z0-9_]+)", "", s)
    #str = re.sub("(@[^A-Za-z0-9]+)", "", str)
    
    #Remove English hashtags
    #s = re.sub("(#[A-Za-z0-9_]+)", "", s)
            
    #Remove urdu hashtags
    #str = re.sub("#[۰-۹1-2آ-یے_]+", "", str)                    
     
    #Remove hyperlinks
    s=re.sub("http[^ ]*[\\\]","\\\\",s)                     
    s=re.sub("http[^ ]* "," ",s) 
    
    
    #Covert space separated compound words to their closed forms
    s = re.sub(  "بے غیرت","بیغیرت", s)
    s = re.sub(  "بے وقوف","بیوقوف", s)
    s = re.sub("دہشت گرد","دہشتگرد",s)
    #s = re.sub("دہشت گردی","دہشتگردی",s)
    s = re.sub("شدت پسند","شدتپسند",s)
    #s = re.sub("شدت پسندی","شدتپسندی",s)
    s = re.sub("حرام زادہ","حرامزادہ",s)
    s = re.sub("حرام زادی","حرامزادی",s)
    s = re.sub("حرام زادے","حرامزادے",s)
    s = re.sub("حرام خور","حرامخور",s)
    s = re.sub("اہل حدیث","اہلحدیث",s)
    s = re.sub("خر دماغ","خردماغ",s)
    s = re.sub("نمک حرام","نمکحرام",s)
    s = re.sub("بد بودار","بدبودار",s)
    s = re.sub("فٹے منہ","فٹےمنہ",s)
    s = re.sub("بد شکل","بدشکل",s)
   
    #Remove punctuations
    exclude = set(string.punctuation)
    for ch in exclude:
        s = s.replace(ch, " ") 
    
    s = s.replace("*", " ")
    s = s.replace("؟", " ")   
    s = s.replace("،", " ")                       
    s = s.replace("۔", " ")
    s = s.replace("٬", " ")
    s = s.replace("_", " ")
    s = s.replace("—", " ")
    s = s.replace("…", " ")
    s = s.replace("“", " ")
    s = s.replace("‘", " ")
    s = s.replace("’", " ")
    s = s.replace("”", " ")
    s = s.replace("‛", " ")
    s = s.replace("•", " ")  
    s = s.replace("؛", " ") 
    s = s.replace("ً", " ")  
    s = s.replace("ۤ", " ")  
    s = s.replace("ٗ", " ") 
    s = s.replace("ّ", " ")
    s = s.replace("ُ", " ")
    s = s.replace("ٰ", " ")
    s = s.replace("ٖ", " ")
    s = s.replace("ِ", " ")
    s = s.replace("َ", " ")
    s = s.replace("ۤ", " ")
    
    #print ("url, emoji, punc, usermenyion =",s)
    #Remove non urdu alphabet
    s=re.sub(r"[a-zA-Z?]", " ", s).strip()    
    
    #Remove digits
    s = re.sub("\d+", " ", s).strip()

    #print ("str = ", s)
    return s.strip()

def remove_stopwords(sentence):
    stopwords_file=os.path.join(os.path.dirname(__file__),'stopwords.txt')
    with codecs.open(stopwords_file, "r", encoding = "utf-8") as f:
        reader=(f.read())
        stopwords=reader.split("\n")
        

        meaningful_words = [w for w in sentence.split() if not w in stopwords]
        clean_sentence=" ".join(meaningful_words)
    
    return clean_sentence

def stemmer ():
    """
    create word to stem dictionary
    """
    word_stem_dict={}
    stemming_file=os.path.join(os.path.dirname(__file__),'Stemming_Output.txt')
    f=codecs.open(stemming_file, "r", encoding="utf-8")
    reader=f.read()
        
    for line in reader.split("\n"):
        line=re.sub("\ufeff","",line)
        #print ("line = ", line)
        words=line.strip().split('\t')[0]
        #print ("words = ", words)
        stem=line.strip().split("\t")[2]
        #print ("stem = ", stem)
        stems=re.sub("Stem: ","",stem)
        word_stem_dict[words]=stems
    return word_stem_dict
        

       
def stem(sent, word_stem_dict):
    """
    perform stemming of words in the corpus using word to stem dictionary
    """
    #print ("sent = ", sent)
    #word_to_stem=[word_stem_dict[w] for w in sent.split() if w in word_stem_dict]
    word_to_stem=[]
    for w in sent.split():
        if w in word_stem_dict:
            word_to_stem.append(word_stem_dict[w])
        else:
            word_to_stem.append(w)
    #print ("word_to_stem = ", word_to_stem)
    #sent=re.sub("(@[A-Za-z0-9_]+)", "", sent)
    return (" ".join(word_to_stem))

def tokenize(segment):
        segment = re.sub(",", " , ", segment)
        segment = re.sub("\.", " . ", segment)
        segment = re.sub("\|", " | ", segment)
        segment = re.sub("-", " - ", segment)
        segment = re.sub("\?", " ? ", segment)
        segment = re.sub("!", " ! ", segment)
        segment = re.sub("\"", " \" ", segment)
        segment = re.sub("\'", " ' ", segment)
        segment = re.sub("\(", " ( ", segment)
        segment = re.sub("\)", " ) ", segment)
        segment = re.sub("\{", " { ", segment)
        segment = re.sub("\{", " } ", segment)
        segment = re.sub("\<", " < ", segment)
        segment = re.sub("\>", " > ", segment)
        segment = re.sub("\;", " ; ", segment)
        segment = re.sub("\:", " : ", segment)
        
        segment = re.sub("\؟", " ? ", segment)
        segment = re.sub("،", " ، ", segment)                       
        segment = re.sub("۔ " ,"۔ ",  segment) 
        segment = re.sub("٬", " ٬ ", segment)
        segment = re.sub("_", " _ ", segment)
        segment = re.sub("—", " — ", segment)
        segment = re.sub("…", " … ", segment)
        segment = re.sub("“", " “ ", segment)
        segment = re.sub("‘", " ‘ ", segment)
        segment = re.sub("’", " ’ ", segment)
        segment = re.sub("”", " ” ", segment)
        segment = re.sub("‛", " ‛ ", segment)
        segment = re.sub("•", " • ", segment)  
        segment = re.sub("؛", "؛ ", segment) 
        
        segment = re.sub(u"\u0964", " "+u"\u0964"+" ", segment)
        segment = re.sub(u"\u0965", " "+u"\u0965"+" ", segment)
        segment = re.sub(u"\u09F7", " "+u"\u09F7"+" ", segment)
        segment = re.sub(u"\u09FB", " "+u"\u09FB"+" ", segment)
        
        segment = re.sub("\s+", " ", segment)
        segment = re.sub("&amp ;", "&amp;", segment)
        segment = re.sub("&quot ;", "&quot;", segment)
        segment = re.sub("&quote ;", "&quote;", segment)                
        
        tokens = segment.split()
        return tokens
"""s="قادیانیوں پہ لعنت ھو"
build_data(s)"""