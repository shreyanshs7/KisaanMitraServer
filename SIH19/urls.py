"""SIH19 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from Authentication.views import login, register, register_merchant
from Inventory.views import upload_product, get_all_products, update_product, update_crop, get_all_crops, get_crops_by_user, delete_crop_user, farmer_dashboard, product_dashboard
from Utilities.views import news_feed
from Advisory.views import get_all_advices, home, dashboard, create, edit, web_login, web_register, is_email_available
from django.conf.urls import url
from django.views import static as stat
from Transaction.views import get_all_rent, rent, rent_release
from Advisory.views import get_all_advices

admin.site.site_header = "Kisaan Mitra Dashboard"

urlpatterns = [
    url(r'^static/(?P<path>.*)$', stat.serve, {'document_root': settings.STATIC_ROOT}),
    path('admin/', admin.site.urls),
    path('api/login', login, name="login"),
    path('api/register', register, name = 'register'),
    path('api/register/merchant', register_merchant, name = 'register_merchant'),
    path('api/upload/product', upload_product, name = 'upload_product'),
    path('api/news', news_feed, name = 'news_feed'),
    path('api/rent/create', rent, name = 'rent_create'),
    path('api/rent/release', rent_release, name = 'rent_release'),
    path('api/rent/list', get_all_rent, name = 'all_rent_list'),
    path('api/product/list', get_all_products, name = 'all_products'),
    path('api/product/update', update_product, name = 'update_product'),
    path('api/advices/all', get_all_advices, name = 'advices'),
    path('api/is_email_available', is_email_available, name = 'is_email_available'),
    path('advisory/dashboard', dashboard, name='advisory_dashboard'),
    path('advisory/create', create, name='advisory_dashboard_create'),
    path('advisory/edit/<int:id>', edit, name='advisory_dashboard_edit'),
    path('login', web_login, name="web_login"),
    path('signup', web_register, name="web_register"),
    path('api/crop/create', update_crop, name = 'create_crop'),
    path('api/crop/list', get_all_crops, name = 'all_crop'),
    path('api/crop/user', get_all_rent, name = 'crop_by_user'),
    path('api/crop/delete', delete_crop_user, name = 'delete_crop'),
    path('dashboard', farmer_dashboard, name='farmer_dashboard'),
    path('product', product_dashboard, name='product_dashboard'),
    path('', home, name = 'home'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)