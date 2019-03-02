from django.contrib import admin
from .models import Advice, AdviceCategory

# Register your models here.
admin.site.register(Advice)
admin.site.register(AdviceCategory)