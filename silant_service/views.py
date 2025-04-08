from django.views.generic import ListView, TemplateView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from .models import Vehicle, TechnicalService, Complaint, ServiceCompany, Manager, Client
from django.contrib.auth.mixins import LoginRequiredMixin
from .utils.roles import get_user_role
from django.shortcuts import render, redirect
from .filters import VehicleFilter, TechnicalServiceFilter, ComplaintFilter
from django.http import HttpResponseForbidden
from django.http import HttpResponse
from .forms import TechnicalServiceForm, ComplaintForm
from django.template.loader import render_to_string


# Проверяем права доступа
class RolePermissionMixin:
    allowed_roles = []

    def dispatch(self, request, *args, **kwargs):
        if get_user_role(request.user) not in self.allowed_roles:
            return HttpResponseForbidden("Нет доступа")
        return super().dispatch(request, *args, **kwargs)
    

class HomePageView(TemplateView):
    template_name = 'home.html'
    

# Поиск на главной
def vehicle_search_view(request):
    user = request.user
    is_htmx = request.headers.get("HX-Request") == "true"

    # Если пользователь авторизован и это не HTMX-запрос — редирект
    if user.is_authenticated and not is_htmx:
        return redirect("dashboard")

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


class DashboardView(TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        role = get_user_role(user)

        # Машины
        vehicle_qs = Vehicle.objects.none()
        if role == "client":
            vehicle_qs = Vehicle.objects.filter(client__user=user)
        elif role == "service":
            vehicle_qs = Vehicle.objects.filter(service_company__user=user)
        elif role == "manager":
            vehicle_qs = Vehicle.objects.all()

        vehicle_filter = VehicleFilter(self.request.GET, queryset=vehicle_qs)
        context["vehicle_filter"] = vehicle_filter
        context["vehicles"] = vehicle_filter.qs.order_by("-ship_date")

        # ТО
        service_qs = TechnicalService.objects.none()
        if role == "client":
            service_qs = TechnicalService.objects.filter(vehicle__client__user=user)
        elif role == "service":
            service_qs = TechnicalService.objects.filter(service_company__user=user)
        elif role == "manager":
            service_qs = TechnicalService.objects.all()

        service_filter = TechnicalServiceFilter(self.request.GET, queryset=service_qs)
        context["service_filter"] = service_filter
        context["services"] = service_filter.qs.order_by("-service_date")  

        # Рекламации
        complaint_qs = Complaint.objects.none()
        if role == "client":
            complaint_qs = Complaint.objects.filter(vehicle__client__user=user)
        elif role == "service":
            complaint_qs = Complaint.objects.filter(vehicle__service_company__user=user)
        elif role == "manager":
            complaint_qs = Complaint.objects.all()

        complaint_filter = ComplaintFilter(self.request.GET, queryset=complaint_qs)
        context["complaint_filter"] = complaint_filter
        context["complaints"] = complaint_filter.qs.order_by("-failure_date") 

        # Добавляем роль пользователя в контекст 
        if role == "client":
            context["company"] = Client.objects.filter(user=user).first()
        elif role == "service":
            context["company"] = ServiceCompany.objects.filter(user=user).first()
        elif role == "manager":
            context["company"] = Manager.objects.filter(user=user).first()

        context["role"] = role
        return context



# Создание записи ТО
class TechnicalServiceCreateView(LoginRequiredMixin, RolePermissionMixin, CreateView):
    model = TechnicalService
    form_class = TechnicalServiceForm
    template_name = "form.html"
    success_url = "/service/dashboard/"
    allowed_roles = ["manager", "service", "client"]

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        role = get_user_role(self.request.user)

        if role == "client":
            form.fields['vehicle'].queryset = Vehicle.objects.filter(client__user=self.request.user)
            form.fields['service_company'].disabled = True
            form.fields['tech_company'].disabled = True

        elif role == "service":
            form.fields['vehicle'].queryset = Vehicle.objects.filter(service_company__user=self.request.user)
            form.fields['service_company'].initial = ServiceCompany.objects.get(user=self.request.user)

        return form

# Рекламация - создание   
class ComplaintCreateView(LoginRequiredMixin, RolePermissionMixin, CreateView):
    model = Complaint
    form_class = ComplaintForm
    template_name = "form.html"
    success_url = "/service/dashboard/"
    allowed_roles = ["manager", "service"]

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        role = get_user_role(self.request.user)

        if role == "service":
            form.fields['vehicle'].queryset = Vehicle.objects.filter(service_company__user=self.request.user)

        return form


# ТО - редактирование
class TechnicalServiceUpdateView(LoginRequiredMixin, RolePermissionMixin, UpdateView):
    model = TechnicalService
    form_class = TechnicalServiceForm
    template_name = "form.html"
    success_url = "/service/dashboard/"
    allowed_roles = ["manager", "service", "client"]

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        role = get_user_role(self.request.user)

        if role == "client":
            form.fields['vehicle'].queryset = Vehicle.objects.filter(client__user=self.request.user)
            form.fields['service_company'].disabled = True
            form.fields['tech_company'].disabled = True
        elif role == "service":
            form.fields['vehicle'].queryset = Vehicle.objects.filter(service_company__user=self.request.user)
            form.fields['service_company'].initial = ServiceCompany.objects.get(user=self.request.user)

        return form


# Рекламации - редактирование
class ComplaintUpdateView(LoginRequiredMixin, RolePermissionMixin, UpdateView):
    model = Complaint
    form_class = ComplaintForm
    template_name = "form.html"
    success_url = "/dashboard/"
    allowed_roles = ["manager", "service"] 

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        role = get_user_role(self.request.user)

        if role == "service":
            form.fields['vehicle'].queryset = Vehicle.objects.filter(service_company__user=self.request.user)
        return form
    
# Детали
class ComplaintDetailView(LoginRequiredMixin, RolePermissionMixin, DetailView):
    model = Complaint
    template_name = "complaint_detail.html"
    context_object_name = "complaint"
    allowed_roles = ["manager", "service", "client"]

    def get_queryset(self):
        role = get_user_role(self.request.user)
        base_qs = super().get_queryset()

        if role == "client":
            return base_qs.filter(vehicle__client__user=self.request.user)
        elif role == "service":
            return base_qs.filter(vehicle__service_company__user=self.request.user)
        elif role == "manager":
            return base_qs
        return base_qs.none()
    
    
class TechnicalServiceDetailView(LoginRequiredMixin, RolePermissionMixin, DetailView):
    model = TechnicalService
    template_name = "technicalservice_detail.html"
    context_object_name = "service"
    allowed_roles = ["manager", "service", "client"]

    def get_queryset(self):
        role = get_user_role(self.request.user)
        base_qs = super().get_queryset()

        if role == "client":
            return base_qs.filter(vehicle__client__user=self.request.user)
        elif role == "service":
            return base_qs.filter(service_company__user=self.request.user)
        elif role == "manager":
            return base_qs
        return base_qs.none()
    

class VehicleDetailView(LoginRequiredMixin, RolePermissionMixin, DetailView):
    model = Vehicle
    template_name = "vehicle_detail.html"
    context_object_name = "vehicle"
    allowed_roles = ["manager", "service", "client"]

    def get_queryset(self):
        role = get_user_role(self.request.user)
        base_qs = super().get_queryset()

        if role == "client":
            return base_qs.filter(client__user=self.request.user)
        elif role == "service":
            return base_qs.filter(service_company__user=self.request.user)
        elif role == "manager":
            return base_qs
        return base_qs.none()


def dashboard_vehicles_partial(request):
    user = request.user
    role = get_user_role(user)
    qs = Vehicle.objects.none()
    if role == "client":
        qs = Vehicle.objects.filter(client__user=user)
    elif role == "service":
        qs = Vehicle.objects.filter(service_company__user=user)
    elif role == "manager":
        qs = Vehicle.objects.all()

    vehicle_filter = VehicleFilter(request.GET, queryset=qs)
    html = render_to_string("partials/tab_vehicles.html", {
        "vehicles": vehicle_filter.qs.order_by("-ship_date"),
        "role": role
    })
    return HttpResponse(html)

# Аналогично для service и complaints:
def dashboard_services_partial(request):
    user = request.user
    role = get_user_role(user)
    qs = TechnicalService.objects.none()
    if role == "client":
        qs = TechnicalService.objects.filter(vehicle__client__user=user)
    elif role == "service":
        qs = TechnicalService.objects.filter(service_company__user=user)
    elif role == "manager":
        qs = TechnicalService.objects.all()

    service_filter = TechnicalServiceFilter(request.GET, queryset=qs)
    html = render_to_string("partials/tab_services.html", {
        "services": service_filter.qs.order_by("-service_date"),
        "role": role
    })
    return HttpResponse(html)

def dashboard_complaints_partial(request):
    user = request.user
    role = get_user_role(user)
    qs = Complaint.objects.none()
    if role == "client":
        qs = Complaint.objects.filter(vehicle__client__user=user)
    elif role == "service":
        qs = Complaint.objects.filter(vehicle__service_company__user=user)
    elif role == "manager":
        qs = Complaint.objects.all()

    complaint_filter = ComplaintFilter(request.GET, queryset=qs)
    html = render_to_string("partials/tab_complaints.html", {
        "complaints": complaint_filter.qs.order_by("-failure_date"),
        "role": role
    })
    return HttpResponse(html)