from django.urls import path
from . import views

urlpatterns = [
    path('setroute/', views.set_route),
]
