"""View module for handling requests for ticket data"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from repairsapi.models import Ticket, Employee, Customer


class TicketView(ViewSet):
    """Honey Rae API tickets view"""

    def list(self, request):
        """Handle GET requests to get all tickets

        Returns:
            Response -- JSON serialized list of tickets
        """
        service_tickets = []

        if request.auth.user.is_staff:
            service_tickets = Ticket.objects.all()

            if "status" in request.query_params:
                if request.query_params['status'] == "done":
                    service_tickets = service_tickets.filter(date_completed__isnull=False)
                if request.query_params['status'] == "unclaimed":
                    service_tickets = service_tickets.filter(date_completed__isnull=True, employee__isnull=True)
                if request.query_params['status'] == "in-progress":
                    service_tickets = service_tickets.filter(date_completed__isnull=True, employee__isnull=False)

            # Filter by priority if provided
            if "priority" in request.query_params:
                service_tickets = service_tickets.filter(priority=request.query_params['priority'])
        else:
            service_tickets = Ticket.objects.filter(customer__user=request.auth.user)

        serialized = TicketSerializer(service_tickets, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single ticket

        Returns:
            Response -- JSON serialized ticket record
        """
        try:
            ticket = Ticket.objects.get(pk=pk)
            serialized = TicketSerializer(ticket)
            return Response(serialized.data, status=status.HTTP_200_OK)
        except Ticket.DoesNotExist:
            return Response({'message': 'Ticket not found'}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a ticket"""
        try:
            service_ticket = Ticket.objects.get(pk=pk)
            service_ticket.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Ticket.DoesNotExist:
            return Response({'message': 'Ticket not found'}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        """Handle POST requests for service tickets

        Returns:
            Response: JSON serialized representation of newly created service ticket
        """
        # Validate required fields
        description = request.data.get('description', '').strip()
        if not description:
            return Response(
                {'message': 'Description is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        new_ticket = Ticket()
        new_ticket.customer = Customer.objects.get(user=request.auth.user)
        new_ticket.description = description
        new_ticket.emergency = request.data.get('emergency', False)
        new_ticket.priority = request.data.get('priority', 'medium')
        new_ticket.save()

        serialized = TicketSerializer(new_ticket)
        return Response(serialized.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        """Handle PUT request for updating a ticket"""
        try:
            ticket = Ticket.objects.get(pk=pk)
        except Ticket.DoesNotExist:
            return Response({'message': 'Ticket not found'}, status=status.HTTP_404_NOT_FOUND)

        # Handle employee assignment
        employee = request.data.get('employee')
        if employee == 0 or employee is None:
            ticket.employee = None
        else:
            try:
                assigned_employee = Employee.objects.get(pk=employee)
                ticket.employee = assigned_employee
            except Employee.DoesNotExist:
                return Response({'message': 'Employee not found'}, status=status.HTTP_400_BAD_REQUEST)

        # Update other fields if provided
        if 'date_completed' in request.data:
            ticket.date_completed = request.data['date_completed']

        if 'priority' in request.data:
            ticket.priority = request.data['priority']

        if 'description' in request.data:
            ticket.description = request.data['description']

        if 'emergency' in request.data:
            ticket.emergency = request.data['emergency']

        ticket.save()
        serialized = TicketSerializer(ticket)
        return Response(serialized.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get ticket statistics for dashboard"""
        if request.auth.user.is_staff:
            all_tickets = Ticket.objects.all()
        else:
            all_tickets = Ticket.objects.filter(customer__user=request.auth.user)

        stats = {
            'total': all_tickets.count(),
            'open': all_tickets.filter(date_completed__isnull=True, employee__isnull=True).count(),
            'in_progress': all_tickets.filter(date_completed__isnull=True, employee__isnull=False).count(),
            'completed': all_tickets.filter(date_completed__isnull=False).count(),
            'urgent': all_tickets.filter(priority='urgent', date_completed__isnull=True).count(),
            'high_priority': all_tickets.filter(priority='high', date_completed__isnull=True).count(),
            'emergency': all_tickets.filter(emergency=True, date_completed__isnull=True).count(),
        }
        return Response(stats, status=status.HTTP_200_OK)


class TicketEmployeeSerializer(serializers.ModelSerializer):
    """JSON serializer for employee"""
    class Meta:
        model = Employee
        fields = ('id', 'specialty', 'full_name')


class TicketCustomerSerializer(serializers.ModelSerializer):
    """JSON serializer for customer"""
    class Meta:
        model = Customer
        fields = ('id', 'user', 'address', 'full_name')


class TicketSerializer(serializers.ModelSerializer):
    """JSON serializer for tickets"""
    employee = TicketEmployeeSerializer(many=False)
    customer = TicketCustomerSerializer(many=False)
    status = serializers.ReadOnlyField()

    class Meta:
        model = Ticket
        fields = ('id', 'description', 'emergency', 'priority', 'status',
                  'date_created', 'date_completed', 'employee', 'customer')
        depth = 2
