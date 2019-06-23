
from django.contrib import admin
from django.urls import path
from . import views


app_name ="app1"
urlpatterns = [
    #path('upload/', views.model_form_upload, name='upload'),
    path('upload/', views.UploadView.as_view(), name='upload'),
    
]

