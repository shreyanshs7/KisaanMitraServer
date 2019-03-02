from django.contrib import admin
from .models import Advice, AdviceCategory

class AdviceAdmin(admin.ModelAdmin):
    list_display=('id','user','title')
    search_fields=('id','user','title')
    list_filters=('user',)
    ordering=('-created_at',)
    readonly_fields=('created_at', 'updated_at')

class AdviceCategoryAdmin(admin.ModelAdmin):
    list_display=('id','advice','crop')
    search_fields=('id','crop','advice')
    list_filters=('user',)
    ordering=('-created_at',)
    readonly_fields=('created_at', 'updated_at')
# Register your models here.
admin.site.register(Advice,AdviceAdmin)
admin.site.register(AdviceCategory,AdviceCategoryAdmin)