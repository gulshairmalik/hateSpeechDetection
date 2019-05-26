# -*- coding: utf-8 -*-
import numpy as np



class TfidfEmbeddingVectorizer(object):
    def __init__(self, word2vec):
        self.word2vec = word2vec
        #self.word2weight = None
        if len(word2vec)>0:
            self.dim=len(word2vec[next(iter(word2vec))])
        else:
            self.dim=0
        
    def fit(self, X, y):
        return self
    
    def transform(self, X):

        tokenized_text=[]
        for sent in X:
            sent=sent.split()
            tokenized_text.append(sent)
        X=tokenized_text
        
        return np.array([
                np.mean([self.word2vec[word]
                         for word in sentence if word in self.word2vec] or
                        [np.zeros(self.dim)], axis=0)
                for sentence in X
            ])
