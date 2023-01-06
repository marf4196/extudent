from django.db import models
from accounts.models import User


# Create your models here
class Orders(models.Model):
    US_DOLLAR = 'USD'
    EURO = 'EUR'
    POUND = 'GBP'
    CURRENCY_CHOICES = [
        (US_DOLLAR, 'US DOLLAR'),
        (EURO, 'EURO'),
        (POUND, 'POUND'),
    ]
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="order_creator")
    amount = models.PositiveBigIntegerField(default=0)
    price = models.PositiveBigIntegerField(default=0)
    description = models.TextField()
    currency = models.CharField(choices=CURRENCY_CHOICES, max_length=20)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="order_buyer")
    status = models.BooleanField(default=False)
    
    def __str__(self):
        return self.description[:30]
    
    
    @property
    def get_status(self):
        return self.status
