from .models import Event
from .serializers import EventSerializer, ReservationSerializer, PaymentSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.shortcuts import render, redirect
from .form import RegisterCustomerForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


def register_customer(request):
    if request.method == 'POST':
        form = RegisterCustomerForm(request.POST)
        if form.is_valid():
            var = form.save(commit=False)
            var.is_costumer = True
            var.save()
            messages.info(request, 'Account created successfully. Please Login')
            return redirect('login')
        else:
            messages.warning(request, 'Something went wrong. Please try again')
            return redirect('register-customer')
    else:
        form = RegisterCustomerForm()
        context = {'form': form}
        return render(request, 'ticket/register_customer.html', context)


@api_view(['GET', 'POST'])
def event_list(request):
    if request.method == 'GET':
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT'])
def event_detail(request, id):
    try:
        event = Event.objects.get(pk=id)
    except Event.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = EventSerializer(event)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = EventSerializer(event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def reservation_create(request):
    serializer = ReservationSerializer(data=request.data)
    if serializer.is_valid():
        with transaction.atomic():
            event = serializer.validated_data['event']
            tickets_reserved = serializer.validated_data['number_of_tickets']
            if event.available_tickets >= tickets_reserved:
                event.available_tickets -= tickets_reserved
                event.save()
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'Not enough tickets available'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def payment_create(request):
    serializer = PaymentSerializer(data=request.data)
    if serializer.is_valid():
        reservation = serializer.validated_data['reservation']
        reservation.paid = True
        reservation.save()
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
