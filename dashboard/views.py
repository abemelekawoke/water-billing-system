from django.shortcuts import render
from datetime import datetime, timedelta
import random
from customers.models import Client
from bills.models import *
from django.db.models import Avg, Sum
from periods.models import Season
from django.db.models.functions import Cast
from django.db.models import FloatField

def dashboard_view(request):
    total = Client.objects.count()
    
    # Get the active season's month and year (assuming there's only one active row)
    try:
        current_season = Season.objects.first()  # Assumes there is only one active row
        current_month = current_season.MONTH_ENGLISH  # Assuming it's a string, like 'Jan', 'Feb'
        current_years = current_season.YEAR  # Assuming it's an integer or string like '2025'
    except Season.DoesNotExist:
        current_month = None
        current_years = None

    # Get total revenue for the current month and year
    if current_month and current_years:
        total_revenue = PaymentMethod.objects.filter(
            month=current_month, year=current_years
        ).exclude(payment_method='Not Sold').aggregate(total_revenue=Sum('total_price'))['total_revenue'] or 0
    else:
        total_revenue = 0  # If no active season is found, set revenue to 0

    # If we found the current month and year, proceed to calculate the average consumption
    if current_month and current_years:
        # Filter HandoverSummaryReport by current month and year
        reports = HandoverDetailReport.objects.filter(
            MONTH=current_month, YEAR=current_years
        )

        # If reports exist, calculate the average consumption
        if reports.exists():
            average_consumption = reports.aggregate(
                avg_consumption=Avg('CONSUMPTION')
            )['avg_consumption'] or 0
            # Round the average consumption to the nearest integer (no decimal places)
            average_consumption = round(average_consumption)
        else:
            average_consumption = 0  # If no records, set the average to 0
    else:
        average_consumption = 0  # If no active season found, set to 0
        
    # Query grouped by SERVICE and MONTH with total consumption per group
    month_year_combos = HandoverDetailReport.objects.values_list(
        'MONTH', 'YEAR'
    ).distinct().order_by('YEAR', 'MONTH')

    # Get all service types from the database
    service_types = HandoverDetailReport.objects.values_list(
        'SERVICE', flat=True
    ).distinct()

    # Create month labels (e.g., "Jan-2023")
    month_labels = [
        f"{datetime.strptime(month, '%m').strftime('%b')}-{year}" 
        for month, year in month_year_combos
    ]

    # Aggregate consumption data
    consumption_data = defaultdict(dict)
    
    queryset = HandoverDetailReport.objects.values(
        'MONTH', 'YEAR', 'SERVICE'
    ).annotate(
        total_consumption=Sum(Cast('CONSUMPTION', FloatField()))
    ).order_by('YEAR', 'MONTH', 'SERVICE')

    for entry in queryset:
        month_year = f"{datetime.strptime(entry['MONTH'], '%m').strftime('%b')}-{entry['YEAR']}"
        consumption_data[entry['SERVICE']][month_year] = entry['total_consumption']

    # Prepare dataset for Chart.js
    datasets = []
    colors = ['#3498db', '#2ecc71', '#e74c3c', '#f39c12', '#9b59b6']  # Add more colors if needed
    
    for i, (service_type, values) in enumerate(consumption_data.items()):
        # Fill in data for all months, defaulting to 0 where no data exists
        data = [values.get(month, 0) for month in month_labels]
        
        datasets.append({
            'label': service_type,
            'data': data,
            'backgroundColor': colors[i % len(colors)],
            'borderColor': colors[i % len(colors)],
            'borderWidth': 1
        })
        
    # Generate months for current and previous year
    current_year = datetime.now().year
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    # 1. Monthly Water Consumption by Zone/Type (Original)
    water_consumption = {
        'Residential': [round(random.uniform(1000, 1500)) for _ in range(12)],
        'Commercial': [round(random.uniform(700, 1000)) for _ in range(12)],
        'Industrial': [round(random.uniform(500, 800)) for _ in range(12)],
        'Zone A': [round(random.uniform(600, 900)) for _ in range(12)],
        'Zone B': [round(random.uniform(400, 700)) for _ in range(12)],
    }

    # 2. Sewerage Coverage by Zone (Original)
    sewerage_coverage = [
        {'zone': 'Zone A', 'percent': 75, 'target': 90},
        {'zone': 'Zone B', 'percent': 65, 'target': 85},
        {'zone': 'Zone C', 'percent': 55, 'target': 80},
        {'zone': 'Zone D', 'percent': 45, 'target': 75},
    ]

    # 3. Revenue Collection (Original)
    revenue = {
        'Water': [round(random.uniform(4000, 7000)) for _ in range(12)],
        'Sewerage': [round(random.uniform(1500, 3000)) for _ in range(12)],
        'Penalties': [round(random.uniform(500, 1500)) for _ in range(12)],
    }

    # 4. Payment Status (Original)
    payment_status = {
        'Paid': 350,
        'Unpaid': 100,
        'Partially Paid': 50,
        'Overdue': 75,
    }

    # 5. Customer Count by Zone (Original)
    customer_counts = {
        'Zone A': 300,
        'Zone B': 250,
        'Zone C': 150,
        'Zone D': 200,
    }

    # 6. Average Consumption per Household (Original)
    avg_consumption = {
        'Zone A': [round(random.uniform(10, 15), 1) for _ in range(12)],
        'Zone B': [round(random.uniform(8, 12), 1) for _ in range(12)],
        'Zone C': [round(random.uniform(7, 10), 1) for _ in range(12)],
    }

    # 7. Water Quality Metrics (New)
    water_quality = {
        'labels': ['Turbidity (NTU)', 'pH Level', 'Chlorine (mg/L)', 'Hardness (mg/L)'],
        'values': [2.1, 7.4, 0.8, 120],
        'standards': [5.0, 8.5, 4.0, 200],  # Max allowed values
    }

    # 8. Infrastructure Status (New)
    infrastructure = {
        'labels': ['Pipes', 'Valves', 'Meters', 'Pumps', 'Treatment Plants'],
        'condition': ['Good', 'Fair', 'Good', 'Poor', 'Excellent'],
        'age': [15, 20, 5, 25, 10],  # Years
        'replacement_cost': [2500000, 500000, 300000, 800000, 2000000],  # USD
    }

    # 9. Water Loss/Leakage (New)
    water_loss = {
        'months': months,
        'total_produced': [round(random.uniform(50000, 60000)) for _ in range(12)],
        'unaccounted_water': [round(random.uniform(5000, 10000)) for _ in range(12)],
        'leakage_percentage': [round(random.uniform(8, 15), 1) for _ in range(12)],
    }

    # 10. Complaint Statistics (New)
    complaints = {
        'types': ['Water Quality', 'Low Pressure', 'Billing', 'No Water', 'Leakage'],
        'counts': [45, 120, 85, 60, 90],
        'resolution_time': [2.5, 1.5, 7.0, 3.0, 4.5],  # Days
    }

    # 11. Water Source Utilization (New)
    water_sources = {
        'labels': ['Ground Water', 'Surface Water', 'Desalination', 'Recycled'],
        'current': [45, 35, 15, 5],  # Percentage
        'projected': [40, 30, 20, 10],  # Next 5 years
    }

    # 12. Emergency Response (New)
    emergencies = {
        'months': months,
        'pipe_bursts': [random.randint(2, 10) for _ in range(12)],
        'response_time': [round(random.uniform(2, 8), 1) for _ in range(12)],  # Hours
    }

    context = {
        'total_customers': total,
        'total_revenue': total_revenue,
        'average_consumption': average_consumption,
        'month_labels': month_labels,
        'consumption_datasets': datasets,
        'months': months,
        'current_year': current_year,
        'current_years': current_years,
        
        # Original data
        'water_consumption': water_consumption,
        'sewerage_coverage': sewerage_coverage,
        'revenue': revenue,
        'payment_status': payment_status,
        'customer_counts': customer_counts,
        'avg_consumption': avg_consumption,
        
        # New data
        'water_quality': water_quality,
        'infrastructure': infrastructure,
        'water_loss': water_loss,
        'complaints': complaints,
        'water_sources': water_sources,
        'emergencies': emergencies,
    }

    return render(request, 'dashboard/index.html', context)