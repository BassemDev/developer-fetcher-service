from django.db import models


# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=200)
    bio = models.TextField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.name


class Advocate(models.Model):
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    username = models.CharField(max_length=500, null=True, blank=True, default="")
    name = models.CharField(max_length=500, null=True, blank=True)
    profile_picture = models.CharField(max_length=500, default="https://uxwing.com/wp-content/themes/uxwing/download/peoples-avatars/corporate-user-icon.png")
    bio = models.TextField(max_length=550, null=True, blank=True)
    twitter = models.URLField(null=True)

    def __str__(self):
        return self.username
