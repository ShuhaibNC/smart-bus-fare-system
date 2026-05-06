# Smart Bus Fare System

A smart NFC-based bus fare collection and management system built using Django.

The system allows students to use NFC cards for cashless bus fare payments, manage wallet balances, track travel history, and securely handle transactions through a centralized cloud-based platform.

The homepage features a modern responsive interface with desktop and mobile optimized layouts, including NFC payment access, wallet management, travel tracking, and administrative controls. :contentReference[oaicite:0]{index=0}

---

# Features

- NFC-based smart bus fare system
- Cashless travel management
- Wallet recharge and balance tracking
- Travel history management
- NFC card management
- Refund system
- Receipt generation and downloads
- Lost/stolen NFC card blocking
- Admin fare management
- Full transaction tracking
- Responsive desktop and mobile interface
- Cloud-based transaction synchronization

---

# Modules

## Home
- [x] signup

## Student
- [x] student_login
- [x] set_route
- [x] info_submit
- [x] view_nfc_card
- [x] view_balance
- [x] recharge_wallet
- [x] add_balance
- [x] refund_system
- [x] download_reciepts
- [x] block_stolen_lost_card
- [x] travel_history
- [x] transactions

## System Admin
- [x] admin_login
- [x] mange_nfc_applications
- [x] manage_fare_system
- [x] full_travel_history
- [x] all_transactions

---

# Technologies Used

- Django
- Python
- HTML
- CSS
- JavaScript
- SCSS
- MariaDB
- NFC Technology

---

# Project Structure

```text
shuhaibnc-smart-bus-fare-system/
│
├── hardware/
│   ├── bus_scanner.py
│   └── nfc_writer.py
│
├── home/
├── student/
├── system_admin/
├── smart_bus_fare_system/
├── static/
├── manage.py
├── requirements.txt
└── README.md
```

---

# Hardware Integration

The project includes NFC hardware integration scripts:

## NFC Bus Scanner

```text
hardware/bus_scanner.py
```

Used for:
- Reading NFC cards
- Fare verification
- Transaction processing

## NFC Writer

```text
hardware/nfc_writer.py
```

Used for:
- Writing student NFC cards
- NFC card initialization
- Card registration

---

# Installation

## Clone Repository

```bash
git clone https://github.com/shuhaibnc/shuhaibnc-smart-bus-fare-system.git
cd shuhaibnc-smart-bus-fare-system
```

---

## Create Virtual Environment

### Linux/macOS

```bash
python -m venv venv
source venv/bin/activate
```

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Database Configuration

Set database configuration in:

```text
smart_bus_fare_system/settings.py
```

Replace database configuration with:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '', # Enter Database name here
        'USER': '', # Enter Database username here
        'PASSWORD': '', # Enter DB Password here
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

Make sure MariaDB server is installed and running before migrating the database.

---

# Apply Migrations

```bash
python manage.py migrate
```

---

# Create Superuser

```bash
python manage.py createsuperuser
```

---

# Run Development Server

```bash
python manage.py runserver
```

Open browser:

```text
http://127.0.0.1:8000/
```

---

# Student Features

Students can:

- Apply for NFC cards
- Recharge wallet balance
- View travel history
- Download payment receipts
- View NFC card details
- Request refunds
- Block lost or stolen cards
- Track transactions

---

# Admin Features

System administrators can:

- Manage NFC applications
- Configure fare systems
- Monitor transactions
- View complete travel history
- Manage NFC card writing

---

# Security Features

- Secure authentication
- NFC-based verification
- Wallet transaction tracking
- Controlled admin access
- Cloud-based synchronization
- Lost card blocking system

---

# Future Improvements

- QR payment integration
- Real-time GPS bus tracking
- Push notifications
- Mobile application
- Multi-bus support
- AI-based fare analytics
- Online recharge gateway integration

---

# Authors

Developed by:

- Shuhaib N C
- Azad Rajeev

---

# License

This project is developed for academic and educational purposes.