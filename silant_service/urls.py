from django.urls import path
from .views import (
    DashboardView, 
    TechnicalServiceCreateView, 
    ComplaintCreateView, 
    TechnicalServiceUpdateView, 
    ComplaintUpdateView, 
    ComplaintDetailView,
    TechnicalServiceDetailView,
    VehicleDetailView,
    dashboard_vehicles_partial,
    dashboard_services_partial,
    dashboard_complaints_partial,
    vehicle_search_view
    )


urlpatterns = [
    path("search/", vehicle_search_view, name="vehicle_search"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("technicalservice/add/", TechnicalServiceCreateView.as_view(), name="technicalservice_create"),
    path("complaint/add/", ComplaintCreateView.as_view(), name="complaint_create"),
    path("technicalservice/<int:pk>/edit/", TechnicalServiceUpdateView.as_view(), name="technicalservice_edit"),
    path("complaint/<int:pk>/edit/", ComplaintUpdateView.as_view(), name="complaint_edit"),
    path("complaint/<int:pk>/", ComplaintDetailView.as_view(), name="complaint_detail"),
    path("technicalservice/<int:pk>/", TechnicalServiceDetailView.as_view(), name="technicalservice_detail"),
    path("vehicle/<int:pk>/", VehicleDetailView.as_view(), name="vehicle_detail"),
    path("dashboard/vehicles-partial/", dashboard_vehicles_partial, name="dashboard_vehicles_partial"),
    path("dashboard/services-partial/", dashboard_services_partial, name="dashboard_services_partial"),
    path("dashboard/complaints-partial/", dashboard_complaints_partial, name="dashboard_complaints_partial"),
]
