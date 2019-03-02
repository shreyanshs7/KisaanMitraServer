from django.db import models
from Authentication.models import UserDetail
from Inventory.models import Product

# Create your models here.
class Cart(models.Model):
	INCART = "INCART"
	PAID = "PAID"
	OTHER = "OTHER"
	STATUS = (
		(INCART, "INCART"),
		(PAID, "PAID"),
		(OTHER, "OTHER")
	)
	user = models.OneToOneField(UserDetail, on_delete=models.CASCADE)
	status = models.CharField(max_length = 10, choices = STATUS)
	sub_total = models.FloatField()
	created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

class CartDetail(models.CharField):
	cart = models.ForeignKey(Cart, on_delete = models.CASCADE)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	quantity = models.IntegerField()
	created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)