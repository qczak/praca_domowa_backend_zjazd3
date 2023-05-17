from django.urls import path

from . import views

urlpatterns = [
    path('', views.measurement_list, name='measurement_list'),
    path('measurements_all', views.measurements_all, name='measurements_all'),
    path('measurement_detail/<int:id>', views.measurement_detail, name='measurement_detail'),
    path('chart/', views.chart, name='chart'),
    path('chart_avr/', views.chart_avr, name='chart_avr'),
    path('<int:id>/delete', views.delete, name='delete'),
]