from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.student_login, name='student_login'),
    path('setroute/', views.set_route, name="set_route"),
    path("routes/add/", views.add_route, name="add_route"),
    path('block/', views.block, name='block'),
    path('block_card/', views.block_card, name='block_card'),
    path('', views.student_login, name='student_login'),
    path('student_wallet/', views.view_balance, name='student_wallet'),
    path('addinfo/', views.addinfo, name="addinfo"),
    path('infosubmit/', views.infosubmit, name='infosubmit'),
    path('nfcview/', views.nfcview, name='nfcview'),
    path('accept-card/', views.accept_card, name='accept_card'),
    path("recharge_wallet/", views.recharge_wallet, name="recharge_wallet"),
    path("getrefund/", views.get_refund, name="getrefund"),
    path("receipt/<uuid:transaction_id>", views.download_receipt_file, name="download_receipt_file"),
    path("receipt_downloader/", views.receipt_downloader, name="receipt_downloader"),
    path("travel_history/", views.travel_history, name="travel_history"),
    path("my_transactions/", views.my_transactions, name="my_transactions"),
]
