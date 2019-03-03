from django.shortcuts import render, redirect
from Helpers.tokens import token_required, get_user
import json
from Helpers.methods import get_or_none, respond
from Authentication.models import Merchant, UserDetail, Merchant
from Helpers.utils import assert_found
from Inventory.models import Product, FarmerCrop, Crop
from Helpers.serializers import get_model_json
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from Transaction.models import Rent
# Create your views here.

@token_required
@require_http_methods(['POST'])
@csrf_exempt
def upload_product(request):
    data = json.loads(request.body)
    token = request.META.get('HTTP_TOKEN')
    user = get_user(token)
    merchant_obj = get_or_none(Merchant, user__user = user)
    assert_found(merchant_obj, "No merchant object found")
    name = data['name']
    product_type = data['product_type']
    price = data['price']
    quantity = data['quantity']
    quantity_type = data['quantity_type']
    image = request.FILES.get('product_image')
    product_obj = Product.objects.create(merchant = merchant_obj, image = image,name = name, product_type = product_type, price = price, quantity = quantity, quantity_type = quantity_type)
    product_obj.save()

    response = {}
    response['success'] = True
    response['message'] = "Product uploaded successfully"
    response['details'] = get_model_json(product_obj)
    return respond(response)

@require_http_methods(['GET'])
@csrf_exempt
@token_required
def get_all_products(request):
    token = request.META.get('HTTP_TOKEN')
    user = get_user(token)
    # user_detail_obj = get_or_none(UserDetail, user = user)
    # assert_found(user_detail_obj, "No user detail object found")
    # merchant_obj = get_or_none(Merchant, user = user_detail_obj)
    # assert_found(merchant_obj, "No merchant object found")

    scheme = request.is_secure() and "https" or "http"
    all_products_obj = Product.objects.all()
    product_list = []
    for obj in all_products_obj:
        temp = {}
        temp['mechant_id'] = obj.merchant.id
        temp['merchant_name'] = obj.merchant.name
        temp['merchant_contact'] = obj.merchant.contact
        temp['merchant_address'] = obj.merchant.address
        temp['product_id'] = obj.id
        temp['name'] = obj.name
        temp['product_type'] = obj.product_type
        temp['sell_price'] = obj.sell_price
        temp['rent_price'] = obj.rent_price
        temp['sell_type'] = obj.sell_type
        temp['quantity'] = obj.quantity
        temp['period'] = obj.period
        temp['product_image'] = scheme + '://' + request.META['HTTP_HOST'] + '/media/' + str(obj.image)
        temp['quantity_type'] = obj.quantity_type
        product_list.append(temp)
    response = {}
    response['success'] = True
    response['message'] = "Products list"
    response['product_list'] = product_list
    return respond(response)

@token_required
@require_http_methods(['POST'])
@csrf_exempt
def update_product(request):
    token = request.META.get('HTTP_TOKEN')
    user = get_user(token)
    data = json.loads(request.body)
    product_id = data['product_id']
    product_obj = get_or_none(Product, id = product_id)
    assert_found(product_obj, "No product object found")
    product_obj.name = data['name']
    product_obj.product_type = data['product_type']
    product_obj.sell_price = data['sell_price']
    product_obj.rent_price = data['rent_price']
    product_obj.sell_type = data['sell_type']
    product_obj.quantity = data['quantity']
    product_obj.period = data['period']
    product_obj.quanity_type = data['quantity_type']

    product_obj.save()
    response = {}
    response['success'] = True
    response['message'] = "Product details updated successfully"
    response['product_detail'] = get_model_json(product_obj)
    return respond(response)

@token_required
@require_http_methods(['GET'])
@csrf_exempt
def update_crop(request):
    response = {}
    token = request.META.get('HTTP_TOKEN')
    user = get_user(token)
    crop_id = request.GET.get('crop_id')
    crop_obj = get_or_none(Crop, id = crop_id )
    assert_found(crop_obj, "No crop object found")
    user_detail_obj = get_or_none(UserDetail, user = user)
    assert_found(user_detail_obj, "No user detail object found")
    try:
        farmer_crop = FarmerCrop.objects.get(user = user_detail_obj, crop = crop_obj)
    except FarmerCrop.DoesNotExist:
        farmer_crop_obj = FarmerCrop.objects.create(user = user_detail_obj, crop = crop_obj)    
        farmer_crop_obj.save()
        farmer_crop = FarmerCrop.objects.filter(user = user_detail_obj)
        response['success'] = True
        response['message'] = "Crop added successfully"
        response['detail'] = get_model_json(farmer_crop_obj)
        return respond(response)
    response['success'] = False
    response['message'] = "You've already added this crop"
    return respond(response)

