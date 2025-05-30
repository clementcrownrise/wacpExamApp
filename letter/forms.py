from django import forms
from . models import Examination
from faculty.models import Faculty

class ExcelUploadForm(forms.Form):
    #examination = forms.ModelChoiceField(queryset=Examination.objects.all(),empty_label='Select an Examination'
    #                                     ,widget=forms.Select(attrs={'class': 'form-control'}))
    file = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control'}))
    
class SearchForm(forms.Form):
    STATUS_CHOICES = [
         ("", "Select Status"),
         ("Not Sent", "Not Sent"),
         ("Sent", "Sent"),
    ]
    examination = forms.ModelChoiceField(queryset=Examination.objects.all(), 
                                         required=True, empty_label="Select Examination")
    faculty = forms.ModelChoiceField(queryset=Faculty.objects.all(), required=True,
                                     to_field_name="facultyName",
                                     empty_label="Select Faculty")
    
    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        label="Status",
        required=True
    )