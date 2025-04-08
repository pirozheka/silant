from django import forms
from .models import TechnicalService, Complaint, ReferenceItem
from django.forms.widgets import DateInput

class DateInputWidget(DateInput):
    input_type = 'date'

class TechnicalServiceForm(forms.ModelForm):
    class Meta:
        model = TechnicalService
        fields = '__all__'
        widgets = {
            'service_date': DateInputWidget(),
            'order_date': DateInputWidget(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['service_type'].queryset = ReferenceItem.objects.filter(type=ReferenceItem.TYPE_TO)

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = '__all__'
        widgets = {
            'failure_date': DateInputWidget(),
            'recovery_date': DateInputWidget(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['failure_node'].queryset = ReferenceItem.objects.filter(type=ReferenceItem.NODE_FAILURE)
        self.fields['recovery_method'].queryset = ReferenceItem.objects.filter(type=ReferenceItem.RECOVERY_METHOD)