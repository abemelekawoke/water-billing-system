# reads/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WaterReadViewSet, get_schedule_status

router = DefaultRouter()
router.register(r'waterReads', WaterReadViewSet, basename='waterread')

urlpatterns = [
    path('', include(router.urls)),
    path('schedule-status/', get_schedule_status, name='get_schedule_status'),
]
