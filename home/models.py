from django.db import models

# Create your models here.
class Login(models.Model):
    firstname = models.CharField(max_length=150)
    lastname = models.CharField(max_length=150)
    username = models.CharField(max_length=150)
    email = models.EmailField(blank=True)
    password_hash = models.CharField(max_length=255)
    role = models.CharField(max_length=150, null=True, default="student")

    def __str__(self):
        return self.username