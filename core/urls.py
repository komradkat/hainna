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
from .views import DashboardView, LiveTrackingView, FleetVehiclesView, AddVehicleView, DriversView, AddDriverView, RoutesView, AddRouteView, AddZoneView, SchedulesView, AddScheduleView, ServiceLogsView, AddServiceLogView, FuelMonitoringView, AddFuelView, AnalyticsView, PersonnelView, AddPersonnelView, system_status
from users.views import UserManagementView, AddUserView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', DashboardView.as_view(), name='dashboard'),
    path('live-tracking/', LiveTrackingView.as_view(), name='live_tracking'),
    path('fleet/vehicles/', FleetVehiclesView.as_view(), name='fleet_vehicles'),
    path('fleet/vehicles/add/', AddVehicleView.as_view(), name='add_vehicle'),
    path('fleet/drivers/', DriversView.as_view(), name='drivers'),
    path('fleet/drivers/add/', AddDriverView.as_view(), name='add_driver'),
    path('fleet/routes/', RoutesView.as_view(), name='routes'),
    path('fleet/routes/add/', AddRouteView.as_view(), name='add_route'),
    path('fleet/zones/add/', AddZoneView.as_view(), name='add_zone'),
    path('schedules/', SchedulesView.as_view(), name='schedules'),
    path('schedules/add/', AddScheduleView.as_view(), name='add_schedule'),
    path('service-logs/', ServiceLogsView.as_view(), name='service_logs'),
    path('service-logs/add/', AddServiceLogView.as_view(), name='add_service_log'),
    path('fuel/', FuelMonitoringView.as_view(), name='fuel'),
    path('fuel/add/', AddFuelView.as_view(), name='add_fuel'),
    path('analytics/', AnalyticsView.as_view(), name='analytics'),
    path('personnel/', PersonnelView.as_view(), name='personnel'),
    path('personnel/add/', AddPersonnelView.as_view(), name='add_personnel'),
    path('users/', UserManagementView.as_view(), name='users'),
    path('users/add/', AddUserView.as_view(), name='add_user'),
    path('system-status/', system_status, name='system_status'),
]
