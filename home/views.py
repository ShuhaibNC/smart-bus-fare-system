from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password
import re
from student.models import Login

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

        # Email validation — must have @ and a domain with a dot
        email_pattern = r'^[^@\s]+@[^@\s]+\.[^@\s]+$'
        if not re.match(email_pattern, email):
            return render(request, "signup.html", {"error": "Enter a valid email address."})

        # Check for duplicate email
        if Login.objects.filter(email=email).exists():
            return render(request, "signup.html", {"error": "Email already registered."})

        if password != confirm_password:
            return render(request, "signup.html", {"error": "Passwords do not match."})

        if Login.objects.filter(username=username).exists():
            return render(request, "signup.html", {"error": "Username already taken."})

        Login.objects.create(
            firstname=firstname,
            lastname=lastname,
            username=username,
            email=email,
            password_hash=make_password(password),
            role="student"
        )

        return render(request, "signup.html", {"info": "Account created successfully."})

    return render(request, "signup.html")


