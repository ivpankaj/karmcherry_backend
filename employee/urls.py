from django.urls import path
from .views import CreateEmployeeView

urlpatterns = [
    path('create/', CreateEmployeeView.as_view(), name='create_employee'),
]