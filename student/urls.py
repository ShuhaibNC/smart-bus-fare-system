from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.student_login, name='student_login'),
    path('setroute/', views.set_route, name="set_route"),
    path("routes/add/", views.add_route, name="add_route"),
    path('cardblock/', views.block_card, name='block_card'),
    path('manage_card/', views.manage_card, name='manage_card'),
    path('', views.student_login, name='student_login'),
    path('student_wallet/', views.view_balance, name='student_wallet'),
    path('addinfo/', views.addinfo, name="addinfo"),
    path('infosubmit/', views.infosubmit, name='infosubmit'),
    path('nfcview/', views.nfcview, name='nfcview'),
    path('accept-card/', views.accept_card, name='accept_card'),
    path("recharge_wallet/", views.recharge_wallet, name="recharge_wallet"),
]
