from django.db import models

user_status_choices = [('Active','Active'),('Inactive','Inactive')]

class M_Customer(models.Model):
    Customer_ID = models.AutoField(primary_key=True)
    Business_Name = models.CharField(max_length=100,blank=True,null=True)
    Business_Information = models.CharField(max_length=255,blank=True,null=True)
    Company_Registered_Number = models.CharField(max_length=100,blank=True,null=True)
    Tax_Number = models.CharField(max_length=100,blank=True,null=True)
    Company_Website = models.CharField(max_length=100,blank=True,null=True)
    Contact_Name = models.CharField(max_length=100,blank=True,null=True)
    Contact_Email_ID = models.CharField(max_length=100)
    Business_Phone_Number = models.CharField(max_length=20,null=True,blank=True)
    Business_Address_First_Line = models.CharField(max_length=255,blank=True,null=True)
    Business_Address_Second_Line = models.CharField(max_length=255,blank=True,null=True)
    # Plan_id = models.ForeignKey(T_Subscription_Plan, on_delete=models.CASCADE,null=True)
    Postal_code = models.CharField(max_length=255,blank=True,null=True)
    Expected_Users_Count = models.CharField(max_length=10,blank=True,null=True)
    city = models.CharField(max_length=120,null=True,blank=True)
    country = models.CharField(max_length=120,null=True,blank=True)
    longitude = models.FloatField(null=True,blank=True)
    lattitude = models.FloatField(null=True,blank=True)
    Customer_Type = models.CharField(max_length=255)
    Status = models.CharField(max_length=10, choices=user_status_choices, default='Active',blank=True,null=True)
    Created_Date = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    Created_By = models.CharField(max_length=100, blank=True,null=True)
    Modified_Date = models.DateTimeField(null=True, blank=True)
    Modified_By = models.CharField(max_length=100,null=True, blank=True)

    def __str__(self):
        return str(self.Business_Name)
