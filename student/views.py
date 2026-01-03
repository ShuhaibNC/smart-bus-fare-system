from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from django.contrib import messages
from .models import Login, StudentNFCCard, BusRoute, StudentWallet

def manage_card(request):
    return render(request, 'manage_card.html')


def block_card(request):
    try:
        card = StudentNFCCard.objects.get(student=request.session.get('user_id'))
    except StudentNFCCard.DoesNotExist:
        card = None

    if request.method == "POST":
        card_id = request.POST.get("card_id")
        reason = request.POST.get("reason")
        remarks = request.POST.get("remarks")
        print(request.POST.get("card_id"))
        print(request.POST.get("reason"))
        print(request.POST.get("remarks"))

        if not card or card.card_id != card_id:
            print(request, "Invalid NFC Card ID.")
            return redirect("home")

        if card.status == "BLOCKED":
            print   (request, "Your card is already blocked.")
            return redirect("home")

        card.status = "BLOCKED"
        card.block_reason = reason
        card.remarks = remarks
        card.blocked_at = timezone.now()
        card.save()

        messages.success(request, "Your NFC card has been blocked successfully.")
        return redirect("/home")

    return render(request, "manage_card.html", {
        "card": card
    })

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

def set_route(request):
    info = None
    login_id = request.session.get("user_id")
    flag = "green"

    if login_id:
        login_user = Login.objects.get(id=login_id)

        # Check if a route exists for this user
        if BusRoute.objects.filter(user=login_user).exists():
            info = "You already have routes saved for your account."
            flag = "red"

    return render(request, "set_route.html", {"info": info, "flag": flag})

def add_route(request):
    if request.method == "POST":
        stops = request.POST.getlist("stops[]")

        # Keep only the first four and pad if fewer
        stops = (stops + ["", "", "", ""])[:4]

        # Example login handling. Adjust if your session key is different
        login_id = request.session.get("user_id")

        if login_id is None:
            return redirect("/")   # or wherever your login page is

        login_user = Login.objects.get(id=login_id)
        
        BusRoute.objects.create(
            user=login_user,
            stop1=stops[0],
            stop2=stops[1],
            stop3=stops[2],
            stop4=stops[3],
        )

        return redirect("add_route")

    return render(request, "set_route.html", {'info':'Routes added successfully'})

def view_balance(request):
    # wallet = StudentWallet.objects.filter(student=request.user).first()
    return render(request, "wallet.html", {
        "card": "wallet"
    })
