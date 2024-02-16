"""View module for handling requests for employee data"""
from django.http import HttpResponseServerError
from django.contrib.auth.models import User
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

    def create(self, request):
        """Handle POST requests for Employee

        Returns:
            Response: JSON serialized representation of newly created Employee
        """

        print(request.data)
        # user = User.objects.create_user(
        #     username=Faker().user_name(),
        #     email=Faker().email(),
        #     password=Faker().password(),
        #     first_name=request.data['firstName'],
        #     last_name=request.data['lastName'],
        # )
        # new_employee = Employee.objects.create(
        #     user=user,
        #     specialty=""
        # )
        # new_employee.save()
        # serialized = EmployeeSerializer(new_employee)

        # return Response(serialized.data, status=status.HTTP_201_CREATED)
        return Response(True, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        """Handle put request for single employee"""
        print(request.data)
        ticket = Employee.objects.get(pk=pk)
        employee = request.data['id']
        specialty = request.data['specialty']

        print('employee update')
        print(employee)
        print(specialty)

        if employee == 0:
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        
        assigned_employee = Employee.objects.get(pk=employee)
        print(assigned_employee)
        
        assigned_employee.specialty = specialty
        
        assigned_employee.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        employee = Employee.objects.get(pk=pk)
        employee.delete()
        
        return Response(None, status=status.HTTP_204_NO_CONTENT)




class EmployeeSerializer(serializers.ModelSerializer):
    """JSON serializer for employees"""
    class Meta:
        model = Employee
        fields = ('id', 'specialty', 'full_name')