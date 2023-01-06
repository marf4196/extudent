from django.db import models
from accounts.models import User

# Create your models here.
class Message(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    text = models.TextField()
    attached_pic = models.ImageField(null=True)
    is_recived = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title
    