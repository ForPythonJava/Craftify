from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Login(AbstractUser):
    userType = models.CharField(max_length=100)
    viewPass = models.CharField(max_length=100, null=True)
    regDate=models.DateField(null=True)

    def __str__(self):
        return self.username


class Artist(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.IntegerField()
    skills = models.CharField(max_length=200)
    image1 = models.ImageField(upload_to="image")
    image2 = models.ImageField(upload_to="image")
    image3 = models.ImageField(upload_to="image")
    address = models.CharField(max_length=300)
    status = models.CharField(max_length=100, default="Not Paid")
    loginid = models.ForeignKey(Login, on_delete=models.CASCADE, default=1)
    
    def __str__(self):
        return self.name

