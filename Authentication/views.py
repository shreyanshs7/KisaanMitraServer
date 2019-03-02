from django.shortcuts import render
from Helpers.methods import respond, get_or_none
import json
from django.contrib.auth.models import User
from Helpers.utils import assert_found, assert_true
from Helpers.tokens import generate_token
from Authentication.models import UserDetail, FcmModel, Merchant
from Helpers.tokens import token_required, get_user
from Helpers.serializers import get_model_json
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@require_http_methods(['POST'])
@csrf_exempt
def login(request):
    response = {}
    data = json.loads(request.body)
    username = data['username']
    password = data['password']
  
    user = get_or_none(User, username = username)
    # assert_found(user, "Account with username not found")

    if user is None:
        response['success'] = False
        response['message'] = "User with username not found"
        return respond(response)
    if user.check_password(password):
        response['success'] = True
        response['token'] = generate_token(user) 
        return respond(response)
    else:
        response['success'] = False
        response['message'] = "Invalid Credentials"
    return respond(response)

@require_http_methods(['POST'])
@csrf_exempt
def register(request):
    response = {}
    data = json.loads(request.body)
    username = data['username']
    password = data['password']
    first_name = data['first_name']
    last_name = data['last_name']
    user_type = data['user_type']
    contact = data['contact']
    email = data['email']
    # latitude = data['latitude']
    # longitude = data['longitude']
    # fcm_token = data['fcm_token']

    user = get_or_none(User, username = username)
    # assert_true(user != None, "User with username already exists")

    if user is not None:
        response['success'] = False
        response['message'] = "User with username already exists"
        return respond(response)

    user_obj = User.objects.create_user(username = username, password = password)
    user_obj.save()

    user_obj.userdetail.first_name = first_name
    user_obj.userdetail.last_name = last_name
    user_obj.userdetail.user_type = user_type
    user_obj.userdetail.contact = contact
    user_obj.userdetail.email = email
    # user_obj.userdetail.latitude = latitude
    # user_obj.userdetail.longitude = longitude
    user_obj.userdetail.save()

    #Fcm register
    # device = FcmModel.objects.create(user = user_obj.userdetail, token = fcm_token, contact = contact)
    # device.save()

    response['success'] = True
    response['message'] = "Registration completed"
    return respond(response)

@token_required
@require_http_methods(['POST'])
@csrf_exempt
def register_merchant(request):
    data = json.loads(request.body)
    token = request.META.get("HTTP_TOKEN")
    user = get_user(token)
    name = data['name']
    email = data['email']
    address = data['address']
    contact = data['contact']

    user_detail_object = get_or_none(UserDetail, user = user)
    assert_found(user_detail_object, "No user detail object found")
    merchant_obj = Merchant.objects.create(user = user_detail_object, name = name, email = email, address = address, contact = contact)
    merchant_obj.save()

    response = {}
    response['success'] = True
    response['message'] = "Merchant created successfully"
    response['details'] = get_model_json(merchant_obj)
    return respond(response)