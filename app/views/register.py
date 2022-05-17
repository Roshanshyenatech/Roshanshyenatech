# from .imports import *
# from .S3_code import *
# from api_app.views.helping_function import *
# from auth_app.local import save_file_to_db

from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
import uuid
from app.models.customer import *
from app.models.roles import *
from app.models.user import *
import base64
from django.core.mail import send_mail

@csrf_exempt
@api_view(['POST'])
def register_customer(request):
    """
    This function is for onboarding of a new customer 
    """
    if request.method =="POST":
        try:
            #  fetch all detail 
            first_name = request.data.get("first_name", None)
            last_name = request.data.get("last_name", None)
            email_id = request.data.get("email", None)
            companyName = request.data.get("companyName", None)
            companyAdress = request.data.get("companyAdress", None)
            zipCode = request.data.get("zipCode", None)
            phoneNo = request.data.get("phoneNo", None)
            role_assigned = request.data.get("role", None)
            plan_id = request.data.get("plan_id",None)
            city = request.data.get("city",None)
            country = request.data.get("country",None)
            lattitude = request.data.get("lattitude",None)
            longitude = request.data.get("longitude",None)
            if not plan_id:
                return Response({"message":"Please select a valid plan."}, status=status.HTTP_403_FORBIDDEN) 

            #! check for email cumpolsary
            if not email_id:
                return Response({"message":"Email is not provided"},status=status.HTTP_403_FORBIDDEN)

            #!  check for duplicate email id
            if M_User.objects.filter(email__iexact=email_id).exists():
                return Response({"message":"Email id already Registered."}, status=status.HTTP_403_FORBIDDEN)
            #! check for duplicate organisation name
            if M_Customer.objects.filter(Business_Name__iexact=companyName).exists():
                return Response({"message":"Company Name already Registered."}, status=status.HTTP_403_FORBIDDEN)

            # Create customer
            try:
                org = M_Customer.objects.create(
                    Business_Name=companyName,
                    Contact_Name=first_name+' '+ last_name,
                    Business_Address_First_Line=companyAdress,
                    Business_Phone_Number=phoneNo,
                    Contact_Email_ID=email_id,
                    Postal_code=zipCode,
                    # Plan_id=T_Subscription_Plan.objects.get(plan_id=plan_id),
                    country=country,
                    city=city,
                    lattitude=lattitude,
                    longitude=longitude,
                    )
              
                # # todo create config table for customer
                # config_customer = create_config(org.Customer_ID)
                # if not config_customer:
                #     org.delete()
                #     return Response({"message":"User could not be configured."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except Exception as e:
                try:
                    org.delete()
                except:
                    pass
                print('Error in customer creation:',e)
                return Response({"message":"Something went wrong Please Try again Later."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            #? Create user
            try:
                user = M_User.objects.create(username=email_id,email=email_id,first_name=first_name,last_name=last_name,phone=phoneNo,Customer_ID=org,Role_ID=M_Role.objects.create(Role_Name=role_assigned))
                password = uuid.uuid4() #create seed password
                user.set_password(str(password))
                user.save()
                #  to send password and id on gmail
                send_mail(
                'testing mail',
                'username='+str(email_id)+'\n'+'password='+str(password),
                'roshanfuse1998@gmail.com',
                ['roshanfuse98@gmail.com'],
                fail_silently=False,
                )
                return Response({"message":"User  created."})
            except Exception as e:
                print('Exception in user creation',e)
                org.delete()
                return Response({"message":"User could not be created."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        #     #?  create s3 configuration for onboarding customer
        #     try:
        #         s3setup = addOrganization(str(org.Customer_ID),str(user.User_ID))
        #         print(s3setup)
        #         if not s3setup['status']:
        #             # if s3 setup return fails delete the user and organisation created
        #             user.delete()
        #             org.delete()
        #             return Response({"message":"Customer environment could not be created."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        #     except Exception as e:
        #         print('Error:',e)
        #         try:
        #             user.delete()
        #             org.delete()
        #         except:
        #             pass
        #         return Response({"message":"Customer environment could not be created."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        #     TRIAL_PERIOD_IN_DAYS = None
        #     if org.Plan_id.unit_price==0:
        #         try:
        #             d=datetime.now()
        #             TRIAL_PERIOD_IN_DAYS = M_List_of_Values.objects.get(lov_name='TRIAL_PERIOD_IN_DAYS').lov_value
        #             T_Cust_Subs_History.objects.create(
        #                 customer_id = org ,
        #                 plan_id = org.Plan_id,
        #                 plan_start_date = datetime.now(),
        #                 plan_expiry_date = datetime(d.year, d.month, d.day, d.hour, d.minute, d.second, d.microsecond, d.tzinfo) + timedelta(days=int(TRIAL_PERIOD_IN_DAYS)),
        #                 subs_amount = 0,
        #                 # todo fetch from table
        #                 user_count=1,
        #                 transaction_count=1000,
        #                 currency = 'GBP',
        #                 plan_status = "Active",
        #                 suspended_date = datetime(d.year, d.month, d.day, d.hour, d.minute, d.second, d.microsecond, d.tzinfo) + timedelta(days=int(TRIAL_PERIOD_IN_DAYS)),
        #                 created_by = "Aiydec Admin",
        #             )
        #         except Exception as e:
        #             print(e)
        #             org.delete()
        #             user.delete()
        #             return Response({"message":"Unable to apply Free plan. Please try again Later."}, status=status.HTTP_501_NOT_IMPLEMENTED)
        #     #  get domain name from lov table
        #     BACKEND_IP = os.getenv('BACKEND_IP')
        #     link = BACKEND_IP+'/signin'
        #     #?  Send email to input email with login credentials
        #     try:
        #         if TRIAL_PERIOD_IN_DAYS:
        #             sendEmail = login_detail_mail(email_id,link,email_id,password,first_name,trial_days = TRIAL_PERIOD_IN_DAYS)
        #         else:
        #             sendEmail = login_detail_mail(email_id,link,email_id,password,first_name,trial_days = None)
        #         if not sendEmail:
        #             # if email sending fails
        #             user.delete()
        #             org.delete()
        #             return Response({"message":"Email could not sent.Please try again Later."}, status=status.HTTP_501_NOT_IMPLEMENTED)
        #     except Exception as e:
        #         print('Exception in sending email',e)
        #         user.delete()
        #         org.delete()
        #         return Response({"message":"Email could not sent.Please try again Later."}, status=status.HTTP_501_NOT_IMPLEMENTED)
            
        #     return Response({"message":"Customer Created Successfully."}, status=status.HTTP_200_OK)
        except Exception as e:
            print('Exception: ',e)
            return Response({"message":"Something went wrong Please Try again Later."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    