from django.db import models

# Create your models here.
class Faculty(models.Model):
    facultyName = models.CharField(max_length=200)
    

    def __str__(self):
            return self.facultyName