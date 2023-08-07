from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Login(AbstractUser):
    userType = models.CharField(max_length=100)
    viewPass = models.CharField(max_length=100, null=True)
    regDate = models.DateField(null=True)
    
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


class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.IntegerField()
    address = models.CharField(max_length=300)
    loginid = models.ForeignKey(Login, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Products(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    price = models.IntegerField()
    color = models.CharField(max_length=100)
    qty = models.IntegerField()
    image = models.ImageField(upload_to="image")
    image1 = models.ImageField(upload_to="image",null=True)
    image2 = models.ImageField(upload_to="image",null=True)
    desc = models.CharField(max_length=300)
    status = models.CharField(max_length=100, default="Pending")
    artistId = models.ForeignKey(Artist, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class Cart(models.Model):
    uid = models.ForeignKey(User, on_delete=models.CASCADE)
    pid = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.IntegerField()
    status = models.CharField(max_length=100, default="InCart")
    date = models.DateField(auto_now=True, null=True)
    name=models.CharField(max_length=100,null=True)
    email=models.EmailField(max_length=100,null=True)
    state=models.CharField(max_length=100,null=True)
    pincode=models.IntegerField(null=True)
    address=models.CharField(max_length=300,null=True)


class Wishlist(models.Model):
    uid = models.ForeignKey(User, on_delete=models.CASCADE)
    pid = models.ForeignKey(Products, on_delete=models.CASCADE)


class Feedback(models.Model):
    uid = models.ForeignKey(User, on_delete=models.CASCADE)
    oid = models.ForeignKey(Cart, on_delete=models.CASCADE)
    rating = models.IntegerField()
    review = models.CharField(max_length=300)
    date = models.DateField(auto_now=True)


class Chat(models.Model):
    uid = models.ForeignKey(User, on_delete=models.CASCADE)
    artistid = models.ForeignKey(Artist, on_delete=models.CASCADE)
    message = models.CharField(max_length=300)
    date = models.DateField(auto_now=True)
    time = models.CharField(max_length=100)
    utype = models.CharField(max_length=100)
