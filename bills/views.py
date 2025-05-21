from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import *
from .serializers import WaterBillSerializer
from rest_framework.response import Response
from django.shortcuts import render
from django.http import HttpResponse
# class WaterBillViewSet(viewsets.ModelViewSet):
#     queryset = WaterBill.objects.all()
#     serializer_class = WaterBillSerializer
    
class WaterBillViewSet(viewsets.ModelViewSet):
    queryset = WaterBill.objects.all()
    serializer_class = WaterBillSerializer
    http_method_names = ['get', 'patch', 'put']

    def partial_update(self, request, *args, **kwargs):
        # Allow only 'status' to be updated
        data = request.data
        if 'status' in data:
            return super().partial_update(request, *args, **kwargs)
        else:
            return Response({'error': 'Only status can be updated'}, status=400)
        
# def print_combined_balance_summary(request):
#     # Get latest month and year data
#     latest = CombinedBalanceSummaryByService.objects.order_by('-year', '-month').first()
#     if not latest:
#         return HttpResponse("No data available.")

#     data = CombinedBalanceSummaryByService.objects.filter(month=latest.month, year=latest.year)

#     html_content = f"""
#     <!DOCTYPE html>
#     <html>
#     <head>
#         <title>Monthly Service Balance Summary - {latest.month}/{latest.year}</title>
#         <style>
#             body {{
#                 font-family: Arial, sans-serif;
#                 margin: 40px;
#             }}
#             h1 {{
#                 text-align: center;
#                 font-size: 26px;
#                 text-transform: uppercase;
#             }}
#             table {{
#                 width: 100%;
#                 border-collapse: collapse;
#                 margin-top: 20px;
#             }}
#             th, td {{
#                 border: 1px solid #ddd;
#                 padding: 10px;
#                 text-align: center;
#             }}
#             th {{
#                 background-color: #f2f2f2;
#                 font-size: 14px;
#             }}
#             td {{
#                 font-size: 13px;
#             }}
#         </style>
#     </head>
#     <body>
#         <h1>Service Balance Summary - {month_name(latest.month)} {latest.year}</h1>
#         <table>
#             <tr>
#                 <th>#</th>
#                 <th>Service Type</th>
#                 <th>Total Bill</th>
#                 <th>Sold Bill</th>
#                 <th>Unsold Bill</th>
#                 <th>Sold Transactions</th>
#                 <th>Unsold Customers</th>
#             </tr>"""

#     for idx, item in enumerate(data, start=1):
#         html_content += f"""
#             <tr>
#                 <td>{idx}</td>
#                 <td>{item.service_type.replace('_', ' ').title()}</td>
#                 <td>{item.total_bill:,.2f}</td>
#                 <td>{item.total_sold_bill:,.2f}</td>
#                 <td>{item.total_unsold_bill:,.2f}</td>
#                 <td>{item.sold_transaction_count}</td>
#                 <td>{item.unsold_customer_count}</td>
#             </tr>"""

#     html_content += """
#         </table>
#     </body>
#     </html>
#     """

#     return HttpResponse(html_content)


# def month_name(month_number):
#     import calendar
#     return calendar.month_name[month_number]
