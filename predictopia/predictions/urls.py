from django.urls import path
from . import views

urlpatterns = [
    path('', views.prediction_list, name='prediction_list'),
    path('place_prediction/', views.place_prediction, name='place_prediction'),
]
