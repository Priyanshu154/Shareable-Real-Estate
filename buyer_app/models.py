from django.contrib.auth.models import User
from django.db import models
from seller_app.models import *


class Buyer(models.Model):
    buyer_details = models.ForeignKey(User, on_delete=models.CASCADE, null=False, default=None)
    buyer_property = models.ForeignKey(Property, on_delete=models.CASCADE, null=False, default=None)
    buyer_shares = models.IntegerField(null=True, blank=True, default=None)
    buyer_bond = models.FileField(upload_to='buyer_bond_file', default=None, null=True,blank=True)
    buyer_order_id = models.CharField(max_length = 30,null=False,blank=False)
