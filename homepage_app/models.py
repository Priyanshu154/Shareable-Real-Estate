from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Person(models.Model):
    user= models.OneToOneField(User, on_delete= models.CASCADE)
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    pan = models.CharField(max_length = 15)
    account_holder_id = models.TextField(null=True)
    account_id = models.TextField(null=True)
    dob = models.DateField(null=True)
    gender = models.CharField(max_length = 15,null=True)
    mobile_no = models.CharField(max_length = 10, null=True)