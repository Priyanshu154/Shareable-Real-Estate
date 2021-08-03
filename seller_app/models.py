from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Property(models.Model):
    actual_price = models.FloatField(null=True, blank=True, default=None)
    area = models.FloatField(null=True, blank=True, default=None)
    address = models.TextField(null=True, blank=True, default=None)
    city = models.CharField(null=True, blank=True, default=None,max_length=1000)
    resale = models.BooleanField(null=True, blank=True, default=None)
    bhk = models.IntegerField(null=True, blank=True, default=None)
    rera_approved = models.BooleanField(null=True, blank=True, default=None)
    prop_image = models.ImageField(upload_to='prop_images', default=None)
    no_of_shares = models.IntegerField(null=True, blank=True, default=None)
    price_per_share = models.FloatField(null=True, blank=True, default=None)


class Seller(models.Model):
    seller_details = models.ForeignKey(User, on_delete=models.CASCADE, null=False, default=None)
    proposed_price = models.FloatField(null=True, blank=True, default=None)
    property_details = models.ForeignKey(Property, on_delete=models.CASCADE, null=False, default=None)
