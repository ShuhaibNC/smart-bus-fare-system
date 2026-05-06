from django.db import models
import uuid
# Create your models here.
class BusFee(models.Model):
    dest_stop = models.CharField(max_length=255, null=True)
    dest_route = models.CharField(max_length=255, null=True)
    busfee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        )
class BusLog(models.Model):
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
        
class Transaction(models.Model):

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("completed", "Completed"),
        ("failed", "Failed"),
        ("refunded", "Refunded"),
    ]


    # Public Transaction ID (safe to expose)
    transaction_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    username = models.CharField(max_length=150, blank=True,
        null=True)
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    # Optional description
    description = models.TextField(
        blank=True,
        null=True
    )

    # Refund eligibility flag
    is_refundable = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.transaction_id} | {self.user} | {self.status}"