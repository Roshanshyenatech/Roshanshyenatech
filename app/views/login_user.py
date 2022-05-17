"""
This file contains login and homepage API 
"""
import jwt
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from app.models.user import M_User
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
from app.encode import encode_auth_token
from app.decode import decode_auth_token
from django.shortcuts import render,HttpResponseRedirect
from rest_framework_simplejwt.views import TokenObtainPairView


@csrf_exempt
@api_view(['POST'])
def login_request(request):
    """
    Login API Endpoint
    input parameters: email(string),password(string)
    """
    if request.method=="POST":
        try:
            # fetch email and password from form
            email = request.data.get("email", None)
            if not M_User.objects.filter(username=email).exists():
                return Response({"message":"User not found"},status=status.HTTP_404_NOT_FOUND)
            password = request.data.get("password", None)
            try:
                # fetching for existance of user with input email
                user_obj = M_User.objects.get(username=email)
                # check for organisation status
                if user_obj.Status == 'Inactive':
                    return Response({"message":"Organisation is Deactivated/Blocked."},status=status.HTTP_403_FORBIDDEN)
                

                # check that user is Active or Inactive 
                if user_obj.Status == 'Inactive':
                    return Response({"message":"User is Deactivated/Blocked."},status=status.HTTP_403_FORBIDDEN)
                username = user_obj.username
                
            except Exception as e:
                # incase of user with such email doesn't exist
                print(e)
                return Response({"message":"Invalid Login Credentials."}, status=status.HTTP_401_UNAUTHORIZED)
            # Authenticate with username and password
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request, user)
                payload = {'username':user.username}
                if user.first_login =='Yes':
                    first_login = True
                    # Force redirect to Reset Password if user login for first time and Create password_authentication token
                    return Response('login successfully')
                else:
                    first_login = False
                        #If user is login second time or later creae a Login_authentication token
                    auth_token = encode_auth_token(payload)
                    return Response(auth_token)
                




                # Fetch the Menu and submenu assign to the user according to his Role

                # rolequery = M_Role_Menu_Mapping.objects.filter(Role_id=user.Role_ID)
                # menus=[]
                # submenus=[]
                # for query in rolequery:
                #     menus.append(str(query.Menu_id))
                #     submenus.append(str(query.Sub_menu_id))
                # menus = list(set(menus))
            #     try:
            #         active_plans = T_Cust_Subs_History.objects.filter(customer_id=user.Customer_ID,plan_id=user.Customer_ID.Plan_id,plan_status='Active')
            #         if len(active_plans)>1:
            #             return Response({"message":"You have more than one Active plan."},status=status.HTTP_400_BAD_REQUEST)
            #         payment_history_obj = T_Cust_Subs_History.objects.filter(customer_id=user.Customer_ID,plan_id=user.Customer_ID.Plan_id).order_by('-created_date')[0]
                    
            #         if (payment_history_obj.plan_status == 'Active' or 'Cancelled'):
            #             payment_status=True
            #         elif T_Invoice.objects.filter(customer_id=user.Customer_ID,payment_status='paid'):
            #             payment_status = True
            #         else:
            #             payment_status = False
            #             # check for payment access 
                        
                        

            #         if payment_history_obj.plan_expiry_date < timezone.now():
            #             payment_history_obj.plan_status = 'Expired'
            #             payment_history_obj.save()
            #     except Exception as e:
            #         print('Exception in getting payment status',e)
            #         payment_status = False
            #     if user.Customer_ID.Plan_id.unit_price:
            #         guest_user=False
            #     else:
            #         guest_user=True
            #     data = {
            #             "message":"user login Successfully.", 
            #             "token": auth_token.decode(),
            #             "first_login":first_login,
            #             "email":user.email,
            #             "companyName":user.Customer_ID.Business_Name,
            #             "companyId":user.Customer_ID.Customer_ID,
            #             "first_name":user.first_name,
            #             "last_name":user.last_name,
            #             "role":user.Role_ID.Role_Name,
            #             "payment_access":user.Role_ID.payment_access,
            #             "plan_id":user.Customer_ID.Plan_id.plan_id,
            #             "payment_status":payment_status,
            #             "is_aiydec_role":user.Role_ID.is_aiydec_role,
            #             "guest_user":guest_user,
            #             "Menus":menus,
            #             "Submenus":submenus,
            #             }
            #     return Response(data, status=status.HTTP_200_OK)
            # else:
            #     # if login information are invalid 
            #     return Response({"message":"Invalid Login Credentials."}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            print('Error: ',e)
            return Response({"message":"Something went wrong Please Try again Later."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



#################################################

# home page of the server
def home(request):
    return HttpResponse('<h1>Welcome to Zinia Backend Dev instance auto build is running</h1>15 MAY 1:49 PM')
