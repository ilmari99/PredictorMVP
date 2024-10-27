from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    #path('place_prediction/', views.place_prediction, name='place_prediction'),
    path('add_target/', views.add_target, name='add_target'),
    path('target/<int:target_id>/', views.target_view, name='target_view'),
]
