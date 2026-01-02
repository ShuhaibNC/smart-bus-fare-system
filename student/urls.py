from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.student_login, name='student_login'),
    path('block_card', views.block_card, name='block_card'),

    
]
