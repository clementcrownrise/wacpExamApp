from django.db import models
from examination.models import Examination

class TimeStampedModel(models.Model):
    """Abstract base class that adds created_at and updated_at fields to models."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# Create your models here.
class Letter(TimeStampedModel):
    examination = models.ForeignKey(Examination, on_delete=models.CASCADE,related_name='letters')
    surname = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    institutionAddress = models.CharField(max_length=300)
    role = models.CharField(max_length=300)
    membershipOrFellowship = models.CharField(max_length=300)
    hotel = models.CharField(max_length=400, default='')
    meal = models.CharField(max_length=400, default='')
    cc = models.CharField(max_length=400, default='')
    centerOfTheExamination = models.CharField(max_length=200)
    countryOfTheExamination = models.CharField(max_length=200, default='')
    onOrBefore = models.CharField(max_length=200, default='')
    holdAt  = models.CharField(max_length=200, default='')
    InstitutionAddressCountry  = models.CharField(max_length=300, default='')
    faculty  = models.CharField(max_length=200, default='')
    arrivalDate = models.CharField(max_length=20, default='')
    depatureDate = models.CharField(max_length=20, default='')
    email = models.CharField(max_length=200)
    userType = models.CharField(max_length=200, default='')
    

    def __str__(self):
        return self.examination.examName
 