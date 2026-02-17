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
class BusData(models.Model):
    card_id = models.CharField(max_length=50)
    student_name = models.CharField(max_length=100)
    tap_date = models.DateField()
    tap_time = models.TimeField()
    location = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.student_name} - {self.tap_date} {self.tap_time}"

    class Meta:
        db_table = "bus_log"
        ordering = ["-tap_date", "-tap_time"]