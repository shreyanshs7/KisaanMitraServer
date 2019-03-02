from django.contrib import admin
from .models import UserDetail, Merchant, FcmModel

class UserDetailAdmin(admin.ModelAdmin):
    list_display=('id','user','contact','email')
    search_fields=('id','user','contact')
    list_filters=('user',)
    ordering=('-created_at',)
    readonly_fields=('created_at', 'updated_at')

class MerchantAdmin(admin.ModelAdmin):
    list_display=('id','user','contact','email','address')
    search_fields=('id','name','email')
    list_filters=('user',)
    ordering=('-created_at',)
    readonly_fields=('created_at', 'updated_at')

class FcmModelAdmin(admin.ModelAdmin):
    list_display=('id','user','contact')
    search_fields=('id','user')
    list_filters=('user',)
    ordering=('-created_at',)
    readonly_fields=('created_at', 'updated_at')


# Register your models here.
admin.site.register(UserDetail,UserDetailAdmin)
admin.site.register(Merchant,MerchantAdmin)
admin.site.register(FcmModel,FcmModelAdmin)