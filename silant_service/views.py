from django.views.generic import ListView, TemplateView
from .models import Vehicle
from .utils.roles import get_user_role
from django.shortcuts import render, redirect


class HomePageView(TemplateView):
    template_name = 'home.html'
    
    
class VehicleListView(ListView):
    model = Vehicle
    template_name = "vehicle_list.html"
    context_object_name = "vehicles"

    def get_queryset(self):
        user = self.request.user
        role = get_user_role(user)

        if role == "client":
            return Vehicle.objects.filter(client__user=user)
        elif role == "service":
            return Vehicle.objects.filter(service_company__user=user)
        elif role == "manager":
            return Vehicle.objects.all()
        else:
            return Vehicle.objects.only(
                "serial_number",
                "tech_model",
                "engine_model",
                "serial_engine",
                "model_transmission",
                "serial_transmission",
                "model_axle",
                "serial_axle",
                "model_man_axle",
                "serial_man_axle",
            )



# Поиск на главной
def vehicle_search_view(request):
    user = request.user
    is_htmx = request.headers.get("HX-Request") == "true"

    # Если пользователь авторизован и это не HTMX-запрос — редирект
    if user.is_authenticated and not is_htmx:
        return redirect("vehicle_list")

    serial_number = request.GET.get("serial_number")
    vehicle = None

    if serial_number:
        try:
            vehicle = Vehicle.objects.only(
                "serial_number",
                "tech_model",
                "engine_model",
                "serial_engine",
                "model_transmission",
                "serial_transmission",
                "model_axle",
                "serial_axle",
                "model_man_axle",
                "serial_man_axle"
            ).get(serial_number=serial_number)
        except Vehicle.DoesNotExist:
            vehicle = None

    return render(request, "partials/information_table.html", {
        "vehicle": vehicle,
        "search_mode": True,
    })
