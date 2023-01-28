from django.db import models
from accounts.models import User

# Create your models here.
class Message(models.Model):
    writer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="message_writer",
        blank=True,null=True
    )
    reciver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="message_reciver",blank=True,null=True
    )
    title = models.CharField(max_length=255)
    text = models.TextField()
    attached_pic = models.ImageField(null=True,blank=True)
    is_recived = models.BooleanField(default=False)

    def __str__(self):
        return self.title
