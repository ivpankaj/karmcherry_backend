from django.db import models
from users.models import User
from business.models import Business

class Employee(models.Model):
    EMPLOYEE_TYPES = (
        ('admin', 'Admin'),
        ('staff', 'Staff'),   
        ('viewer', 'Viewer'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee_profile')
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='employees')
    employee_type = models.CharField(max_length=10, choices=EMPLOYEE_TYPES)
    is_employee = models.BooleanField(default=True)
    def __str__(self):
        return self.user.email
