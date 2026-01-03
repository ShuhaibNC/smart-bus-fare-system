from django.db import models
from django.contrib.auth.models import User

class Login(models.Model):
    firstname = models.CharField(max_length=150)
    lastname = models.CharField(max_length=150)
    username = models.CharField(max_length=150)
    email = models.EmailField(blank=True)
    password_hash = models.CharField(max_length=255)
    role = models.CharField(max_length=150, null=True, default="student")
    test=models.CharField(max_length=150,default="test")

    def __str__(self):
        return self.username

class StudentNFCCard(models.Model):
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('BLOCKED', 'Blocked'),
    ]

    REASON_CHOICES = [
        ('lost', 'Lost'),
        ('stolen', 'Stolen'),
        ('damaged', 'Damaged'),
    ]

    student = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='nfc_card'
    )

    card_id = models.CharField(
        max_length=50,
        unique=True
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='ACTIVE'
    )

    block_reason = models.CharField(
        max_length=20,
        choices=REASON_CHOICES,
        blank=True,
        null=True
    )

    remarks = models.TextField(
        blank=True,
        null=True
    )

    blocked_at = models.DateTimeField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.card_id} ({self.status})"
    
class BusRoute(models.Model):
    user = models.CharField(max_length=255, null=True)
    stop1 = models.CharField(max_length=255, null=True)
    stop2 = models.CharField(max_length=255, blank=True, null=True)
    stop3 = models.CharField(max_length=255, blank=True, null=True)
    stop4 = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    # test = models.CharField(max_length=255, blank=True, null=True)



    def __str__(self):
        return f"Route {self.id}"
    
class StudentWallet(models.Model):
    STATUS_CHOICES = [
        ('HEALTHY', 'Healthy'),
        ('LOW', 'Low Balance'),
    ]

    student = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="wallet"
    )

    card_id = models.CharField(
        max_length=20,
        unique=True
    )

    balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='LOW'
    )

    updated_at = models.DateTimeField(auto_now=True)

    def update_status(self):
        if self.balance < 100:
            self.status = 'LOW'
        else:
            self.status = 'HEALTHY'
        self.save()

    def __str__(self):
        return f"{self.student.username} - ₹{self.balance}"
