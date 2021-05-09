from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Sentiment

from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

import datetime
import uuid

key = "6ea67e20bec5465ea0e2123b72a80a34"
endpoint = "https://ioachimsentiment.cognitiveservices.azure.com/"

connect_str = "DefaultEndpointsProtocol=https;AccountName=sentimentfiles;AccountKey=C3trnsUDVc47gX1+j+LFnefsmGsoeavYCHgDpWdQ8CZ3u9eM/qBuqMmu66QR6Um/w9ZAIZKUHPH/YKL5HY7hLA==;EndpointSuffix=core.windows.net"

def authenticate_client():
    ta_credential = AzureKeyCredential(key)
    text_analytics_client = TextAnalyticsClient(
            endpoint=endpoint, 
            credential=ta_credential)
    return text_analytics_client

def sentiment_analysis_example(client, documents):
    response = client.analyze_sentiment(documents=documents)[0]
    mesaj = ""
    mesaj += "Document Sentiment: {} \n".format(response.sentiment)
    mesaj += "Overall scores: positive={0:.2f}; neutral={1:.2f}; negative={2:.2f} \n".format(
        response.confidence_scores.positive,
        response.confidence_scores.neutral,
        response.confidence_scores.negative,
    )
    for idx, sentence in enumerate(response.sentences):
        mesaj += "Sentence: {} \n".format(sentence.text) 
        mesaj += "Sentence {} sentiment: {} \n".format(idx+1, sentence.sentiment)
        mesaj += "Sentence score:\nPositive={0:.2f}\nNeutral={1:.2f}\nNegative={2:.2f}\n".format(
            sentence.confidence_scores.positive,
            sentence.confidence_scores.neutral,
            sentence.confidence_scores.negative,
        )
    return mesaj



def hello(request):
    table = Sentiment.object.all()
    context = [
        'table' = table;
    ]
    return render(request, "home.html", context)

