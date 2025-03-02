
from django.contrib import admin
from django.urls import path
from .import views

app_name = 'examination'

urlpatterns = [
    path("",views.index, name="index"),
    path("create/", views.createExam ,name='createExam'),
    path("selected/", views.selected , name='selected'),
    path("details/<int:examination_id>", views.exam_details, name='details'),
    path("edit/<int:examination_id>", views.examEdit, name='edit'),
    path('delete/<int:examination_id>', views.deleteExam, name='deleteExam'),
]