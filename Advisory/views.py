from django.shortcuts import render
from django.http import JsonResponse
from Helpers.tokens import token_required, get_user
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from  .models import Advice, AdviceCategory
from Helpers.methods import respond
from Authentication.models import UserDetail
from Inventory.models import FarmerCrop
from Advisory.models import AdviceCategory

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
        response['message'] = "It's not you, it's us. Please try again, we deserve a chance"
    return respond(response)

@token_required
@require_http_methods(['POST'])
@csrf_exempt
def get_advices_for_user(request):
    response = {}
    try:
        token = request.META.get('token')
        user = get_user(token)
        user = user.userdetail
        temp_crops = FarmerCrop.objects.filter(user=user)
        advices_set = {}
        for temp_crop in temp_crops:
            temp_advices = AdviceCategory.objects.filter(crop=temp_crop)
            for temp_advice in temp_advices:
                advices_set.add(temp_advice.advice)
        advices_list = []
        for advice in advices:
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
        response['message'] = "It's not you, it's us. Please try again, we deserve a chance"
    return respond(response)