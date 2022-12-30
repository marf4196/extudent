from django.db import models

class User(models.Model):
    f_name = models.models.CharField(max_length=50)
    l_name = models.models.CharField(max_length=50)
    email = models.EmailField(blank=False)
    # code melli
    melli_code = models.BigIntegerField(max_length=10)
    # tasvir cart melli
    id_card_img = models.ImageField()
    # field video
    video = models.FileField()