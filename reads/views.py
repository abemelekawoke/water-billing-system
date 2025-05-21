from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from reads.models import WaterRead
from reads.serializers import WaterReadSerializer
from setups.models import Reader
from rest_framework.exceptions import PermissionDenied

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Schedule
from periods.models import Season
from setups.models import *
from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
def get_schedule_status(request):
    try:
        # Fetch the most recent schedule or customize based on your needs
        schedule = Schedule.objects.latest('id')
        return Response({'status': schedule.status}, status=200)
    except Schedule.DoesNotExist:
        return Response({'error': 'No schedule found'}, status=404)


# class WaterReadViewSet(viewsets.ModelViewSet):
#     serializer_class = WaterReadSerializer
#     permission_classes = [AllowAny]  # Allow unauthenticated access

#     def get_queryset(self):
#         if self.request.user.is_authenticated:
#             try:
#                 # Get the reader associated with the logged-in user
#                 reader = Reader.objects.get(user=self.request.user)

#                 # Get the zones associated with the reader
#                 zones = Zone.objects.filter(reader=reader)

#                 # Filter WaterRead entries by the zones
#                 return WaterRead.objects.filter(zone__in=zones)
#             except Reader.DoesNotExist:
#                 return WaterRead.objects.none()  # Return an empty queryset if no reader is found
#         else:
#             # Optionally return all water reads or handle unauthenticated access
#             return WaterRead.objects.none()  # Return none for unauthenticated users

class WaterReadViewSet(viewsets.ModelViewSet):
    serializer_class = WaterReadSerializer
    permission_classes = [AllowAny]  # Allow unauthenticated access

    def get_queryset(self):
        # Initialize queryset
        queryset = WaterRead.objects.none()

        # Handle authenticated user case
        if self.request.user.is_authenticated:
            try:
                # Get the reader associated with the logged-in user
                reader = Reader.objects.get(user=self.request.user)

                # Get the zones associated with the reader
                zones = Zone.objects.filter(reader=reader)

                # Filter WaterRead entries by the zones
                queryset = WaterRead.objects.filter(zone__in=zones)
            except Reader.DoesNotExist:
                queryset = WaterRead.objects.none()  # Return empty if no reader found

        # Handle filtering by season (month and year)
        try:
            # Fetch the latest season
            current_season = Season.objects.latest('MONTH_ID')
        except Season.DoesNotExist:
            current_season = None

        # If a season is found, filter further by month and year
        if current_season:
            queryset = queryset.filter(month=current_season.MONTH_ENGLISH, year=current_season.YEAR)
        else:
            queryset = WaterRead.objects.none()  # No season found, return no records

        return queryset
