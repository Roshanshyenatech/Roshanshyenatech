"""
This file contains the Data Models for Role Tables
"""

from djongo import models
from app.models import *
user_status_choices = [('Active','Active'),('Inactive','Inactive')]


class M_Menu(models.Model):
    menu_id = models.AutoField(primary_key=True)
    menu_name = models.CharField(max_length=100)
    menu_desc = models.CharField(max_length=100)
    status = models.CharField(max_length=10, choices=user_status_choices, default='Active')
    is_feature = models.BooleanField(default=False)
    Created_Date = models.DateTimeField(auto_now_add=True)
    Created_By = models.CharField(max_length=100, blank=True)
    Modified_Date = models.DateTimeField(null=True, blank=True)
    Modified_By = models.CharField(max_length=100,null=True, blank=True)

    def __str__(self):
        return str(self.menu_name)
    
class M_Sub_Menu(models.Model):
    sub_menu_id = models.AutoField(primary_key=True)
    Sub_menu_name = models.CharField(max_length=100)
    Sub_menu_desc = models.CharField(max_length=100)
    menu_id = models.ForeignKey(M_Menu, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=user_status_choices, default='Active')
    is_feature = models.BooleanField(default=False)
    Created_Date = models.DateTimeField(auto_now_add=True)
    Created_By = models.CharField(max_length=100, blank=True)
    Modified_Date = models.DateTimeField(null=True, blank=True)
    Modified_By = models.CharField(max_length=100,null=True, blank=True)

    def __str__(self):
        return str(self.Sub_menu_name)


class M_Role(models.Model):
    Role_ID =  models.AutoField(primary_key=True)
    Role_Name = models.CharField(max_length=20, default='Guest')
    Is_active = models.CharField(max_length=10, choices=user_status_choices, default='Active')
    is_default = models.BooleanField(default=False)
    is_aiydec_role = models.BooleanField(default=False)
    payment_access = models.BooleanField(default=False)
    Created_Date = models.DateTimeField(auto_now_add=True)
    Created_By = models.CharField(max_length=100, blank=True)
    Modified_Date = models.DateTimeField(null=True, blank=True)
    Modified_By = models.CharField(max_length=100,null=True, blank=True)

    def __str__(self):
        return str(self.Role_Name)


class M_Role_Menu_Mapping(models.Model):
    Role_menu_id = models.AutoField(primary_key=True)
    Role_id = models.ForeignKey(M_Role, on_delete=models.CASCADE)
    Menu_id = models.ForeignKey(M_Menu, on_delete=models.CASCADE)
    Sub_menu_id = models.ForeignKey(M_Sub_Menu, on_delete=models.CASCADE)
    # # Customer_id = 
    Created_Date = models.DateTimeField(auto_now_add=True)
    Created_By = models.CharField(max_length=100, blank=True)
    Modified_Date = models.DateTimeField(null=True, blank=True)
    Modified_By = models.CharField(max_length=100,null=True, blank=True)
    def __str__(self):
        return str(self.Sub_menu_id)
