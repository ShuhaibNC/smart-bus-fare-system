from django.db import models

# Create your models here.
class BusFee(models.Model):
    dest_stop = models.CharField(max_length=255, null=True)
    dest_route = models.CharField(max_length=255, null=True)
    busfee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        )