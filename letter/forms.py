from django import forms
from . models import Examination

class ExcelUploadForm(forms.Form):
    #examination = forms.ModelChoiceField(queryset=Examination.objects.all(),empty_label='Select an Examination'
    #                                     ,widget=forms.Select(attrs={'class': 'form-control'}))
    file = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control'}))
    
