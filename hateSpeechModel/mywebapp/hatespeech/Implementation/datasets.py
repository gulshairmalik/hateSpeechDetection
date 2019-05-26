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
import segmenter
    

def build_data(fname):
    sentences = []
    vocab = defaultdict(float)
    labels=[]
    rows = []
    
    word_stem_dict=stemmer()
    
    df =  pd.read_excel(fname+".xlsx")
    num_sents=df['text'].size
        
    count = 0
    for i in range( 0, num_sents ):
        if count%1000 == 0:
            print ("Reading line no. ",count)
        count+=1 
        label = (str(df['labels'][i]))
        
        rows.append((label, df['text'][i]))  # Tuple: (label,text)
        labels=labels+[label]

    labels = list(set(labels))
    labels.sort()
    print ("Labels = ", labels)
    labelIdToLabel = dict(zip(labels,range(len(labels))))
    text=[]
    for row in rows:
        y=labelIdToLabel[row[0]]
        rev = []
        rev.append(row[1].strip())
       
        orig_rev = clean_str(" ".join(rev))
        
        
        orig_rev=" ".join(orig_rev.split())
        
        #tokenize text
        tokens = tokenize(orig_rev)
    
        #segment tokens with length greater than 7 
        for index, token in enumerate (tokens):
            if len(token)>7:
                seg_token=segmenter.lex_segment_sentence(token)
                tokens[index]=seg_token
                
        
        orig_rev=" ".join(tokens)
        orig_rev=orig_rev.split()
        orig_rev=" ".join(orig_rev)
        orig_rev=remove_stopwords(orig_rev)
        orig_rev=stem(orig_rev, word_stem_dict)
        
        text.append(orig_rev)
        words = set(orig_rev.split())
        for word in words:
            vocab[word] += 1

        datum  = {"y":y,
                  "text": orig_rev,
                  "num_words": len(orig_rev.split()),
                  "hate_category": row[0],
                  "orig_sentence":row[1],
                  }
        
        
        sentences.append(datum)
    l=0
    for i in text:
        l=l+len(i.split())
    
    print ("Text Preprocessing Done!")
    return text, sentences, vocab, labels


def clean_str(s):
    """
    String cleaning. This is specific to tweets, but can be applied for other texts as well.
    """
    s=s+" "
    
    s=s.replace('\n',' ')
    
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
    

    s=emoji_pattern.sub(r'', s)
    
    #Remove English usernames
    s=re.sub("(@[A-Za-z0-9_]+)", "", s)

    #Remove hyperlinks
    s=re.sub("http[^ ]*[\\\]","\\\\",s)                     
    s=re.sub("http[^ ]* "," ",s) 
    
    #Covert space separated (open) compound words to their closed forms
    s = re.sub(  "بے غیرت","بیغیرت", s)
    s = re.sub(  "بے وقوف","بیوقوف", s)
    s = re.sub("دہشت گرد","دہشتگرد",s)
    s = re.sub("شدت پسند","شدتپسند",s)
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

    #Remove non urdu alphabet
    s=re.sub(r"[a-zA-Z?]", " ", s).strip()    
    
    #Remove digits
    s = re.sub("\d+", " ", s).strip()

    return s.strip()

def remove_stopwords(sentence):
    """
    remove stopwords
    """
    with codecs.open("stopwords.txt", "r", encoding = "utf-8") as f:
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
    with codecs. open("Stemming_Output.txt", "r", encoding="utf-8") as f:
        reader=f.read()
        
        for line in reader.split("\n"):
            line=re.sub("\ufeff","",line)
            words=line.strip().split('\t')[0]
            stem=line.strip().split("\t")[2]
            stems=re.sub("Stem: ","",stem)
            word_stem_dict[words]=stems
        return word_stem_dict
        

       
def stem(sent, word_stem_dict):
    """
    perform stemming of words in the corpus using word to stem dictionary
    """
    word_to_stem=[]
    for w in sent.split():
        if w in word_stem_dict:
            word_to_stem.append(word_stem_dict[w])
        else:
            word_to_stem.append(w)
    return (" ".join(word_to_stem))

def tokenize(segment):
    """
    tokenization
    """
    
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
