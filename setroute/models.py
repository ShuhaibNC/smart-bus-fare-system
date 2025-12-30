from django.db import models
from home.models import Login

# Create your models here.
class BusRoute(models.Model):
    user = models.ForeignKey(Login, on_delete=models.CASCADE)
    stop1 = models.CharField(max_length=255, null=True)
    stop2 = models.CharField(max_length=255, blank=True, null=True)
    stop3 = models.CharField(max_length=255, blank=True, null=True)
    stop4 = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Route {self.id}"