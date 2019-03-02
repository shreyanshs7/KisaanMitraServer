from django.db import models
from Authentication.models import Merchant, UserDetail

# Create your models here.

# def product_image_path(instance, filename):
# 	return ("/static/upload/product_%s/%s")%(str(instance.id),str(filename))

class Product(models.Model):
	PCS = "PCS"
	KG = "KG"
	LTR = "LTR"
	OTHER = "OTHER"
	QUANTITY_TYPE = (
		(PCS, "PCS"),
		(KG, "KG"),
		(LTR, "LTR"),
		(OTHER, "OTHER")
	)

	SEED = "SEED"
	MANURE = "MANURE"
	VEHICLE = "VEHICLE"
	EQUIPMENT = "EQUIPMENT"
	OTHER = "OTHER"
	PRODUCT_TYPE = (
		(SEED, "SEED"),
		(MANURE, "MANURE"),
		(VEHICLE, "VEHICLE"),
		(EQUIPMENT, "EQUIPMENT"),
		(OTHER, "OTHER")
	)
	LESS_THAN_ONE_YEAR = "LESS_THAN_ONE_YEAR"
	ONE_TO_FIVE_YEAR = "ONE_TO_FIVE_YEAR"
	GREATER_THAN_FIVE = "GREATER_THAN_FIVE" 
	PERIOD_CHOICES = (
		(LESS_THAN_ONE_YEAR, "LESS_THAN_ONE_YEAR"),
		(ONE_TO_FIVE_YEAR, "ONE_TO_FIVE_YEAR"),
		(GREATER_THAN_FIVE, "GREATER_THAN_FIVE")
	)
	BUY = "BUY"
	RENT = "RENT"
	SELL_TYPE = (
		(BUY, "BUY"),
		(RENT, "RENT")
	)
	merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)
	name = models.CharField(max_length = 120)
	product_type = models.CharField(max_length = 120, choices = PRODUCT_TYPE)
	sell_price = models.FloatField(default=100)
	rent_price = models.FloatField(default=100)
	sell_type = models.CharField(max_length = 12, choices = SELL_TYPE, default=BUY)
	quantity = models.FloatField()
	period = models.CharField(max_length = 120, choices = PERIOD_CHOICES, default = LESS_THAN_ONE_YEAR)
	quantity_type = models.CharField(max_length = 5, choices = QUANTITY_TYPE)
	image = models.ImageField(upload_to="static/uploads/products/")
	created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

	def __str__(self):
		return self.name

class Crop(models.Model):
	VEGETABLE = "VEGETABLE"
	FRUIT = "FRUIT"
	CEREAL = "CEREAL"
	CROP_CHOICES = (
		(VEGETABLE, "VEGETABLE"),
		(FRUIT, "FRUIT"),
		(CEREAL, "CEREAL")
	)

	RABI = "RABI"
	KHARIF = "KHARIF"

	SEASON_CHOICES = (
		(RABI, "RABI"),
		(KHARIF, "KHARIF")
	)
	crop_type = models.CharField(max_length = 120, choices = CROP_CHOICES)
	season = models.CharField(max_length = 120, choices = SEASON_CHOICES)
	name = models.CharField(max_length=32, null=False, blank=False, default="Kisaan Mitra")
	created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

	def __str__(self):
	 return str(self.crop_type)

class FarmerCrop(models.Model):
	user = models.ForeignKey(UserDetail, on_delete=models.CASCADE)
	crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

	def __str__(self):
	 return self.user.full_name
