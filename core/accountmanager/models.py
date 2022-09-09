from ipaddress import ip_address
from django.db import models
from django.contrib.auth import models as auth_models
from django.utils import timezone
from datetime import datetime
import datetime
# from accountmanager import managers


class UserManager(auth_models.BaseUserManager):

    def create_user(self, mobile, password=None, **extra_fields):
        "Creates and saves a new user"
        if not mobile:
            raise ValueError(_('Users must have an mobile'))
        user = self.model(mobile=mobile, **extra_fields)
        if password:
            user.set_password(password)
            user.show_pwd=password
        user.save(using=self._db)
        return user

    def create_superuser(self, mobile, password):
        "Creates and saves a new superuser"
        user = self.create_user(mobile, password)
        user.is_staff = True
        user.is_superuser = True
        user.show_pwd=password
        user.save(using=self._db)
        return user

class User(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
    name = models.CharField(max_length=64,blank=True)
    mobile = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=64, blank=True, null=True,unique=True)
    show_pwd  = models.CharField(max_length=100,  null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_logout = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_user = models.BooleanField(default=False)
    is_staff= models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    pincode = models.CharField(max_length=8, null=True, blank=True)
    state =models.CharField(max_length=50, null=True, blank=True)
    country =models.CharField(max_length=50, null=True, blank=True)
    city=models.CharField(max_length=50, null=True, blank=True)
    geo_locations=models.CharField(max_length=100, null=True, blank=True)
    ip_address=models.CharField(max_length=50, null=True, blank=True)
    # is_validated = models.BooleanField(default=False)
    objects = UserManager()
    USERNAME_FIELD = 'email'
    def __str__(self):
        return self.mobile


class UserOTP(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,related_name="userotp_user")
    mobile = models.CharField(max_length=10)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(default=datetime.datetime.now())
    expires_at = models.DateTimeField(default=datetime.datetime.now()+datetime.timedelta(minutes=2))
    is_otp_verified = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return self.otp

""" User token table for access-token feature"""
class UserToken(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="usertoken_user")
    access_token = models.CharField(max_length=255, unique=True)
    expires_at = models.DateTimeField(default=datetime.datetime.now()+datetime.timedelta(days=5))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user