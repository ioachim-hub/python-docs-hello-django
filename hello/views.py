from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Sentiment

import datetime
import uuid

from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from azure.storage.blob import BlobServiceClient

key = "6ea67e20bec5465ea0e2123b72a80a34"
endpoint = "https://ioachimsentiment.cognitiveservices.azure.com/"

connect_str = "DefaultEndpointsProtocol=https;AccountName=sentimentfiles;AccountKey=C3trnsUDVc47gX1+j+LFnefsmGsoeavYCHgDpWdQ8CZ3u9eM/qBuqMmu66QR6Um/w9ZAIZKUHPH/YKL5HY7hLA==;EndpointSuffix=core.windows.net"



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
        file = request.POST.get('file')
        
        local_file_name = str(uuid.uuid4()) + ".txt"
        
        destination =  open(local_file_name, 'w')
            
        destination.write(file)
            
        destination.close()
        

        
        file = open(local_file_name, 'r')
        documents = file.read()
        file.close()
        
        documents = [ documents ]
        
        output = sentiment_analysis_example(client, documents)
        
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)
        container_name = str(uuid.uuid4())
        container_client = blob_service_client.create_container(container_name)
        
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=local_file_name)
        
        with open(local_file_name, "rb") as data:
            blob_client.upload_blob(data)
            
        link = "https://sentimentfiles.blob.core.windows.net/" + container_name + "/" + local_file_name
        
        sentiment = Sentiment.objects.create(link     = link,
                                             data     = datetime.date,
                                             rezultat = output)
        sentiment.save()
        
        
    return redirect("home")

