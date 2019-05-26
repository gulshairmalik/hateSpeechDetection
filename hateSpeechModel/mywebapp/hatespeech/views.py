import os
import json
from django.shortcuts import render
from .Implementation import preprocess_sentence,hate,rel,eth,nat,offensive
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

def classify(request):
    #sent="قادیانیوں پہ لعنت ھو"
    
    if 'sentence' in request.POST:
        sent = request.POST['sentence']  
        sent=str(sent)
        sent=preprocess_sentence.build_data(sent)
        
    else:
        sent = "None"

    #print (sent)
    sent=preprocess_sentence.build_data(sent)
    sent=[sent]
    offensive_label=" "
    hate_label=" "
    hate_level=" "
    
    offensive_label=offensive.predict_label(sent)

    if offensive_label=="Offensive":
        hate_label = hate.predict_label(sent)
        if hate_label=="Religion":
            hate_level=rel.predict_label(sent)
        elif hate_label=="Ethnicity":
            hate_level=eth.predict_label(sent)
        elif hate_label=="National Origin":
            hate_level=nat.predict_label(sent)
        elif hate_label=="Not Hate Speech":
            hate_label="Not-Hate-Speech"
            hate_level="Not-Hate-Speech"
    else:
        offensive_label=offensive_label
        hate_label="Not-Hate-Speech"
        hate_level="Not-Hate-Speech"
    
    context = {'offensive_label': offensive_label, 'hate_label': hate_label, 'hate_level': hate_level}
    
    print ("offensive_label = ", offensive_label)
    print ("hate_label = ", hate_label)
    print ("hate_level = ", hate_level)
    

    return render(request, 'hatespeech/index.html',context)



@csrf_exempt
def classifyApi(request):

    if request.method == 'POST':
        data = json.loads(request.body.decode("utf-8"))
        sent = data['sentence'];  
        sent=str(sent)
        sent=preprocess_sentence.build_data(sent)
    else:
        sent = "None"

    sent=preprocess_sentence.build_data(sent)
    sent=[sent]
    offensive_label=" "
    hate_label=" "
    hate_level=" "
    
    offensive_label=offensive.predict_label(sent)

    # if offensive_label=="Offensive":
    #     hate_label = hate.predict_label(sent)
    #     if hate_label=="Religion":
    #         hate_level=rel.predict_label(sent)
    #     elif hate_label=="Ethnicity":
    #         hate_level=eth.predict_label(sent)
    #     elif hate_label=="National Origin":
    #         hate_level=nat.predict_label(sent)
    #     elif hate_label=="Not Hate Speech":
    #         hate_label="Not-Hate-Speech"
    #         hate_level="Not-Hate-Speech"
    # else:
    #     #offensive_label=offensive_label
    #     hate_label="Not-Hate-Speech"
    #     hate_level="Not-Hate-Speech"

    hate_label = hate.predict_label(sent)

    if hate_label=="Religion":
        hate_level=rel.predict_label(sent)
        offensive_label="Offensive"
    elif hate_label=="Ethnicity":
        hate_level=eth.predict_label(sent)
        offensive_label="Offensive"
    elif hate_label=="National Origin":
        hate_level=nat.predict_label(sent)
        offensive_label="Offensive"
    elif hate_label=="Not Hate Speech":
        hate_label="Not-Hate-Speech"
        hate_level="Not-Hate-Speech"
    
    
    response_data= {'offensive_label': offensive_label, 'hate_label': hate_label, 'hate_level': hate_level}
        
           
    return HttpResponse(json.dumps(response_data), content_type="application/json")

    #return HttpResponse("OK");