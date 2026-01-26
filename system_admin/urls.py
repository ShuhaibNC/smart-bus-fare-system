from django.urls import path
from . import views

urlpatterns = [
    path('admin_login', views.admin_login, name='admin_login'),
    path('managenfc/', views.manage_nfc, name='manage_nfc'),
    path('managenfc/accept/<int:id>/', views.accept_nfc_card, name='accept_nfc_card'),
    path('managenfc/update/<int:id>/', views.update_nfc_card, name='update_nfc_card'),
    path("write_nfc/", views.write_nfc, name="write_nfc"),
    
]
