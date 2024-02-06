"""View module for handling requests for employee data"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from repairsapi.models import Employee


class EmployeeView(ViewSet):
    """Honey Rae API employee view"""

    def list(self, request):
        """Handle GET requests to get all employees

        Returns:
            Response -- JSON serialized list of employees
        """

        employees = Employee.objects.all()
        serialized = EmployeeSerializer(employees, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single employee

        Returns:
            Response -- JSON serialized employee record
        """

        employee = Employee.objects.get(pk=pk)
        serialized = EmployeeSerializer(employee)
        return Response(serialized.data, status=status.HTTP_200_OK)


class EmployeeSerializer(serializers.ModelSerializer):
    """JSON serializer for employees"""
    class Meta:
        model = Employee
        fields = ('id', 'specialty', 'full_name')