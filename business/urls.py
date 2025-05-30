from django.urls import path
from .views import CreateBusinessView

urlpatterns = [
    path('register/', CreateBusinessView.as_view(), name='register_business'),
]