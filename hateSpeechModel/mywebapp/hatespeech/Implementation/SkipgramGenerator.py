#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 29 20:38:56 2018

@author: ramsha
"""

import nltk
from itertools import combinations
from toolz import compose
from sklearn.feature_extraction.text import TfidfVectorizer

class SkipGramVectorizer(TfidfVectorizer):

    def __init__(self, k=1, **kwds):
        super(SkipGramVectorizer, self).__init__(**kwds)
        self.k=k
        

    def build_sent_analyzer(self, tokenize):
        return lambda sent : self._word_skip_grams(
                compose(tokenize, self.decode)(sent))

    def build_analyzer(self):    
        tokenize = self.build_tokenizer()
        sent_analyze = self.build_sent_analyzer(tokenize)

        return lambda doc : self._sent_skip_grams(doc, sent_analyze)

    def _sent_skip_grams(self, doc, sent_analyze):
        skip_grams = []
        for sent in nltk.sent_tokenize(doc):
            skip_grams.extend(sent_analyze(sent))
        return skip_grams

    def _word_skip_grams(self, tokens):
        """Turn tokens into a sequence of n-grams after stop words filtering"""

        # handle token n-grams
        min_n, max_n = self.ngram_range
        k = self.k
        if max_n != 1:
            original_tokens = tokens
            if min_n == 1:
                # no need to do any slicing for unigrams
                # just iterate through the original tokens
                tokens = list(original_tokens)
                min_n += 1
            else:
                tokens = []

            n_original_tokens = len(original_tokens)

            # bind method outside of loop to reduce overhead
            tokens_append = tokens.append
            space_join = " ".join

            for n in range(min_n,
                            min(max_n + 1, n_original_tokens + 1)):
                for i in range(n_original_tokens - n + 1):
                    # k-skip-n-grams
                    head = [original_tokens[i]]                    
                    for skip_tail in combinations(original_tokens[i+1:i+n+k], n-1):
                        tokens_append(space_join(head + list(skip_tail)))
        return tokens

"""text = ['Insurgents killed in ongoing fighting.']
vectorizer = SkipGramVectorizer(ngram_range=(2,3), k=2)
vectorizer.fit_transform(text)
print(vectorizer.get_feature_names())"""

