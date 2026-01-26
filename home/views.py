from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password
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

        # Basic validation
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, "signup.html", {"info" : "Passwords do not match."})

        # Optional uniqueness check
        if Login.objects.filter(username=username).exists():
            return render(request, "signup.html", {"info" : "Username already taken."})

        # Create the user
        Login.objects.create(
            firstname=firstname,
            lastname=lastname,
            username=username,
            email=email,
            password_hash=make_password(password),  # secure hashing
            role="student"
        )

        messages.success(request, "Account created successfully.")
        return render(request, "signup.html", {"info" : "Account created successfully."}) # change to your login view name

    return render(request, "signup.html")

