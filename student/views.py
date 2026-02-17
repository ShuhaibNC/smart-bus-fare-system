from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate
from django.utils import timezone
from decimal import Decimal
from django.contrib import messages
from .models import Login, StudentNFCCard, BusRoute, InfoSubmit
from system_admin.models import BusFee
import json
import uuid

def manage_card(request):
    return render(request, 'manage_card.html')

def addinfo(request):
    return render(request, 'addinfo.html')

def block_card(request):
    try:
        card = StudentNFCCard.objects.get(username=request.session["username"])
    except StudentNFCCard.DoesNotExist:
        card = None
    if request.method == "POST":
        card_id = request.POST.get("card_id")
        reason = request.POST.get("reason")
        remarks = request.POST.get("remarks")
        
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
        return redirect("home")   # change to whatever page you want after login

    return render(request, "student_login.html")

def set_route(request):
    login_id = request.session.get("user_id")
    info = None
    flag = "green"

    if login_id:
        # Assuming Login is your user model or related to it
        if BusRoute.objects.filter(user=login_id).exists():
            info = "You just saved routes to your account."
            flag = "red"

    # Fetch data from BusFee model
    bus_fees = BusFee.objects.all()
    
    # Structure data: { "Route Name": { "stops": [], "fares": [] } }
    route_data_dict = {}
    for fee in bus_fees:
        route = fee.dest_route
        if route not in route_data_dict:
            route_data_dict[route] = {"stops": [], "fares": []}
        
        route_data_dict[route]["stops"].append(fee.dest_stop)
        route_data_dict[route]["fares"].append(float(fee.busfee))

    context = {
        "info": info,
        "flag": flag,
        # Convert dictionary to JSON string for JavaScript
        "route_data_json": json.dumps(route_data_dict)
    }
    
    return render(request, "set_route.html", context)

def add_route(request):
    if request.method == "POST":
        login_id = request.session.get("user_id")
        if not login_id:
            return redirect('login') # Or handle error

        stop1 = request.POST.get('stop1')
        stop2 = request.POST.get('stop2')
        
        # Create the route
        BusRoute.objects.create(
            user=login_id,
            stop1=stop1,
            stop2=stop2
        )
        return redirect('set_route')
    return render(request, "set_route.html", {'info':'Routes added successfully'})

def view_balance(request):
    user = request.session.get("username")

    if not user:
        return render(request, "wallet.html", {
            "card": None,
            "student_info": None
        })

    # Get student info (for name display)
    student_info = InfoSubmit.objects.filter(user=user).first()

    # Get NFC card (source of truth for balance & status)
    card = StudentNFCCard.objects.filter(username=user).first()

    return render(request, "wallet.html", {
        "card": card,
        "student_info": student_info,
    })


