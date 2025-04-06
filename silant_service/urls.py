from django.urls import path
from .views import VehicleListView
from .views import vehicle_search_view



urlpatterns = [
    path("vehicles/", VehicleListView.as_view(), name="vehicle_list"),
    path("search/", vehicle_search_view, name="vehicle_search"),
]
