from django.db import models
from accounts.models import User

# Create your models here.

class Orders(models.Model):
    US_DOLLAR = 'USD'
    EURO = 'EUR'
    POUND  = 'GBP'
    CURRENCY_CHOICES = [
        (US_DOLLAR,'US DOLLAR'),
        (EURO,'EURO'),
        (POUND,'POUND'),
    ]
    amount = models.PositiveBigIntegerField(default=0)
    price = models.PositiveBigIntegerField(default=0)
    description = models.TextField()
    currency = models.CharField(choices=CURRENCY_CHOICES,max_length=20)
    owner = models.ForeignKey(User,on_delete=models.CASCADE,related_name="order_creator")
    buyer =models.ForeignKey(User,on_delete=models.CASCADE,related_name="order_buyer")
    status = models.BooleanField(default=False)
    