def infosubmit(request):
    existing_info = InfoSubmit.objects.filter(user=request.user).first()

    if request.method == "POST":
        user = request.session["username"]

        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()
        guardian_name = request.POST.get("guardian_name", "").strip()
        blood_group = request.POST.get("blood_group", "").strip()
        address = request.POST.get("address", "").strip()
        pin_code = request.POST.get("pin_code", "").strip()
        phone_no = request.POST.get("phone_no", "").strip()
        sphone_no = request.POST.get("sphone_no", "").strip()
        college_name = request.POST.get("college_name", "").strip()
        aadhaar_no = request.POST.get("aadhaar_no", "").strip()

        if not all([
            first_name, last_name, guardian_name, blood_group,
            address, pin_code, phone_no, sphone_no,
            college_name, aadhaar_no
        ]):
            messages.error(request, "All fields are required.")
            return render(request, "addinfo.html", {"form_data": request.POST})

        if not pin_code.isdigit() or len(pin_code) != 6:
            messages.error(request, "Pin code must be 6 digits.")
            return render(request, "addinfo.html", {"form_data": request.POST})

        if not phone_no.isdigit() or len(phone_no) != 10:
            messages.error(request, "Primary phone number must be 10 digits.")
            return render(request, "addinfo.html", {"form_data": request.POST})

        if not sphone_no.isdigit() or len(sphone_no) != 10:
            messages.error(request, "Second phone number must be 10 digits.")
            return render(request, "addinfo.html", {"form_data": request.POST})

        if not aadhaar_no.isdigit() or len(aadhaar_no) != 12:
            messages.error(request, "Aadhaar number must be 12 digits.")
            return render(request, "addinfo.html", {"form_data": request.POST})

        if InfoSubmit.objects.filter(aadhaar_no=aadhaar_no).exclude(user=request.user).exists():
            messages.error(request, "This Aadhaar number is already registered.")
            return render(request, "addinfo.html", {"form_data": request.POST})

        if existing_info:
            existing_info.first_name = first_name
            existing_info.last_name = last_name
            existing_info.guardian_name = guardian_name
            existing_info.blood_group = blood_group
            existing_info.address = address
            existing_info.pin_code = pin_code
            existing_info.phone_no = phone_no
            existing_info.sphone_no = sphone_no
            existing_info.college_name = college_name
            existing_info.aadhaar_no = aadhaar_no
            existing_info.save()
            messages.success(request, "Information updated successfully.")
        else:
            InfoSubmit.objects.create(
                user=user,
                first_name=first_name,
                last_name=last_name,
                guardian_name=guardian_name,
                blood_group=blood_group,
                address=address,
                pin_code=pin_code,
                phone_no=phone_no,
                sphone_no=sphone_no,
                college_name=college_name,
                aadhaar_no=aadhaar_no,
                card_id=generate_card_id(user),
            )
            messages.success(request, "Information submitted successfully.")

        return redirect("nfcview")

    return render(request, "addinfo.html", {"existing_info": existing_info})


def nfcview(request):
    """
    View function to display NFC card with user information
    """
    # Generate or retrieve unique card ID
    # You can store this in a separate model or in InfoSubmit model
    
    user = request.session["username"]
    # Check flag status (adjust this based on your flag logic)
    # For example, check if user has completed registration
    flag = 'green'
    
    names = InfoSubmit.objects.filter(user=user).values('first_name', 'last_name')
    card_id = InfoSubmit.objects.filter(user=user).values('card_id')
    context = {
        'card_id': card_id,
        'flag': flag,
        'names' : names
    }
    
    return render(request, 'nfcview.html', context)



def accept_card(request):
    """
    View function to handle card acceptance
    """
    # Add your card acceptance logic here
    # For example: activate card, update database, etc.
    user = request.session["username"]
    
    try:
        # Your acceptance logic
        
        # Example: Update a field in InfoSubmit or create a card record
        if hasattr(user, 'info_submit'):
            # Add your logic here
            # user.info_submit.card_activated = True
            # user.info_submit.save()
            pass
        
        messages.success(request, 'NFC Card accepted successfully!')
        return redirect('nfcview')  # Change to your desired redirect
        
    except Exception as e:
        messages.error(request, f'Error accepting card: {str(e)}')
        return redirect('nfcview')


def generate_card_id(user):
    """
    Generate a unique card ID for the user
    You can customize this format as needed
    """
    # Check if user already has a card ID stored
    if hasattr(user, 'info_submit') and hasattr(user.info_submit, 'card_id'):
        return user.info_submit.card_id
    
    # Generate new card ID in format: XXXX-XXXX-XXXX
    unique_id = str(uuid.uuid4().hex[:12].upper())
    formatted_id = f"{unique_id[:4]}-{unique_id[4:8]}-{unique_id[8:12]}"
    if hasattr(user, 'info_submit'):
        user.info_submit.card_id = formatted_id
        user.info_submit.save()
    
    return formatted_id

def recharge_wallet(request):
    user = request.session.get("username")

    # Get NFC card (source of truth for balance & status)
    card = StudentNFCCard.objects.filter(username=user).first()

    if request.method == "POST":
        amount = request.POST.get("amount")

        try:
            amount = Decimal(amount)
            if amount <= 0:
                raise ValueError
        except:
            messages.error(request, "Invalid recharge amount")
            return redirect("recharge_wallet")

        if card.status == "BLOCKED":
            messages.error(request, "Blocked cards cannot be recharged")
            return redirect("recharge_wallet")

        card.balance += amount
        card.save(update_fields=["balance"])

        messages.success(request, f"₹{amount} added successfully")
        return redirect("recharge_wallet")

    return render(request, "recharge_wallet.html", {
        "card": card
    })
