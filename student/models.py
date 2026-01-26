from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


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

    username = models.CharField(max_length=150, blank=True,
        null=True)

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
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    #test = models.CharField(max_length=255, blank=True, null=True)



    def __str__(self):
        return f"Route {self.id}"
    

class InfoSubmit(models.Model):
    BLOOD_GROUP_CHOICES = [
        ("A+", "A+"), ("A-", "A-"),
        ("B+", "B+"), ("B-", "B-"),
        ("AB+", "AB+"), ("AB-", "AB-"),
        ("O+", "O+"), ("O-", "O-"),
    ]

    user = models.CharField(max_length=255, null=True)

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    guardian_name = models.CharField(max_length=200)

    blood_group = models.CharField(
    max_length=3,
    choices=BLOOD_GROUP_CHOICES,
    null=True,
    blank=True
)


    address = models.TextField()
    pin_code = models.CharField(max_length=6)

    phone_no = models.CharField(max_length=10)
    sphone_no = models.CharField(max_length=10,null=True,
    blank=True)

    college_name = models.CharField(max_length=200)
    aadhaar_no = models.CharField(max_length=12, unique=True)

    card_id = models.CharField(max_length=20, blank=True, null=True, unique=True)
    card_activated = models.BooleanField(default=False)
    card_accepted_at = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.user}"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    def activate_card(self):
        if self.card_activated:
            return False

        self.card_activated = True
        self.card_accepted_at = timezone.now()
        self.save(update_fields=["card_activated", "card_accepted_at"])
        return True

