"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import DashboardView, LiveTrackingView, FleetVehiclesView, DriversView, RoutesView, SchedulesView, ServiceLogsView, FuelMonitoringView, AnalyticsView, PersonnelView, UserManagementView, system_status

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', DashboardView.as_view(), name='dashboard'),
    path('live-tracking/', LiveTrackingView.as_view(), name='live_tracking'),
    path('fleet-vehicles/', FleetVehiclesView.as_view(), name='fleet_vehicles'),
    path('drivers/', DriversView.as_view(), name='drivers'),
    path('routes/', RoutesView.as_view(), name='routes'),
    path('schedules/', SchedulesView.as_view(), name='schedules'),
    path('service-logs/', ServiceLogsView.as_view(), name='service_logs'),
    path('fuel/', FuelMonitoringView.as_view(), name='fuel'),
    path('analytics/', AnalyticsView.as_view(), name='analytics'),
    path('personnel/', PersonnelView.as_view(), name='personnel'),
    path('users/', UserManagementView.as_view(), name='users'),
    path('system-status/', system_status, name='system_status'),
]
