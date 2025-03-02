
from django.contrib import admin
from django.urls import path
from . import views
from . views import upload_excel

app_name = "letter"


urlpatterns = [
    path("",views.index, name="index"),
    path("create/", views.upload_excel ,name='createLetter'),
    path("mailsample/<int:letter_id>", views.mailSample, name='mailsample'),
    path("details/<int:letter_id>", views.letterDetails ,name='details'),
    path('deleteAll/', views.deleteAll, name='deleteAll'),
    path('send-email/', views.send_personalized_email, name='send-email'),
    path('send-letter/<int:id>', views.sendLetter, name='send-letter'),

]


