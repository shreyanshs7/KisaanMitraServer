from django.contrib import admin
from .models import Cart, CartDetail, Rent

class CartAdmin(admin.ModelAdmin):
    list_display=('id','user','status')
    search_fields=('id','user','status')
    list_filters=('user',)
    ordering=('-created_at',)
    readonly_fields=('created_at', 'updated_at')

class CartDetailAdmin(admin.ModelAdmin):
    list_display=('id','cart','product','quantity')
    search_fields=('id','product','quantity')
    list_filters=('user',)
    ordering=('-created_at',)
    readonly_fields=('created_at', 'updated_at')

class RentAdmin(admin.ModelAdmin):
    list_display=('id','product','user','price','quantity')
    search_fields=('id','user','product')
    list_filters=('user',)
    ordering=('-created_at',)
    readonly_fields=('created_at', 'updated_at')
# Register your models here.
admin.site.register(Cart,CartAdmin)
admin.site.register(CartDetail,CartDetailAdmin)
admin.site.register(Rent,RentAdmin)