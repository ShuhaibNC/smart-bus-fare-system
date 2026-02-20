from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate
from django.utils import timezone
from django.http import HttpResponse
from decimal import Decimal
from django.contrib import messages
from .models import Login, StudentNFCCard, BusRoute, InfoSubmit
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
)
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import HRFlowable
from system_admin.models import BusFee, BusLog
import json
import uuid
from system_admin.models import Transaction
from django.db import transaction
from io import BytesIO
from datetime import datetime

def block_card(request):
    return render(request, 'block_card.html')

def addinfo(request):
    return render(request, 'addinfo.html')

def block(request):
    try:
        card = StudentNFCCard.objects.get(username=request.session["username"])
    except StudentNFCCard.DoesNotExist:
        card = None
    if request.method == "POST":
        card_id = request.POST.get("card_id")
        reason = request.POST.get("reason")
        remarks = request.POST.get("remarks")
        
        if not card or card.card_id != card_id:
            messages.success(request, f"Invalid NFC Card ID. {card.card_id} and {card_id} not matching")
            return redirect("block")

        if card.status == "BLOCKED":
            messages.success(request, "Your card is already blocked.")
            return redirect("block")

        card.status = "BLOCKED"
        card.block_reason = reason
        card.remarks = remarks
        card.blocked_at = timezone.now()
        card.save()

        messages.success(request, "Your NFC card has been blocked successfully.")
        return redirect('block_card')

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

        request.session["user_id"] = user.id
        request.session["username"] = user.username
        request.session["role"] = user.role
        return redirect("home")   # change to whatever page you want after login

    return render(request, "student_login.html")

def set_route(request):
    username = request.session["username"]
    info = None
    flag = "green"

    if username:
        # Assuming Login is your user model or related to it
        if BusRoute.objects.filter(user=username).exists():
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
        username = request.session["username"]
        if not username:
            return redirect('login') # Or handle error

        stop1 = request.POST.get('stop1')
        stop2 = request.POST.get('stop2')
        
        # Create the route
        BusRoute.objects.create(
            user=username,
            stop1=stop1,
            stop2=stop2,
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
    card = StudentNFCCard.objects.filter(username=user).first()
    student_info = InfoSubmit.objects.filter(user=user).first()
    if not card:
        messages.error(request, "Card not found")
        return redirect("recharge_wallet")

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

        try:
            with transaction.atomic():

                # 1. Create transaction record (pending)
                txn = Transaction.objects.create(
                    transaction_id=uuid.uuid4(),
                    amount=amount,
                    status="pending",
                    description="Wallet Recharge"
                )

                # 2. Update balance
                card.balance += amount
                card.save(update_fields=["balance"])

                # 3. Mark transaction completed
                txn.status = "completed"
                txn.save(update_fields=["status"])

        except Exception as e:
            messages.error(request, "Recharge failed. Try again.")
            return redirect("recharge_wallet")

        messages.success(request, f"₹{amount} added successfully")
        return redirect("recharge_wallet")

    return render(request, "recharge_wallet.html", {
        "card": card,
        "student_info": student_info
    })


def get_refund(request):
    if request.method == "POST":
        transaction_id = request.POST.get("transaction_id")
        message_text = request.POST.get("message")

        # Save refund request logic here

        messages.success(request, "Refund request sent successfully.")
        return redirect("getrefund")  # or your URL name

    return render(request, "getrefund.html")

def download_receipt_file(request, transaction_id):

    username = request.session.get("username")

    if not username:
        messages.error(request, "You must be logged in.")
        return redirect("login")

    txn = get_object_or_404(
        Transaction,
        transaction_id=transaction_id,
        username=username
    )

    if txn.status != "completed":
        messages.error(request, "Receipt not available for this transaction.")
        return redirect("transaction_list")

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=50,
        leftMargin=50,
        topMargin=60,
        bottomMargin=40
    )

    elements = []

    styles = getSampleStyleSheet()

    # Custom Styles
    title_style = ParagraphStyle(
        "TitleStyle",
        parent=styles["Heading1"],
        fontSize=22,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#1a237e"),
        spaceAfter=20
    )

    amount_style = ParagraphStyle(
        "AmountStyle",
        parent=styles["Heading2"],
        fontSize=18,
        textColor=colors.HexColor("#2e7d32"),
        spaceAfter=10
    )

    right_style = ParagraphStyle(
        "RightStyle",
        parent=styles["Normal"],
        alignment=TA_RIGHT,
        fontSize=9,
        textColor=colors.grey
    )

    normal_style = styles["Normal"]
    # Header
    elements.append(Paragraph("PAYMENT RECEIPT", title_style))
    elements.append(HRFlowable(width="100%", thickness=1, color=colors.grey))
    elements.append(Spacer(1, 0.3 * inch))
    # Amount Highlight
    elements.append(Paragraph(f"Amount Paid: ₹ {txn.amount}", amount_style))
    elements.append(Spacer(1, 0.2 * inch))
    # Transaction Table
    data = [
        ["Transaction ID", str(txn.transaction_id)],
        ["Username", txn.username],
        ["Status", txn.status.capitalize()],
        ["Payment Date", txn.created_at.strftime("%d %b %Y, %H:%M")],
    ]

    table = Table(data, colWidths=[160, 300])

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.whitesmoke),
        ("BOX", (0, 0), (-1, -1), 0.8, colors.HexColor("#d0d0d0")),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#eeeeee")),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 11),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, -1), (-1, -1), 8),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 0.5 * inch))

    elements.append(HRFlowable(width="100%", thickness=0.8, color=colors.grey))
    elements.append(Spacer(1, 0.2 * inch))

    # Footer
    elements.append(Paragraph(
        "This is a system generated receipt. No signature required.",
        normal_style
    ))

    elements.append(Spacer(1, 0.1 * inch))

    elements.append(Paragraph(
        f"Generated on {datetime.now().strftime('%d %b %Y, %H:%M')}",
        right_style
    ))

    doc.build(elements)

    pdf = buffer.getvalue()
    buffer.close()

    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = (
        f'attachment; filename="receipt_{txn.transaction_id}.pdf"'
    )

    return response


def receipt_downloader(request):
    return render(request, "receiptdownloader.html")

def travel_history(request):
    username = request.session["username"]
    tap_records = BusLog.objects.filter(student_name=username).order_by("-tap_date", "-tap_time")
    return render(request, "travel_history.html", {"tap_records": tap_records})