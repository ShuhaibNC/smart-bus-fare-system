from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.student_login, name='student_login'),
    path('block_card/', views.block_card, name='block_card'),
    path('manage_card/', views.manage_card, name='manage_card'),
    path('', views.student_login, name='student_login'),
    path('student_wallet/', views.view_balance, name='student_wallet'),
    

]
