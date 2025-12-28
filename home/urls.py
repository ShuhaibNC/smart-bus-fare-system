from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('base', views.base, name='base'),
    path('signup', views.signup, name='signup'),
]
