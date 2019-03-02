from django.shortcuts import render
from Helpers.methods import respond
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from Helpers.tokens import token_required, get_user
import json
from Transaction.models import Rent
from Helpers.methods import get_or_none
from Inventory.models import Product
from Authentication.models import UserDetail
from Helpers.serializers import get_model_json
from Helpers.utils import assert_found
from dateutil.parser import parse

# Create your views here.
@require_http_methods(['POST'])
@token_required
@csrf_exempt
def rent(request):
    response = {}
    token = request.META.get('token')
    user = get_user(token)
    data = json.loads(request.body)
    product_id = data['product_id']
    quantity = data['quantity']
    duration_start = data['start']
    duration_end = data['end']
    duration_start = parse(duration_start)
    duration_end = parse(duration_end)
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
    response['details'] = get_model_json(rent_obj)
    return respond(response)

@token_required
@csrf_exempt
@require_http_methods(['POST'])
def rent_release(request):
    token = request.META.get('token')
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
