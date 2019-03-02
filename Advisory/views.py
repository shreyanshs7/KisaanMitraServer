from django.shortcuts import render
from django.http import JsonResponse
from  .models import Advice, AdviceCategory
from Helpers.methods import respond

# Create your views here.

def get_all_advices(request):
    response = {}
    try:
        advices_list = []
        temp_advices = Advice.objects.all()
        for temp_advice in temp_advices:
            advice = {}
            advice['title'] = temp_advice.title
            advice['description'] = temp_advice.description
            advice['author'] = str(temp_advice.user)
            categories = []
            temp_categories = AdviceCategory.objects.filter(advice=temp_advice)
            for temp_category in temp_categories:
                category = {}
                category['name'] = temp_category.crop.name
                category['crop_type'] = temp_category.crop.crop_type
                category['season'] = temp_category.crop.season
                categories.append(category)
            advice['categories'] = categories
            advices_list.append(advice)
        response['success'] = True
        response['data'] = advices_list
    except:
        response['success'] = False
        response['message'] = "Kuchh ho gaya"
    return respond(response)

def get_advices_for_user(request):
    response = {}
    try:
        advices_list = []
        temp_advices = Advice.objects.all()
        for temp_advice in temp_advices:
            advice = {}
            advice['title'] = temp_advice.title
            advice['description'] = temp_advice.description
            advice['author'] = str(temp_advice.user)
            categories = []
            temp_categories = AdviceCategory.objects.filter(advice=temp_advice)
            for temp_category in temp_categories:
                category = {}
                category['name'] = temp_category.crop.name
                category['crop_type'] = temp_category.crop.crop_type
                category['season'] = temp_category.crop.season
                categories.append(category)
            advice['categories'] = categories
            advices_list.append(advice)
        response['success'] = True
        response['data'] = advices_list
    except:
        response['success'] = False
        response['message'] = "Kuchh ho gaya"
    return respond(response)