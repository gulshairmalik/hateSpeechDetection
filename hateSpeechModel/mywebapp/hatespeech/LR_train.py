# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 19:52:20 2018

@author: ETsham
"""

import sys

if len(sys.argv)<3 or len(sys.argv)>3:
    print ("Arguements invalid.")
    print ("\nUsage: script.py category features")
    print ("\ncategory: <ethnicity|nationality|religion|offensive>")
    print ("features: <slurs|wordngrams|charngrams|skipgrams|word2vec|fasttext|wordngrams+skipgrams|wordngrams+charngrams|charngrams+skipgrams|wordngrams+charngrams+skipgrams|all(word2vec)|all(fasttext)>")
    print ("\nExample Usage: LR_train.py ethnicity wordngrams")
    
    exit(0)

if sys.argv[1]=="ethnicity":
    training_file = 'Data/Train/eth_train'
    dirname="Ethnicity"
elif sys.argv[1]=="nationality":
    training_file = 'Data/Train/nat_train'
    dirname="Nationality"
elif sys.argv[1]=="religion":
    training_file = 'Data/Train/rel_train'
    dirname="Religion"
elif sys.argv[1]=="offensive":
    training_file = 'Data/Train/comb_train'
    dirname="Offensive"
else:
    print ("Arguements invalid.")
    print ("\nUsage: script.py category features")
    print ("\ncategory: <ethnicity|nationality|religion|offensive>")
    
    print ("features: <slurs|wordngrams|charngrams|skipgrams|word2vec|fasttext|wordngrams+skipgrams|wordngrams+charngrams|charngrams+skipgrams|wordngrams+charngrams+skipgrams|all(word2vec)|all(fasttext)>")
    print ("\nExample Usage: LR_train.py ethnicity wordngrams")
    exit(0)

features=sys.argv[2]
if features=="slurs"or features=="wordngrams"or features=="charngrams"or features=="skipgrams"or features=="word2vec"or features=="fasttext"or features=="wordngrams+skipgrams"or features=="wordngrams+charngrams"or features=="charngrams+skipgrams"or features=="wordngrams+charngrams+skipgrams"or features=="all(word2vec)"or features=="all(fasttext)":
    features=features
else:
    print ("Arguements invalid.")
    print ("\nUsage: script.py category features")
    print ("\ncategory: <ethnicity|nationality|religion|offensive>")
    print ("features: <slurs|wordngrams|charngrams|skipgrams|word2vec|fasttext|wordngrams+skipgrams|wordngrams+charngrams|charngrams+skipgrams|wordngrams+charngrams+skipgrams|all(word2vec)|all(fasttext)>")
    print ("\nExample Usage: LR_train.py ethnicity wordngrams")
    
    exit(0)

import datasets
import gensim
import numpy as np
import os
import pickle
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import FunctionTransformer
from sklearn.model_selection import GridSearchCV
#from toolz import itertoolz, compose
#from toolz.curried import map as cmap, sliding_window, pluck
from Embedding_Generator import TfidfEmbeddingVectorizer
from SkipgramGenerator import SkipGramVectorizer
from slurs import get_slurterms




w2v_file = "w2v/w2v_300.bin"
ft_file = "w2v/ft_300_wn2.bin"

print ("\nCategory = ", dirname)
print ("Training data = ", training_file)
print ("Features = ", features)
    
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


def load_fasttext(vocab):
    model=FastText(ft_file)
    print ("Fasttext Loaded...")
    word_vecs= {}
        
    for word in vocab:    
        word_vecs[word]=model.get_numpy_vector(word)
    return word_vecs

def load_word2vec(vocab):

    model = gensim.models.Word2Vec.load(w2v_file)
    print ("Word2vec Loaded...")
    word_vecs= {}
        
    for word in vocab:
        if word in model.wv.vocab:
            word_vecs[word]=model.wv[word]

    return word_vecs
                

def classify_slurterms():
        
    lr_clf_slurterms = Pipeline([
            ('features', FeatureUnion([
                ('hateful_words', Pipeline([
                    ('count', FunctionTransformer(get_slurterms, validate=False)),
                ])),
            ])),
            ('clf', GridSearchCV(LogisticRegression(class_weight='balanced', 
                    n_jobs=1, random_state=32, tol=0.2, solver='sag', multi_class='multinomial'),
                    param_grid={'C': [1, 5]},
                    scoring='accuracy', cv=5, refit='accuracy'))])
                
           
    return lr_clf_slurterms
    
    
def classify_wordngrams():   
    lr_clf_wordngrams = Pipeline([
            ('features', FeatureUnion([
                ('word_ngrams', Pipeline([
                    ('ngram_vectorizer', TfidfVectorizer(ngram_range=(1, 3)))
                ])), 
            ])),
           
            ('clf', GridSearchCV(LogisticRegression(class_weight='balanced',
                    n_jobs=1,random_state=32,solver='sag', tol=0.2, multi_class='multinomial'),
                    param_grid={'C': [1, 5]},verbose=10,
                    scoring='accuracy', cv=5, refit='accuracy'))]) 
    
    return lr_clf_wordngrams


def classify_skipgrams():

   
    lr_clf_skipgrams = Pipeline([
            ('features', FeatureUnion([
                ('skipgrams2', Pipeline([
                    ('skipgram_vectorizer2', SkipGramVectorizer(ngram_range=(2,2), k=3))
                ])),  
   
            ])),
            ('clf', GridSearchCV(LogisticRegression(class_weight='balanced',
                    n_jobs=1, random_state=32,solver='sag', tol=0.2,multi_class='multinomial'),
                    param_grid={'C': [1, 5]},verbose=10,
                    scoring='accuracy', cv=5, refit='accuracy'))])              
    
    return lr_clf_skipgrams


def classify_charngrams():   
    lr_clf_charngrams = Pipeline([
            ('features', FeatureUnion([
                ('charngrams', Pipeline([
                    ('charngrams_vectorizer', TfidfVectorizer(ngram_range=(3, 6), analyzer='char'))
                ])), 
            ])),
            ('clf', GridSearchCV(LogisticRegression(class_weight='balanced', 
                    n_jobs=1, random_state=32,solver='sag', tol=0.2, multi_class='multinomial'),
                    param_grid={'C': [1, 5]},verbose=10,
                    scoring='accuracy', cv=5, refit='accuracy'))])

                    
    return lr_clf_charngrams

def classify_wordvecs(word_vectors):
    word_vecs=word_vectors
    lr_clf_wordvecs = Pipeline([
            ('features', FeatureUnion([
                ('word_vecs', Pipeline([
                    ('wordvec_vectorizer', TfidfEmbeddingVectorizer(word_vecs))
                ])), 
            ])),
            ('clf', GridSearchCV(LogisticRegression(class_weight='balanced', 
                    n_jobs=1, random_state=32,tol=0.2,solver='sag',multi_class='multinomial'),
                    param_grid={'C': [1, 5]},verbose=1,
                    scoring='accuracy', cv=5, refit='accuracy'))])
                    

                    
    return lr_clf_wordvecs

def classify_wordngrams_charngrams():
    lr_clf_wng_cng = Pipeline([
            ('features', FeatureUnion([
                ('word_ngrams', Pipeline([
                    ('ngram_vectorizer', TfidfVectorizer(ngram_range=(1, 3)))
                ])),      
                ('char_ngrams', Pipeline([
                    ('chargram_vectorizer', TfidfVectorizer(ngram_range=(3, 6), analyzer='char'))
                ])), 
            ])),
            ('clf', GridSearchCV(LogisticRegression(class_weight='balanced', 
                    n_jobs=1, random_state=32,solver='sag', tol=0.2, multi_class='multinomial'),
                    param_grid={'C': [1, 5]},verbose=10,
                    scoring='accuracy', cv=5, refit='accuracy'))])

    
    return lr_clf_wng_cng

def classify_wordngrams_skipgrams():
    
    lr_clf_wng_sg = Pipeline([
            ('features', FeatureUnion([
                ('word_ngrams', Pipeline([
                    ('ngram_vectorizer', TfidfVectorizer(ngram_range=(1, 3)))
                ])),      
                ('skipgrams2', Pipeline([
                    ('skipgram_vectorizer2', SkipGramVectorizer(ngram_range=(2,2), k=3))
                ])),
            ])),
            ('clf', GridSearchCV(LogisticRegression(class_weight='balanced', 
                    n_jobs=1, random_state=32,solver='sag', tol=0.2, multi_class='multinomial'),
                    param_grid={'C': [1, 5]},verbose=10,
                    scoring='accuracy', cv=5, refit='accuracy'))])
   
    return lr_clf_wng_sg

def classify_charngrams_skipgrams():
    
    lr_clf_cng_sg = Pipeline([
            ('features', FeatureUnion([
                ('char_ngrams', Pipeline([
                    ('chargram_vectorizer', TfidfVectorizer(ngram_range=(3, 6), analyzer='char'))
                ])),      
                ('skipgrams2', Pipeline([
                    ('skipgram_vectorizer2', SkipGramVectorizer(ngram_range=(2,2), k=3))
                ])),   

            ])),
            ('clf', GridSearchCV(LogisticRegression(class_weight='balanced', 
                    n_jobs=1, random_state=32,solver='sag', tol=0.2, multi_class='multinomial'),
                    param_grid={'C': [1, 5]},verbose=10,
                    scoring='accuracy', cv=5, refit='accuracy'))])

    
    return lr_clf_cng_sg

def classify_wordngrams_charngrams_skipgrams():
    
    lr_clf_wng_cng_sg = Pipeline([
            ('features', FeatureUnion([
                ('word_ngrams', Pipeline([
                    ('ngram_vectorizer', TfidfVectorizer(ngram_range=(1, 3)))
                ])),
                ('char_ngrams', Pipeline([
                    ('chargram_vectorizer', TfidfVectorizer(ngram_range=(3, 6), analyzer='char'))
                ])),      
                ('skipgrams2', Pipeline([
                    ('skipgram_vectorizer2', SkipGramVectorizer(ngram_range=(2,2), k=3))
                ])),  

            ])),
            ('clf', GridSearchCV(LogisticRegression(class_weight='balanced', 
                    n_jobs=1, random_state=32,solver='sag', tol=0.2, multi_class='multinomial'),
                    param_grid={'C': [1, 5]},verbose=10,
                    scoring='accuracy', cv=5, refit='accuracy'))])
    

    
    return lr_clf_wng_cng_sg

def classify_allfeatures(word_vecs):
    
    lr_clf_all = Pipeline([
            ('features', FeatureUnion([
                ('hateful_words', Pipeline([
                    ('count', FunctionTransformer(get_slurterms, validate=False)),
                ])),
                ('word_vecs', Pipeline([
                    ('wordvec_vectorizer', TfidfEmbeddingVectorizer(word_vecs))
                ])), 
                ('word_ngrams', Pipeline([
                    ('ngram_vectorizer', TfidfVectorizer(ngram_range=(1, 3)))
                ])),    
                ('skipgrams2', Pipeline([
                    ('skipgram_vectorizer2', SkipGramVectorizer(ngram_range=(2,2), k=3))
                ])),  
                ('char_ngrams', Pipeline([
                    ('chargram_vectorizer', TfidfVectorizer(ngram_range=(3, 6), analyzer='char'))
                ])), 
            ])),
            ('clf', GridSearchCV(LogisticRegression(class_weight='balanced', 
                    n_jobs=1, random_state=32,solver='sag', tol=0.2, multi_class='multinomial'),
                    param_grid={'C': [1, 5]},verbose=10,
                    scoring='accuracy', cv=5, refit='accuracy'))])
                    
    return lr_clf_all

def save_model(clf,outputdir,modelname):      
    with open(outputdir+'/'+modelname+'.p', 'wb') as fid:
        pickle.dump(clf, fid) 
        


def fitting_the_model(lr_features):
    for clf, label in zip([lr_features], ['LR']):
        print ("\nClassifier =", label,"\n")
        
        clf.fit(text_train, actual_label_ids_train) 
        best_score = clf.named_steps['clf'].best_score_
        print("\nBest_score = ",best_score)
        print('\nBest model:', clf.named_steps['clf'].best_estimator_.get_params())
        
        outputdir="Results/"+label+"/"+dirname+"/"+features
        if not os.path.exists(outputdir):
            print ("\nOutput dir ",outputdir, " doesn't exist. Creating it")
            os.makedirs(outputdir)
            
        modelname=label+"_"+dirname+"_"+features
        
        print ("\nSaving the best model...")
        save_model(clf, outputdir, modelname) 
        
        print ("\nBest model is at Implementation/",outputdir+'/'+modelname+'.p')
     

#load training dataset
X_train, y_train, text_train, actual_label_ids_train, vocab_train, labels_train,sentences_train=loaddata(training_file)


if features=="slurs":
    lr_clf_slurterms = classify_slurterms()
    fitting_the_model(lr_clf_slurterms)
        
elif features=="wordngrams":
    lr_clf_wordngrams=classify_wordngrams()
    fitting_the_model(lr_clf_wordngrams)

elif features=="skipgrams":
    lr_clf_skipgrams=classify_skipgrams()
    fitting_the_model(lr_clf_skipgrams)
           
elif features=="charngrams":
    lr_clf_charngrams=classify_charngrams()
    fitting_the_model(lr_clf_charngrams)

elif features=="word2vec":  
    word_vecs=load_word2vec(vocab_train)    
    lr_clf_wordvecs=classify_wordvecs(word_vecs)
    fitting_the_model(lr_clf_wordvecs)
        
elif features=="fasttext": 
    from pyfasttext import FastText
    word_vecs=load_fasttext(vocab_train)
    lr_clf_wordvecs = classify_wordvecs(word_vecs)
    fitting_the_model(lr_clf_wordvecs)
    
elif features=="wordngrams+charngrams":
    lr_clf_wng_cng=classify_wordngrams_charngrams()
    fitting_the_model(lr_clf_wng_cng)
    
elif features=="wordngrams+skipgrams":
    lr_clf_wng_sg=classify_wordngrams_skipgrams()
    fitting_the_model(lr_clf_wng_sg)
    
elif features=="charngrams+skipgrams":
    lr_clf_cng_sg=classify_charngrams_skipgrams()
    fitting_the_model(lr_clf_cng_sg)
    
elif features=="wordngrams+charngrams+skipgrams":
    lr_clf_wng_cng_sg=classify_wordngrams_charngrams_skipgrams()
    fitting_the_model(lr_clf_wng_cng_sg)
    
elif features=="all(word2vec)":
    word_vecs=load_word2vec(vocab_train)
    lr_clf_all=classify_allfeatures(word_vecs)
    fitting_the_model(lr_clf_all)
    
elif features=="all(fasttext)":
    from pyfasttext import FastText
    word_vecs=load_fasttext(vocab_train)
    lr_clf_all=classify_allfeatures(word_vecs)
    fitting_the_model(lr_clf_all)

    


