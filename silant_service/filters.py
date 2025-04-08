import django_filters
from .models import Vehicle, TechnicalService, Complaint, ReferenceItem, ServiceCompany

class VehicleFilter(django_filters.FilterSet):
    tech_model = django_filters.ModelChoiceFilter(
        label="Модель техники",
        queryset=ReferenceItem.objects.filter(type=ReferenceItem.MODEL_TECH)
    )
    engine_model = django_filters.ModelChoiceFilter(
        label="Модель двигателя",
        queryset=ReferenceItem.objects.filter(type=ReferenceItem.TYPE_ENGINE)
    )
    model_transmission = django_filters.ModelChoiceFilter(
        label="Модель трансмиссии",
        queryset=ReferenceItem.objects.filter(type=ReferenceItem.TYPE_TRANSMISSION)
    )
    model_man_axle = django_filters.ModelChoiceFilter(
        label="Модель управляемого моста",
        queryset=ReferenceItem.objects.filter(type=ReferenceItem.TYPE_MAN_AXLE)
    )
    model_axle = django_filters.ModelChoiceFilter(
        label="Модель ведущего моста",
        queryset=ReferenceItem.objects.filter(type=ReferenceItem.TYPE_AXLE)
    )

    class Meta:
        model = Vehicle
        fields = ['tech_model', 'engine_model', 'model_transmission', 'model_axle', 'model_man_axle']


class TechnicalServiceFilter(django_filters.FilterSet):
    service_type = django_filters.ModelChoiceFilter(
        label="Вид ТО",
        queryset=ReferenceItem.objects.filter(type=ReferenceItem.TYPE_TO)
    )
    vehicle__serial_number = django_filters.CharFilter(label="Зав. номер", lookup_expr='icontains')
    service_company = django_filters.ModelChoiceFilter(
        label="Сервисная компания",
        queryset=ServiceCompany.objects.all()
    )

    class Meta:
        model = TechnicalService
        fields = ['service_type', 'vehicle__serial_number', 'service_company']


class ComplaintFilter(django_filters.FilterSet):
    failure_node = django_filters.ModelChoiceFilter(
        label="Узел отказа",
        queryset=ReferenceItem.objects.filter(type=ReferenceItem.NODE_FAILURE)
    )
    recovery_method = django_filters.ModelChoiceFilter(
        label="Способ восстановления",
        queryset=ReferenceItem.objects.filter(type=ReferenceItem.RECOVERY_METHOD)
    )
    vehicle__service_company = django_filters.ModelChoiceFilter(
        label="Сервисная компания",
        queryset=ServiceCompany.objects.all()
    )

    class Meta:
        model = Complaint
        fields = ['failure_node', 'recovery_method', 'vehicle__service_company']