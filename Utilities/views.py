from django.shortcuts import render
import requests
import json
from django.conf import settings
from Helpers.methods import respond

# Create your views here.
def news_feed(request):
    data = json.loads(request.body)
    query = data['query']
    url = "https://newsapi.org/v2/everything"
    querystring = { "q":query,"sources":"the-hindu","apiKey": settings.NEWS_API_KEY }
    response = requests.request("GET", url, params=querystring)
    if response.status_code is 200:
        response = response.json()
        return respond(response)
    response = {}
    response['success'] = False
    response['message'] = "Cannot fetch news currently"
    return respond(response)