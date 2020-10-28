from django import forms
from .models import Payroll, Person, Occupation
from .widget import XDSoftDateTimePickerInput
from .calendar_models import PersonSchedule


class BaseForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class PersonScheduleForm(BaseForm, forms.ModelForm):
    date_start = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M'],
        widget=XDSoftDateTimePickerInput(attrs={'autocomplete': 'off'}), label='From..'
    )

    date_end = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M'],
        widget=XDSoftDateTimePickerInput(attrs={'autocomplete': 'off'}), label='Until...'
    )
    person = forms.ModelChoiceField(queryset=Person.objects.all(), widget=forms.HiddenInput())

    class Meta:
        model = PersonSchedule
        fields = ['date_start', 'date_end', 'person', 'category']


class PayrollForm(BaseForm, forms.ModelForm):
    date_expired = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}), label='Date')

    class Meta:
        model = Payroll
        fields = ['is_paid', 'date_expired', 'person', 'title', 'category', 'value', 'notes', ]


class PersonForm(BaseForm, forms.ModelForm):

    class Meta:
        model = Person
        fields = ['active', 'title', 'phone', 'phone1', 'occupation',
         'value_per_hour', 'extra_per_hour'
                  ]


class PayrollPersonForm(PayrollForm):
    person = forms.ModelChoiceField(queryset=Person.objects.all(), widget=forms.HiddenInput())


class OccupationForm(BaseForm, forms.ModelForm):
    
    class Meta:
        model = Occupation
        fields = ("title",)