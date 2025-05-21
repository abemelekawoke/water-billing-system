from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WaterBillViewSet  # Import the WaterBillViewSet
from . import views

router = DefaultRouter()
router.register(r'waterbills', WaterBillViewSet)  # Register the WaterBillViewSet

urlpatterns = [
    path('', include(router.urls)),  # Include the API URLs
    # path('print-combined-summary/', views.print_combined_balance_summary, name='print_combined_summary'),

]
