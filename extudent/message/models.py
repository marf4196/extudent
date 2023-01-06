from django.db import models
from accounts.models import User

# Create your models here.
class Message(models.Model):
    writer = models.ForeignKey(User,null=True, blank=True, on_delete=models.CASCADE,related_name="writer")
    reciver = models.ForeignKey(User,null=True,blank=True, on_delete=models.CASCADE, related_name="reciver")
    title = models.CharField(max_length=255)
    text = models.TextField()
    attached_pic = models.ImageField(blank=True,null=True)
    is_recived = models.BooleanField(default=False)
