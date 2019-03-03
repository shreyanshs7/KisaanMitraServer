from django.shortcuts import render
from django.http import JsonResponse
from Helpers.tokens import token_required, get_user
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from Helpers.methods import respond
from Authentication.models import UserDetail
from Inventory.models import FarmerCrop, Crop
from Advisory.models import AdviceCategory
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from Inventory.models import FarmerCrop
from Advisory.models import AdviceCategory, Advice

# Create your views here.

def get_all_advices(request):
    response = {}
    try:
        scheme = request.is_secure() and "https" or "http"
        advices_list = []
        temp_advices = Advice.objects.all()
        for temp_advice in temp_advices:
            advice = {}
            advice['id'] = temp_advice.pk
            advice['title'] = temp_advice.title
            advice['description'] = temp_advice.description
            advice['author'] = str(temp_advice.user)
            advice['image_url'] = scheme + '://' + request.META['HTTP_HOST'] + '/media/' +str(temp_advice.image)
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
        scheme = request.is_secure() and "https" or "http"
        token = request.META.get('HTTP_TOKEN')
        user = get_user(token)
        user = user.userdetail
        temp_crops = FarmerCrop.objects.filter(user=user)
        advices_set = {}
        for temp_crop in temp_crops:
            temp_advices = AdviceCategory.objects.filter(crop=temp_crop)
            for temp_advice in temp_advices:
                advices_set.add(temp_advice.advice)
        advices_list = []
        for advice in advices_set:
            advice = {}
            advice['id'] = temp_advice.pk
            advice['title'] = temp_advice.title
            advice['description'] = temp_advice.description
            advice['author'] = str(temp_advice.user)
            advice['image_url'] = scheme + '://' + request.META['HTTP_HOST'] + '/media/' +str(temp_advice.image)
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

def home(request):
    return render(request, 'home.html')

def dashboard(request):
    temp_advices = Advice.objects.filter(user=request.user.userdetail)
    length = len(temp_advices)
    paginator = Paginator(temp_advices, 4)
    advices = []
    for i in paginator.page_range:
        data = iter(paginator.get_page(i))
        advices.append(data)

    context = {}
    context['advices'] = advices
    context['length'] = length
    return render(request, 'dashboard.html', context=context)

def create(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        cover = request.FILES['cover']
        advice = Advice(title=title, description = description, user=request.user.userdetail, image=cover)
        advice.save()
        crops = Crop.objects.all()
        for crop in crops:
            try:
                if request.POST['crop_'+str(crop.pk)] == 'on':
                    print(crop.name)
                    advice_category = AdviceCategory(advice=advice, crop = crop)
                    advice_category.save()
            except:
                print("This crop is not checked")
        return redirect('/advisory/dashboard')
    else:
        crops = Crop.objects.all()
        context = {}
        context['crops'] = crops
        return render(request, 'create.html', context=context)

def edit(request, id):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        cover = request.FILES['cover']
        advice = Advice.objects.get(pk=id)
        advice.title = title
        advice.description = description
        advice.user = request.user.userdetail
        advice.image = cover
        advice.save()
        crops = Crop.objects.all()
        for crop in crops:
            try:
                if request.POST['crop_'+str(crop.pk)] == 'on':
                    print(crop.name)
                    if not AdviceCategory.objects.filter(advice=advice, crop = crop).exists():
                        advice_category = AdviceCategory(advice=advice, crop = crop)
                        advice_category.save()
            except:
                if AdviceCategory.objects.filter(advice=advice, crop = crop).exists():
                    AdviceCategory.objects.get(advice=advice, crop = crop).delete()
                print("This crop is not checked")
        return redirect('/advisory/dashboard')
    else:
        advice = Advice.objects.get(pk=id)
        final_crops = []
        related_crops = AdviceCategory.objects.filter(advice=advice)
        for related_crop in related_crops:
            final_crops.append(related_crop)
        context = {}
        crops = Crop.objects.all()
        context['title'] = advice.title
        context['description'] = advice.description
        context['related_crops'] = final_crops
        context['crops'] = crops
        return render(request, 'edit.html', context=context)

def web_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.get(email=email)
        user = authenticate(username=user.username, password=password)
    else:
        return render(request, 'login.html')

def web_register(request):
    if request.method == 'POST':
        # email = request.POST['email']
        # password = request.POST['password']
        # user = User.objects.get(email=email)
        # user = authenticate(username=user.username, password=password)
        print("Register")
    else:
        return render(request, 'register.html')