from django.db import models



LOV_Type_choices = [("App", "App"), ("Cust", "Cust")]
Is_Active_choices = [("Y", "Y"), ("N", "N")]


class M_List_of_Values(models.Model):
    lov_id = models.AutoField(primary_key=True)
    lov_name = models.CharField(max_length=100)
    lov_value = models.CharField(max_length=100, null=True, blank=True)
    lov_description = models.CharField(max_length=100, null=False, blank=False)
    lov_type = models.CharField(max_length=10, choices=LOV_Type_choices, blank=True, null=True)
    lov_data_type = models.CharField(max_length=20, blank=True, null=True)
    is_active = models.CharField(max_length=1, choices=Is_Active_choices, default="Y")
    is_editable = models.CharField(max_length=1, choices=Is_Active_choices, default="Y")
    Created_Date = models.DateTimeField(auto_now_add=True)
    Created_By = models.CharField(max_length=100, blank=True)
    Modified_Date = models.DateTimeField(null=True, blank=True)
    Modified_By = models.CharField(max_length=100,null=True, blank=True)
