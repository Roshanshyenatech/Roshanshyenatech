from django.db import models
from django.contrib.auth.models import AbstractUser
from app.models.roles import M_Role
from app.models.customer import M_Customer

user_status_choices = [('Active','Active'),('Inactive','Inactive')]
class M_User(AbstractUser):
    email = models.EmailField(unique=True)
    User_ID = models.AutoField(primary_key=True)
    Customer_ID = models.ForeignKey(M_Customer, on_delete=models.CASCADE)
    Role_ID = models.ForeignKey(M_Role, on_delete=models.CASCADE)
    first_login = models.CharField(max_length=10, default='Yes')
    Recovery_Email_Address = models.CharField(max_length=100, blank=True)
    phone = models.CharField(blank=True,null=True,max_length=20)
    ftp_activated = models.BooleanField(default=False)
    Status = models.CharField(max_length=10, choices=user_status_choices, default='Active')
    Created_Date = models.DateTimeField(auto_now_add=True)
    Created_By = models.CharField(max_length=100, blank=True)
    Modified_Date = models.DateTimeField(null=True, blank=True)
    Modified_By = models.CharField(max_length=100, blank=True)
    End_Date = models.DateTimeField(null=True, blank=True)
    