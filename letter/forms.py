from django import forms
from . models import Examination
from faculty.models import Faculty

class ExcelUploadForm(forms.Form):
    #examination = forms.ModelChoiceField(queryset=Examination.objects.all(),empty_label='Select an Examination'
    #                                     ,widget=forms.Select(attrs={'class': 'form-control'}))
    file = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control'}))
    
class SearchForm(forms.Form):
    examination = forms.ModelChoiceField(queryset=Examination.objects.all(), 
                                         required=True, empty_label="Select Examination")
    faculty = forms.ModelChoiceField(queryset=Faculty.objects.all(), required=True,
                                     to_field_name="facultyName",
                                     empty_label="Select Faculty")