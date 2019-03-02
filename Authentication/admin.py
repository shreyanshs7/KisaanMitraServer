from django.contrib import admin
from .models import UserDetail, Merchant, FcmModel

# Register your models here.
admin.site.register(UserDetail)
admin.site.register(Merchant)
admin.site.register(FcmModel)