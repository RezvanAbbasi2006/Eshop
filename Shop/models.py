from django.contrib.auth.models import User
from django.db import models


class Product(models.Model):
    title = models.CharField(max_length=100, null=True)
    price = models.IntegerField(default=1)
    color = models.CharField(max_length=100, null=True)
    expire_date = models.CharField(max_length=50, null=True)
    company_name = models.CharField(max_length=100, null=True)
    count = models.IntegerField(null=True, default=1)

    def save(self, *args, **kwargs):
        super(Product, self).save(*args, **kwargs)


class Profile(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user',
        null=True
    )
    img = models.ImageField(null=True)
    profile_type = models.CharField(max_length=100, default="customer")
    mobile = models.CharField(max_length=11)
    username = models.CharField(max_length=8, null=True)
    password = models.CharField(max_length=8)
    address = models.CharField(max_length=100, null=True)

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)


class Message(models.Model):
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='message',
        null=True
    )
    text = models.TextField()
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super(Message, self).save(*args, **kwargs)


class Cart(models.Model):
    title = models.CharField(max_length=100, null=True, default='سبد خرید')
    create_date = models.DateTimeField(verbose_name='', name='date', auto_now=True)
    update_date = models.DateTimeField(verbose_name='update date', name='update date', auto_now=True)
    content_text = models.CharField(max_length=100, null=True, default=None)
