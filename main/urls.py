from django.urls import path

from . import views

urlpatterns = [
    path('', views.Index, name='home'),
    path('airlines/', views.Airlines, name='airlines'),
    path('airline-add/', views.AirlineAdd, name='airline-add'),
    path('airlines-edit/<int:id>/', views.AirlineEdit, name='airline-edit'),
    path('airlines-delete/<int:id>/', views.AirlineDelete, name='airline-delete'),
]
