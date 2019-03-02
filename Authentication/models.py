from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class UserDetail(models.Model):
	ADMIN = "ADMIN"
	RETAILER = "RETAILER"
	FARMER = "FARMER"
	OTHER = "OTHER"
	USER_CHOICES = (
		(ADMIN, "ADMIN"),
		(RETAILER, "RETAILER"),
		(FARMER, "FARMER"),
		(OTHER, "OTHER")
	)
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	first_name = models.CharField(max_length = 120)
	last_name = models.CharField(max_length = 120)
	user_type = models.CharField(max_length = 120, choices = USER_CHOICES)
	contact = models.CharField(max_length = 10)
	email = models.EmailField(max_length=254, default = "abcd@gmail.com")
	latitude = models.CharField(max_length = 6)
	longitude = models.CharField(max_length = 6)
	created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

	@property
	def full_name(self):
		return ("%s %s")%(self.first_name, self.last_name)

	def __str__(self):
	 return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserDetail.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userdetail.save()

class Merchant(models.Model):
	user = models.ForeignKey(UserDetail, on_delete=models.CASCADE)
	name = models.CharField(max_length = 120)
	email = models.EmailField(max_length = 254)
	address = models.CharField(max_length = 500)
	contact = models.CharField(max_length = 10)
	created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

	def __str__(self):
	 return self.name

class FcmModel(models.Model):
	user = models.ForeignKey(UserDetail, on_delete = models.CASCADE)
	token = models.CharField(max_length = 500)
	contact = models.CharField(max_length = 10)
	created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

	def __str__(self):
		return self.contact