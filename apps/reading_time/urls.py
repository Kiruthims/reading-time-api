
from django.urls import path
from . import views

urlpatterns = [
    # Health check -for api test 
    path('health/', views.api_health_check, name='api_health_check'),
    
    # Main endpoint
    path('', views.calculate_reading_time_api, name='calculate_reading_time'),
    
    # Bulk processing
    path('bulk/', views.bulk_calculate_reading_time, name='bulk_calculate'),
]