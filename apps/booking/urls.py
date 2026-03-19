from django.urls import path
from . import views

app_name = 'booking'

urlpatterns = [
    path('pos/', views.BookingPOSView.as_view(), name='pos'),
    path('pos/trip/<int:trip_id>/', views.trip_details_htmx, name='trip_details'),
    path('pos/ticket/issue/', views.issue_ticket, name='issue_ticket'),
    
    path('dispatch/', views.DispatchBoardView.as_view(), name='dispatch'),
    path('dispatch/update/<int:trip_id>/', views.update_trip_status, name='update_trip_status'),
    path('board/', views.PublicBoardView.as_view(), name='public_board'),
    path('board/feed/', views.public_board_feed, name='public_board_feed'),
]
