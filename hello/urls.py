from django.urls import path

from . import views

urlpatterns = [    
    path('', views.hello, name='hello'),
    path('submit/', views.hello_submit, name='submit'),
]
