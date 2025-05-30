from rest_framework import generics, permissions
from .models import Employee
from .serializers import EmployeeSerializer
from .permissions import IsBusinessOwner

class CreateEmployeeView(generics.CreateAPIView):
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAuthenticated, IsBusinessOwner]

    def get_queryset(self):
        return Employee.objects.filter(business__owner=self.request.user)

    def perform_create(self, serializer):
        business = self.request.user.business
        serializer.save(business=business)
