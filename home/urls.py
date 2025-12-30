from django.urls import path
from . import views

urlpatterns = [
    path('home', views.index, name='home'),
    path('base', views.base, name='base'),
    path('signup', views.signup, name='signup'),
    path('', views.student_login, name='student_login'),
]
