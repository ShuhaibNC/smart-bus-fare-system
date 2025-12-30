from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html')

def base(request):
    return render(request, 'base.html')

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from .models import Login

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
            messages.error(request, "Username already taken.")
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

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from .models import Login

def student_login(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        # Find the user
        try:
            user = Login.objects.get(username=username)
        except Login.DoesNotExist:
            messages.error(request, "Invalid username or password.")
            return render(request, "student_login.html", {"info": "Login failed"})

        # Verify password
        if not check_password(password, user.password_hash):
            messages.error(request, "Invalid username or password.")
            return render(request, "student_login.html", {"info": "Login failed"})

        # Store session data
        request.session["user_id"] = user.id
        request.session["username"] = user.username
        request.session["role"] = user.role

        messages.success(request, "Login successful.")
        return redirect("home")   # change to whatever page you want after login

    return render(request, "student_login.html")
