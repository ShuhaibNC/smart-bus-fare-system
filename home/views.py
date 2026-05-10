from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password
import re
from student.models import Login
from email_validator import validate_email, EmailNotValidError

def index(request):
    return render(request, 'index.html')

def base(request):
    return render(request, 'base.html')


def signup(request):
    if request.method == "POST":
        firstname = request.POST.get("firstname", "").strip()
        lastname = request.POST.get("lastname", "").strip()
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")

        # Validate email format + check domain MX records
        try:
            valid = validate_email(email, check_deliverability=True)
            email = valid.email
        except EmailNotValidError as e:
            return render(request, "signup.html", {
                "error": str(e)
            })

        # Duplicate email check
        if Login.objects.filter(email=email).exists():
            return render(request, "signup.html", {
                "error": "Email already registered."
            })

        # Password match check
        if password != confirm_password:
            return render(request, "signup.html", {
                "error": "Passwords do not match."
            })

        # Username exists check
        if Login.objects.filter(username=username).exists():
            return render(request, "signup.html", {
                "error": "Username already taken."
            })

        # Create account
        Login.objects.create(
            firstname=firstname,
            lastname=lastname,
            username=username,
            email=email,
            password_hash=make_password(password),
            role="student"
        )

        return render(request, "signup.html", {
            "info": "Account created successfully."
        })

    return render(request, "signup.html")