@csrf_exempt
def get_all_crops(request):
    crop_obj = Crop.objects.all()
    crop_list = []
    for obj in crop_obj:
        temp = {}
        temp['crop_id'] = obj.id
        temp['crop_type'] = obj.crop_type
        temp['season'] = obj.season
        temp['name'] = obj.name
        crop_list.append(temp)
    response = {}
    response['success'] = True
    response['crop_list'] = crop_list
    response['message'] = "Crops list"
    return respond(response)

@token_required
@csrf_exempt
@require_http_methods(['GET'])
def get_crops_by_user(request):
    response = {}
    token = request.META.get("HTTP_TOKEN")
    user = get_user(token)
    user_detail_obj = user.userdetail
    farmer_crop_obj = FarmerCrop.objects.filter(user = user_detail_obj)
    farmer_crop_list = []
    if farmer_crop_obj is None:
        response['success'] = False
        response['message'] = "No crop selected"
        response['farmer_crop_list'] = farmer_crop_list
        return respond(response)
    assert_found(farmer_crop_obj, "No farmer crop object found")
    for obj in farmer_crop_obj:
        temp = {}
        temp['crop_name'] = obj.crop.name
        temp['crop_type'] = obj.crop.crop_type
        temp['season'] = obj.crop.season
        farmer_crop_list.append(temp)
    response['success'] = True
    response['farmer_crop_list'] = farmer_crop_list
    return respond(response)

@require_http_methods(['GET'])
@token_required
@csrf_exempt
def delete_crop_user(request):
    token = request.META.get('HTTP_TOKEN')
    user = get_user(token)
    crop_id = request.GET.get('crop_id')
    crop_obj = get_or_none(Crop, id = crop_id)
    user_detail_obj = user.userdetail
    farmer_crop_obj = FarmerCrop.objects.get(user = user_detail_obj, crop = crop_obj )
    assert_found(farmer_crop_obj, "No Farmer crop object found")
    farmer_crop_obj.delete()
    response = {}
    response['success'] = True
    response['message'] = "Crop deleted successfully"
    return respond(response)

def farmer_dashboard(request):
    temp_products = Product.objects.all()
    length = len(temp_products)
    paginator = Paginator(temp_products, 3)
    products = []
    for i in paginator.page_range:
        data = iter(paginator.get_page(i))
        products.append(data)
    context = {}
    context['products'] = products
    return render(request,'farmerdashboard.html', context=context)
    
@login_required
def rent_signup(request):
    user = request.user 
    if user.userdetail.user_type == 'RETAILER':
        return redirect('/rent/dashboard')
    else:
        return render(request, 'rent.html')

@login_required
def rent_confirm_signup(request):
    user = request.user 
    if user.userdetail.user_type != 'RETAILER':
        user = request.user 
        user = user.userdetail
        user.user_type = 'RETAILER'
        user.save()
        temp_merchant = Merchant(user=user, name=user.user.first_name)
        temp_merchant.save()
        # print(user.userdetail.user_type == 'RETAILER')
    return redirect('/rent/dashboard')

@login_required
def retailer_dashboard(request):
    temp_merchant = Merchant.objects.get(user=request.user.userdetail)
    temp_products = Product.objects.filter(merchant=temp_merchant)
    paginator = Paginator(temp_products, 3)
    products = []
    for i in paginator.page_range:
        data = iter(paginator.get_page(i))
        products.append(data)
    context = {}
    context['products'] = products
    return render(request, 'retailerdashboard.html', context=context)

@login_required
def retailer_dashboard_add(request):
    if request.method == "POST":
        user = request.user
        user = user.userdetail
        name = request.POST['name']
        product_type = request.POST['product_type']
        sell_price = request.POST['sell_price']
        rent_price = request.POST['rent_price']
        sell_type = request.POST['sell_type']
        quantity = request.POST['quantity']
        period = request.POST['period_type']
        quantity_type = request.POST['quantity_type']
        image = request.FILES['image']
        temp_merchant = get_or_none(Merchant, user=user)
        assert_found(temp_merchant, "no merchant object found")
        temp_product = Product(merchant=temp_merchant, name=name, product_type=product_type, sell_price=sell_price, rent_price=rent_price, sell_type=sell_type, quantity=quantity, period=period, quantity_type=quantity_type, image=image)
        temp_product.save()        
        return redirect('/rent/dashboard')
    else:
        return render(request, 'retailer_dashboard_add.html')

@login_required
def retailer_dashboard_transactions(request):
    user = request.user
    user = user.userdetail
    temp_merchant = Merchant.objects.get(user=user)
    temp_products = Product.objects.filter(merchant=temp_merchant)
    rents = []
    for temp_product in temp_products:
        temp_rents = Rent.objects.filter(product=temp_product)
        print(temp_rents)
        for temp_rent in temp_rents:
            rents.append(temp_rent)
    context = {}
    context['rents'] = rents
    return render(request, 'transactions.html', context=context)