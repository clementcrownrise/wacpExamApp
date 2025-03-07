from django import forms
import datetime
from .models import Examination
from django.forms.widgets import DateInput
from django_ckeditor_5.widgets import CKEditor5Widget
#class DateInput(forms.DateInput):
#    input_type = 'date'


class ExamForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
          super().__init__(*args, **kwargs)
          self.fields["totDetails"].required = False


    class Meta:
        model = Examination
        fields = "__all__"
        widgets = {
           # 'TotDate': forms.DateInput(attrs={'type': 'date'}),
            'totDetails': CKEditor5Widget(
                attrs={"class":"django_ckeditor_5"}, config_name= "extends"
            )
            #'timetableIbadan':forms.ClearableFileInput(attrs={'type': 'form-control'}),
            #'timetableAccra':forms.ClearableFileInput(attrs={'type': 'form-control'}),
            #'timetableAbuja':forms.ClearableFileInput(attrs={'type': 'form-control'}),
            #'travelProtocol':forms.ClearableFileInput(attrs={'type': 'form-control'}),
        }

        #examName = forms.CharField(max_length=300,widget=forms.TextInput(attrs={'class': 'form-control'}))
        #totTopic = forms.CharField(max_length=400,widget=forms.TextInput(attrs={'class': 'form-control'}))
        #totFlyers = forms.FileField(widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
        #totDate = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control'}))
        #totDetails = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}))
        #timetableIbadan = forms.FileField(widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
        #timetableAccra = forms.FileField(widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
        #timetableAbuja = forms.FileField(widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
        #travelProtocol = forms.FileField(widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
        

       



