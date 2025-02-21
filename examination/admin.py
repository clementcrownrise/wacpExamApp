from django.contrib import admin
from .models import Examination
# Register your models here.

class ExaminationAdmin(admin.ModelAdmin):
        list_display = ["examName", "totTopic"]


admin.site.register(Examination, ExaminationAdmin)
