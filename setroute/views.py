from django.shortcuts import render,redirect
from home.models import Login
from .models import BusRoute

def set_route(request):
    return render(request, 'set_route.html')
def add_route(request):
    if request.method == "POST":
        stops = request.POST.getlist("stops[]")

        # Keep only the first four and pad if fewer
        stops = (stops + ["", "", "", ""])[:4]

        # Example login handling. Adjust if your session key is different
        login_id = request.session.get("user_id")

        if login_id is None:
            return redirect("/")   # or wherever your login page is

        login_user = Login.objects.get(id=login_id)
        
        BusRoute.objects.create(
            user=login_user,
            stop1=stops[0],
            stop2=stops[1],
            stop3=stops[2],
            stop4=stops[3],
        )

        return redirect("add_route")

    return render(request, "set_route.html")