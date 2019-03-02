from django.shortcuts import render
from Helpers.tokens import token_required, get_user
import json
from Helpers.methods import get_or_none, respond
from Authentication.models import Merchant
from Helpers.utils import assert_found
from Inventory.models import Product
from Helpers.serializers import get_model_json
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

@token_required
@require_http_methods(['POST'])
@csrf_exempt
def upload_product(request):
    data = json.loads(request.body)
    token = request.META.get('token')
    user = get_user(token)
    merchant_obj = get_or_none(Merchant, user__user = user)
    assert_found(merchant_obj, "No merchant object found")
    name = data['name']
    product_type = data['product_type']
    price = data['price']
    quantity = data['quantity']
    quantity_type = data['quantity_type']
    # image = request.FILES.get('product_image')
    product_obj = Product.objects.create(merchant = merchant_obj, name = name, product_type = product_type, price = price, quantity = quantity, quantity_type = quantity_type)
    product_obj.save()

    response = {}
    response['success'] = True
    response['message'] = "Product uploaded successfully"
    response['details'] = get_model_json(product_obj)
    return respond(response)

    