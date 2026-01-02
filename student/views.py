from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from django.contrib import messages
from .models import Login, StudentNFCCard

def manage_card(request):
    return render(request, 'manage_card.html')

@login_required
def block_card(request):
    try:
        card = StudentNFCCard.objects.get(student=request.user)
    except StudentNFCCard.DoesNotExist:
        card = None

    if request.method == "POST":
        card_id = request.POST.get("card_id")
        reason = request.POST.get("reason")
        remarks = request.POST.get("remarks")

        if not card or card.card_id != card_id:
            messages.error(request, "Invalid NFC Card ID.")
            return redirect("block_card")

        if card.status == "BLOCKED":
            messages.warning(request, "Your card is already blocked.")
            return redirect("block_card")

        card.status = "BLOCKED"
        card.block_reason = reason
        card.remarks = remarks
        card.blocked_at = timezone.now()
        card.save()

        messages.success(request, "Your NFC card has been blocked successfully.")
        return redirect("/home")

    return render(request, "block_card.html", {
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

