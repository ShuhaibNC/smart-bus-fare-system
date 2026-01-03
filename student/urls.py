from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.student_login, name='student_login'),
    path('cardblock/', views.block_card, name='block_card'),
    path('manage_card/', views.manage_card, name='manage_card'),
    path('', views.student_login, name='student_login'),
]
