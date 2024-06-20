from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Ticket, TicketPurchase
import datetime
from .form import CreateTicketForm, UpdateTicketForm
from django.shortcuts import get_object_or_404
from .form import TicketPurchaseForm


#Parte per i customer
def create_ticket(request):
    if request.method == 'POST':
        form = CreateTicketForm(request.POST)
        if form.is_valid():
            var = form.save(commit=False)
            var.created_by = request.user
            var.ticket_status = 'Pending'
            var.save()
            messages.info(request, 'Ticket created successfully')
            return redirect('dashboard')
        else:
            messages.warning(request, 'Something went wrong')
            return redirect('create-ticket')
    else:
        form = CreateTicketForm()
        context = {'form': form}
        return render(request, 'ticket/create_ticket.html', context)


def update_ticket(request, id):
    ticket = get_object_or_404(Ticket, pk=id)

    if request.method == 'POST':
        form = UpdateTicketForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            messages.info(request, 'Ticket information has been updated')
            return redirect('dashboard')
        else:
            messages.warning(request, 'Something went wrong. Please check the form.')
    else:
        form = UpdateTicketForm(instance=ticket)

    context = {'form': form, 'ticket': ticket}
    return render(request, 'ticket/update_ticket.html', context)


def all_tickets(request):
    tickets = Ticket.objects.filter(created_by=request.user)
    context = {'tickets': tickets}
    return render(request, 'ticket/all_tickets.html', context)


def all_available_tickets(request):
    accepted_tickets = Ticket.objects.filter(created_by=request.user, ticket_status='Accepted')
    context = {'tickets': accepted_tickets}
    return render(request, 'ticket/all_available_tickets.html', context)


#parte per gli admin
def ticket_queue(request):
    tickets = Ticket.objects.filter(ticket_status='Pending')
    context = {'tickets': tickets}
    return render(request, 'ticket/ticket_queue.html', context)


def accept_ticket(request, pk):
    ticket = Ticket.objects.get(pk=pk)
    ticket.ticket_status = 'Accepted'
    ticket.assigned_to = request.user
    ticket.accepted_date = datetime.datetime.now()
    ticket.save()
    messages.info(request, 'Ticket has been accepted')
    return redirect('ticket-queue')


def buy_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)

    if request.method == 'POST':
        form = TicketPurchaseForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            if quantity > ticket.quantity_available:
                form.add_error('quantity', f'Only {ticket.quantity_available} tickets available')
            else:
                ticket.quantity_available -= quantity
                ticket.is_purchased = True
                ticket.save()

                # Create a new TicketPurchase object
                purchase = TicketPurchase(user=request.user, ticket=ticket, quantity=quantity)
                purchase.save()

                return render(request, 'ticket/purchase_confirmation.html', {'ticket': ticket, 'quantity': quantity})
    else:
        form = TicketPurchaseForm(initial={'ticket_id': ticket_id})

    return render(request, 'ticket/buy_ticket.html', {'ticket': ticket, 'form': form})


def purchased_tickets(request):
    purchases = TicketPurchase.objects.filter(user=request.user, ticket__is_purchased=True)
    tickets_with_quantity = [(purchase.ticket, purchase.quantity) for purchase in purchases]
    context = {'tickets': tickets_with_quantity}
    return render(request, 'ticket/purchased_tickets.html', context)

