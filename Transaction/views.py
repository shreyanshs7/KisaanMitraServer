from django.shortcuts import render
from Helpers.methods import respond
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from Helpers.tokens import token_required, get_user
import json
from Transaction.models import Rent
from Helpers.methods import get_or_none
from Inventory.models import Product
from Authentication.models import UserDetail, Merchant
from Helpers.serializers import get_model_json
from Helpers.utils import assert_found
from dateutil.parser import parse

# Create your views here.
@require_http_methods(['POST'])
@token_required
@csrf_exempt
def rent(request):
    response = {}
    token = request.META.get('HTTP_TOKEN')
    user = get_user(token)
    data = json.loads(request.body)
    product_id = data['product_id']
    quantity = data['quantity']
    duration_start = data['start']
    duration_end = data['end']
    print(duration_start)
    print(duration_end)
    duration_start = parse(duration_start)
    duration_end = parse(duration_end)
    # if duration_end is None and duration_start is None:
    #     print("SOmething")
    product_obj = get_or_none(Product, id = product_id)
    assert_found(product_obj, "No product object found")
    if product_obj.quantity < quantity:
        response['success'] = False
        response['message'] = "Total available quantity is less"
        return respond(response)
    product_obj.quantity = product_obj.quantity - quantity
    user_detail_obj = get_or_none(UserDetail, user = user)
    assert_found(user_detail_obj, "No user detail object found")
    price = float(product_obj.rent_price * quantity)
    rent_obj = Rent.objects.create(product = product_obj, user = user_detail_obj, price = price, quantity = quantity, duration_start = duration_start, duration_end = duration_end)
    rent_obj.save()

    response['success'] = True
    response['message'] = "Product taken for rent successfully"
    # response['details'] = get_model_json(rent_obj)
    return respond(response)

@token_required
@csrf_exempt
@require_http_methods(['POST'])
def rent_release(request):
    token = request.META.get('HTTP_TOKEN')
    user = get_user(token)
    data = json.loads(request.body)
    rent_id = data['rent_id']
    rent_obj = get_or_none(Rent, id = rent_id)
    assert_found(rent_obj, "No rent object found")
    rent_obj.rent_completed = True
    rent_obj.save()
    response = {}
    response['success'] = True
    response['message'] = "Rented product duration completed"
    return respond(response)

@token_required
@csrf_exempt
def get_all_rent(request):
    token = request.META.get('HTTP_TOKEN')
    user = get_user(token)
    user_detail_obj = get_or_none(UserDetail, user = user)
    assert_found(user_detail_obj, "No user detail object found")
    all_rent_obj = Rent.objects.filter(user = user_detail_obj)
    all_rent_list = []
    for obj in all_rent_obj:
        temp =  {}
        temp['product_name'] = obj.product.name
        temp['rent_id'] = obj.id
        temp['price'] = obj.price
        temp['quantity'] = obj.quantity
        temp['status'] = obj.rent_completed
        temp['duration_start'] = str(obj.duration_start)
        temp['duration_end'] = str(obj.duration_end)
        all_rent_list.append(temp)
    response = {}
    response['success'] = True
    response['message'] = "Rent list"
    response['rent_list'] = all_rent_list
    return respond(response)

@require_http_methods(['GET'])
def get_merchant_rent_request(request):
    user = request.user
    user_detail_obj = user.userdetail
    merchant_obj = get_or_none(Merchant, user = user_detail_obj)
    assert_found(merchant_obj, "No merchant object found")
    product_obj = Product.objects.filter(merchant = merchant_obj)
    product_list = []
    for pro_obj in product_obj:
        temp = {}
        temp['product_id'] = pro_obj.id
        temp['product_name'] = pro_obj.name
        temp_merchant_rent_obj = Rent.objects.filter(product = pro_obj)
        rent_list = []
        for rent_obj in temp_merchant_rent_obj:
            var = {}
            var['rent_id'] = rent_obj.id
            var['user_id'] = rent_obj.user.user.id
            var['user_name'] = rent_obj.user.full_name
            var['price'] = rent_obj.price
            var['quantity'] = rent_obj.quantity
            start = parse(rent_obj.duration_start)
            var['duration_start'] = start.strftime('%d %B, %Y')
            end = parse(rent_obj.duration_end)
            var['duration_end'] = end.strftime('%d %B, %Y')
            rent_list.append(var)
        temp['rents'] = rent_list
        product_list.append(temp)
    response = {}
    response['success'] = True
    response['message'] = "Rent requests"
    response['request_list'] = product_list
    return respond(response)

@require_http_methods(['GET'])
def accept_rent_request(request):
    user = request.user
    rent_id = request.GET.get('rent_id')
    rent_obj = get_or_none(Rent, id = rent_id)
    rent_obj.rent_completed = True
    rent_obj.save()
    response = {}
    response['success'] = True
    response['message'] = "Rent request accepted"
    return respond(response)