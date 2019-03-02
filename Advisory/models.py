from django.db import models
from Inventory.models import Crop
from Authentication.models import UserDetail
from froala_editor.fields import FroalaField

# Create your models here.

class Advice(models.Model):
    user = models.ForeignKey(UserDetail, on_delete=models.CASCADE)
    title = models.CharField(null=False, blank=False, max_length=64)
    description = FroalaField()
    active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='static/uploads/advice_covers/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    def __str__(self):
        return self.title

class AdviceCategory(models.Model):
    advice = models.ForeignKey(Advice, on_delete=models.CASCADE)
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    def __str__(self):
        return str(self.advice)