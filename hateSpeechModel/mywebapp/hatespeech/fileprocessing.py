# -*- coding: utf-8 -*-


# Create your views here.


#outputdir=str(prev_dir)+"/Implementation/"


import os
"""sys.path.insert(0, "E:/Project/")

two_dir_up_path=os.path.abspath('../..')
two_dir_up_path=two_dir_up_path.replace('\\', '/')
#print (two_dir_up_path)
sys.path.insert(0, two_dir_up_path+"/")"""

#print (sys.path)

#from Implementation import preprocess_sentence,segmenter

from django.shortcuts import render
from .Implementation import preprocess_sentence,hate_file,rel_file,eth_file,nat_file

from django.http import HttpResponse

def classify(request):
    #sentence=["قادیانی کافر ہیں"]

    hate_label=" "
    hate_level=" "
    hate_label = hate_file.predict_label()
    if hate_label=="Religion":
        hate_level=rel_file.predict_label()
    elif hate_label=="Ethnicity":
        hate_level=eth_file.predict_label()
    elif hate_label=="National Origin":
        hate_level=nat_file.predict_label()
    elif hate_label=="Not Hate Speech":
        hate_label="Not-Hate-Speech"
        hate_level="Not-Hate-Speech"
    context = {'hate_label': hate_label, 'hate_level': hate_level}

    return render(request, 'hatespeech/index.html',context)