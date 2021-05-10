from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import Sentiment

import datetime
import uuid

from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from azure.storage.blob import BlobServiceClient, BlobClient
from azure.storage.blob import PublicAccess

key = "6ea67e20bec5465ea0e2123b72a80a34"
endpoint = "https://ioachimsentiment.cognitiveservices.azure.com/"

connect_str = "DefaultEndpointsProtocol=https;AccountName=sentimentfiles;AccountKey=U0stv7+ORvDYPihq28MoIl+B1NZD4SGcu56xhW8UGgDFa6If+nILpTF2X8+gx+BfTuniYHvIC0PccB13jLUttA==;EndpointSuffix=core.windows.net"



def hello(request):
    if request.method == 'GET':
        table = Sentiment.objects.all()
        context = {
            'table' : table
        }
    return render(request, "home.html", context)



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


def hello_submit(request):
    if request.method == 'POST':
        client = authenticate_client()
        file =  request.FILES.get('file')
        
        local_file_name = str(uuid.uuid4()) + ".txt"
       
        with open(local_file_name, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        destination.close()
        
        file_ = open(local_file_name, 'r')
        documents = file_.read()
        file_.close()
        
        documents = [ documents ]
        
        output = sentiment_analysis_example(client, documents)
        
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)
        container_name = str(uuid.uuid4())
        container_client = blob_service_client.create_container(container_name, public_access=PublicAccess.Container)
        
        blob = BlobClient.from_connection_string(conn_str=connect_str, container_name=container_name, blob_name=local_file_name)

        with open(local_file_name, "rb") as data:
            blob.upload_blob(data)
            
        link = "https://sentimentfiles.blob.core.windows.net/" + container_name + "/" + local_file_name
        
        sentiment = Sentiment.objects.create(link     = link,
                                             data     = datetime.datetime.today(),
                                             rezultat = output)
        sentiment.save()
        
        
    return HttpResponseRedirect(reverse('home'))

