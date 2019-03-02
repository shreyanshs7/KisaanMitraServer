from django.contrib import admin
from .models import Product, Crop, FarmerCrop

class ProductAdmin(admin.ModelAdmin):
    list_display=('id','merchant','name','product_type','quantity')
    search_fields=('id','name','product_type','quantity')
    list_filters=('user',)
    ordering=('-created_at',)
    readonly_fields=('created_at', 'updated_at')

class FarmerCropAdmin(admin.ModelAdmin):
    list_display=('id','user','crop')
    search_fields=('id','user','crop')
    list_filters=('user',)
    ordering=('-created_at',)
    readonly_fields=('created_at', 'updated_at')

class CropAdmin(admin.ModelAdmin):
    list_display=('id','crop_type','name','season')
    search_fields=('id','crop_type','name')
    list_filters=('user',)
    ordering=('-created_at',)
    readonly_fields=('created_at', 'updated_at')
# Register your models here.
admin.site.register(Product,ProductAdmin)
admin.site.register(Crop,CropAdmin)
admin.site.register(FarmerCrop,FarmerCropAdmin)