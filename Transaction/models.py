from django.db import models
from Authentication.models import UserDetail
from Inventory.models import Product

# Create your models here.
class Cart(models.Model):
	class Meta:
		verbose_name="Cart"
		verbose_name_plural="Carts"
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

class CartDetail(models.Model):
	class Meta:
		verbose_name="CartDetail"
		verbose_name_plural="CartDetails"
	cart = models.ForeignKey(Cart, on_delete = models.CASCADE)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	quantity = models.IntegerField()
	created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)


class Rent(models.Model):
	class Meta:
		verbose_name="Rent"
		verbose_name_plural="Rents"
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	user = models.ForeignKey(UserDetail, on_delete=models.CASCADE)
	price = models.FloatField()
	quantity = models.FloatField()
	rent_completed = models.BooleanField(default=False)
	duration_start = models.DateTimeField()
	duration_end = models.DateTimeField()
	created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

	def __str__(self):
	 return self.product.name