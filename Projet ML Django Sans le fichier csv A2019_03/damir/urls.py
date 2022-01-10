from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('damir', views.damir, name='damir'),
    path('beneficiaires', views.beneficiaires, name='beneficiaires'),


]