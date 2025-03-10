from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django.forms.widgets import DateInput
#from .forms import UploadFileForm


# Create your models here.
class Examination(models.Model):
    examName = models.CharField(max_length=200)
    totTopic = models.CharField(max_length=200)
    totFlyers =models.ImageField(upload_to='uploads/' , blank=True, null=True)
    totDate = models.CharField(max_length=200)
    totDetails = CKEditor5Field('TOT Details', config_name='comment')
    timetableIbadan = models.FileField(upload_to='uploads/')
    timetableAccra = models.FileField(upload_to='uploads/')
    timetableAbuja = models.FileField(upload_to='uploads/')
    travelProtocol = models.FileField(upload_to='uploads/')

    def __str__(self):
            return self.examName



    
