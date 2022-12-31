from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(_("email address"), unique=True)
    is_staff = models.BooleanField(default=False)
    
    is_active = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def fullname(self):
        return f"{self.first_name} {self.last_name}"


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    f_name = models.CharField(max_length=55,null=True, blank=True)
    l_name = models.CharField(max_length=55,null=True, blank=True)
    phone_number = models.PositiveBigIntegerField(null=True)
    code_melli = models.PositiveBigIntegerField(null=True)
    img = models.ImageField(null=True)
    # upload to required 
    ############################
    video = models.FileField(null=True)
    ############################
    ballance = models.PositiveBigIntegerField(default=0)
    is_complete = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

class UserIdentDocs(models.Model):
    owner = models.ForeignKey(User,on_delete=models.CASCADE, related_name = "user_ident_Docs")
    code_melli = models.PositiveBigIntegerField(null=True)
    img = models.ImageField(null=True)
    # upload to required 
    ############################
    video = models.FileField(null=True)
    ############################
    ballance = models.PositiveBigIntegerField(default=0)
    is_complete = models.BooleanField(default=False)
    