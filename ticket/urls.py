from django.urls import path
from . import views

urlpatterns = [
    path('create-ticket/', views.create_ticket, name='create-ticket'),
    path('update-ticket/<int:id>/', views.update_ticket, name='update-ticket'),
    path('all-tickets/', views.all_tickets, name='all-tickets'),
    path('ticket-queue/', views.ticket_queue, name='ticket-queue'),
    path('accept-ticket/<int:pk>/', views.accept_ticket, name='accept-ticket'),
    path('buy-ticket/<int:ticket_id>/', views.buy_ticket, name='buy-ticket'),
    path('all-available-tickets/', views.all_available_tickets, name='all-available-tickets'),
    path('purchased-tickets/', views.purchased_tickets, name='purchased-tickets')
]
