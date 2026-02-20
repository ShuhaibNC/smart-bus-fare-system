from django.urls import path
from . import views

urlpatterns = [
    path('admin_login', views.admin_login, name='admin_login'),
    path('managenfc/', views.manage_nfc, name='manage_nfc'),
    path('managenfc/accept/<int:id>/', views.accept_nfc_card, name='accept_nfc_card'),
    path('managenfc/update/<int:id>/', views.update_nfc_card, name='update_nfc_card'),
    path("write_nfc/<str:card_id>/", views.write_nfc, name="write_nfc"),
    path("nfcwriter/<str:card_id>/", views.nfcwriter, name="nfcwriter"),
    path("managefaresystem/", views.managefaresystem, name="managefaresystem"),
    path("managefaresystem/create/", views.create_new_route, name="create_new_route"),
    path("managefaresystem/update-stop/", views.update_route_stops, name="update_route_stops"),
    path("managefaresystem/rename-route/<str:route_name>/", views.update_route_name, name="update_route_name"),
    path("all_travel_history/", views.all_travel_history, name="all_travel_history"),
]
