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
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from .views import (
    DashboardView, LiveTrackingView, SchedulesView, AddScheduleView, 
    FuelMonitoringView, AddFuelView, AnalyticsView, PersonnelView, 
    AddPersonnelView, system_status, tracking_positions, LoginLoadingView,
    health_check
)
from users.views import UserManagementView, AddUserView, EditUserView, DeleteUserView, ChangePasswordView
from fleet.views import FleetVehiclesView, AddVehicleView, EditVehicleView, DeleteVehicleView, DriversView, AddDriverView, EditDriverView, DeleteDriverView, ServiceLogsView, AddServiceLogView, EditServiceLogView, DeleteServiceLogView, RoutesView, AddRouteView, EditRouteView, DeleteRouteView, AddZoneView, EditZoneView, DeleteZoneView, TerminalsView, AddTerminalView, EditTerminalView, DeleteTerminalView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='/login/'), name='logout'),
    path('', DashboardView.as_view(), name='dashboard'),
    path('loading/', LoginLoadingView.as_view(), name='loading_screen'),
    path('live-tracking/', LiveTrackingView.as_view(), name='live_tracking'),
    path('live-tracking/positions/', tracking_positions, name='tracking_positions'),
    path('fleet/vehicles/', FleetVehiclesView.as_view(), name='fleet_vehicles'),
    path('fleet/vehicles/add/', AddVehicleView.as_view(), name='add_vehicle'),
    path('fleet/vehicles/edit/<int:pk>/', EditVehicleView.as_view(), name='edit_vehicle'),
    path('fleet/vehicles/delete/<int:pk>/', DeleteVehicleView.as_view(), name='delete_vehicle'),
    path('fleet/drivers/', DriversView.as_view(), name='drivers'),
    path('fleet/drivers/add/', AddDriverView.as_view(), name='add_driver'),
    path('fleet/drivers/edit/<int:pk>/', EditDriverView.as_view(), name='edit_driver'),
    path('fleet/drivers/delete/<int:pk>/', DeleteDriverView.as_view(), name='delete_driver'),
    path('fleet/terminals/', TerminalsView.as_view(), name='terminals'),
    path('fleet/terminals/add/', AddTerminalView.as_view(), name='add_terminal'),
    path('fleet/terminals/edit/<int:pk>/', EditTerminalView.as_view(), name='edit_terminal'),
    path('fleet/terminals/delete/<int:pk>/', DeleteTerminalView.as_view(), name='delete_terminal'),
    path('fleet/routes/', RoutesView.as_view(), name='routes'),
    path('fleet/routes/add/', AddRouteView.as_view(), name='add_route'),
    path('fleet/routes/edit/<int:pk>/', EditRouteView.as_view(), name='edit_route'),
    path('fleet/routes/delete/<int:pk>/', DeleteRouteView.as_view(), name='delete_route'),
    path('fleet/zones/add/', AddZoneView.as_view(), name='add_zone'),
    path('fleet/zones/edit/<int:pk>/', EditZoneView.as_view(), name='edit_zone'),
    path('fleet/zones/delete/<int:pk>/', DeleteZoneView.as_view(), name='delete_zone'),
    path('schedules/', SchedulesView.as_view(), name='schedules'),
    path('schedules/add/', AddScheduleView.as_view(), name='add_schedule'),
    path('fleet/service-logs/', ServiceLogsView.as_view(), name='service_logs'),
    path('fleet/service-logs/add/', AddServiceLogView.as_view(), name='add_service_log'),
    path('fleet/service-logs/edit/<int:pk>/', EditServiceLogView.as_view(), name='edit_service_log'),
    path('fleet/service-logs/delete/<int:pk>/', DeleteServiceLogView.as_view(), name='delete_service_log'),
    path('fuel/', FuelMonitoringView.as_view(), name='fuel'),
    path('fuel/add/', AddFuelView.as_view(), name='add_fuel'),
    path('analytics/', AnalyticsView.as_view(), name='analytics'),
    path('personnel/', PersonnelView.as_view(), name='personnel'),
    path('personnel/add/', AddPersonnelView.as_view(), name='add_personnel'),
    path('users/', UserManagementView.as_view(), name='users'),
    path('users/add/', AddUserView.as_view(), name='add_user'),
    path('users/edit/<int:pk>/', EditUserView.as_view(), name='edit_user'),
    path('users/delete/<int:pk>/', DeleteUserView.as_view(), name='delete_user'),
    path('users/change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('system-status/', system_status, name='system_status'),
    path('health/', health_check, name='health_check'),
    path('booking/', include('booking.urls')),
]
