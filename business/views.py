from rest_framework import generics, permissions
from .models import Business
from .serializers import BusinessSerializer

class CreateBusinessView(generics.CreateAPIView):
    serializer_class = BusinessSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)