from django.contrib import admin
from .models import Faculty

class FacultyAdmin(admin.ModelAdmin):
    list_display =('id', 'facultyName')

admin.site.register(Faculty, FacultyAdmin)