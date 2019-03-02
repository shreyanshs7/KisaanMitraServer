from django.shortcuts import render
import requests
import json
from django.conf import settings
from Helpers.methods import respond
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from Helpers.tokens import token_required

# Create your views here.
# @token_required
@require_http_methods(['GET'])
@csrf_exempt
def news_feed(request):
    # token = request.META.get("token")
    query = request.GET.get('query')
    url = "https://newsapi.org/v2/everything"
    querystring = { "q":query,"sources":"the-hindu","apiKey": settings.NEWS_API_KEY }
    response = requests.request("GET", url, params=querystring)
    if response.status_code is 200:
        response = response.json()
        response['success'] = True
        return respond(response)
    response = {}
    response['success'] = False
    response['message'] = "Cannot fetch news currently"
    return respond(response)