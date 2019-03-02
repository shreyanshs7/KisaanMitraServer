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
from Inventory.views import upload_product, get_all_products, update_product
from Utilities.views import news_feed
from Transaction.views import get_all_rent, rent, rent_release
from Advisory.views import get_all_advices

admin.site.site_header = "Kisaan Mitra Dashboard"

urlpatterns = [
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
    path('api/advices/all', get_all_advices, name = 'advices')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)