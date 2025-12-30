from django.urls import path
from . import views

urlpatterns = [
    path('setroute/', views.set_route),
    path("routes/add/", views.add_route, name="add_route"),
]
