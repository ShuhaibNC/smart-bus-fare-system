from django.shortcuts import render, redirect, get_object_or_404
from student.models import Login, StudentNFCCard, InfoSubmit
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.utils import timezone
from hardware.nfc_writer import NFCWriter
from django.http import JsonResponse

def admin_login(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        try:
            user = Login.objects.get(username=username)
        except Login.DoesNotExist as e:
            return render(request, "admin_login.html", {"info": f"Login failed, couldn't find user, {e}"})

        if not check_password(password, user.password_hash):
            return render(request, "admin_login.html", {"info": "Login failed, Invalid username or password."})
        
        elif user.role != "admin":
            return render(request, "admin_login.html", {"info": "Your account appears to be a student account, please use student login."})

        # Store session data
        request.session["user_id"] = user.id
        request.session["username"] = user.username
        request.session["role"] = user.role
        return redirect("home")
    return render(request, 'admin_login.html')

def manage_nfc(request):
    pending_cards = InfoSubmit.objects.filter(
        card_id__isnull=False,
        card_activated=False
    )

    active_cards = StudentNFCCard.objects.all().order_by('-created_at')

    context = {
        'pending_cards': pending_cards,
        'active_cards': active_cards
    }

    return render(request, 'manage_nfc.html', context)

def accept_nfc_card(request, id):
    if request.method != 'POST':
        return redirect('manage_nfc')
    info = get_object_or_404(InfoSubmit, id=id)

    if info.card_activated:
        messages.warning(request, "This card is already activated.")
        return redirect('manage_nfc')

    if not info.card_id:
        messages.error(request, "No card ID found for this student.")
        return redirect('manage_nfc')


    if StudentNFCCard.objects.filter(card_id=info.card_id).exists():
        messages.error(request, "This NFC card already exists in system.")
        return redirect('manage_nfc')

    StudentNFCCard.objects.create(
        username=info.user,
        card_id=info.card_id,
        status='ACTIVE',
        balance=0
)
    # Activate in InfoSubmit
    info.activate_card()
    messages.success(request, "NFC card accepted and activated successfully.")
    return redirect('manage_nfc')

def update_nfc_card(request, id):
    if request.method != 'POST':
        return redirect('manage_nfc')

    card = get_object_or_404(StudentNFCCard, id=id)

    status = request.POST.get('status')
    block_reason = request.POST.get('block_reason')
    remarks = request.POST.get('remarks')

    if status not in ['ACTIVE', 'BLOCKED']:
        messages.error(request, "Invalid status value.")
        return redirect('manage_nfc')

    card.status = status

    if status == 'BLOCKED':
        card.block_reason = block_reason if block_reason else None
        card.remarks = remarks
        card.blocked_at = timezone.now()
    else:
        # Reset block-related fields
        card.block_reason = None
        card.remarks = None
        card.blocked_at = None

    card.save()

    messages.success(request, "NFC card updated successfully.")
    return redirect('manage_nfc')

def write_nfc(request, card_id):
    flag = 'green'
    card = get_object_or_404(InfoSubmit, card_id=card_id)

    context = {
        'card_id': card.card_id,
        'flag': flag,
        'names': {
            'first_name': card.first_name,
            'last_name': card.last_name,
        }
    }
    
    return render(request, "write_nfc.html", context)

def nfcwriter(request, card_id):
    #hardware
    card = get_object_or_404(InfoSubmit, card_id=card_id)
    fullname = card.first_name + card.last_name
    writer = NFCWriter(card_id=card_id, fullname=fullname)
    writer.run()
    return render(
        request,
        "write_nfc.html",
        {
            "card_id": card_id,
            "write_status": "reading",
            'names': {
            'first_name': card.first_name,
            'last_name': card.last_name,
        }
        }
    )