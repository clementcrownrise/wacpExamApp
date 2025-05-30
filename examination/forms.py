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
        labels = {
            'examName': 'Exam Name',
            'totTopic': 'TOT Topic',
            'totFlyers': 'TOT Flyer(must be jpeg/jpg)',
            'totDate': 'TOT Date',
            'totDetails': 'TOT Details',
            'arrivalinfo': 'Arrival Information(for CEs)',
            'timetableIbadan': 'Timetable for Ibadan',
            'timetableAccra': 'Timetable for Accra',
            'timetableAbuja': 'Timetable for Abuja',
            'travelProtocol': 'Travel Protocol Document',
        }
        widgets = {  
             
            'examName': forms.TextInput(attrs={'class': 'form-control'}),
            'totTopic': forms.TextInput(attrs={'class': 'form-control'}),
            'totDate': forms.TextInput(attrs={'class': 'form-control'}),
            'arrivalinfo': forms.Textarea(attrs={'class': 'form-control'}),
            'totDetails': forms.Textarea(attrs={'class': 'form-control'}),
            'totFlyers': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'timetableIbadan': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'timetableAccra': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'timetableAbuja': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'travelProtocol': forms.ClearableFileInput(attrs={'class': 'form-control'}),

            #'examName' : forms.CharField(max_length=300,widget=forms.TextInput(attrs={'class': 'form-control'})),
            #'totTopic' : forms.CharField(max_length=400,widget=forms.TextInput(attrs={'class': 'form-control'})),
            #'totFlyers' : forms.FileField(widget=forms.ClearableFileInput(attrs={'class': 'form-control'})),
            #'totDate' : forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control'})),
            #'arrivalinfo' : forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4})),
            #'totDetails' : forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4})),
            #'timetableIbadan' : forms.FileField(widget=forms.ClearableFileInput(attrs={'class': 'form-control'})),
            #'timetableAccra' : forms.FileField(widget=forms.ClearableFileInput(attrs={'class': 'form-control'})),
            #'timetableAbuja' : forms.FileField(widget=forms.ClearableFileInput(attrs={'class': 'form-control'})),
            #'travelProtocol' : forms.FileField(widget=forms.ClearableFileInput(attrs={'class': 'form-control'})),
        }

       



