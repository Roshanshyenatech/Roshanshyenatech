"""
File for containing Password related APIs
"""
from django.contrib.auth import login, logout, authenticate
from app.encode import encode_auth_token
from app.decode import decode_auth_token
from django.core.exceptions import ValidationError
from app.models.user import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from app.models.customer import *
from app.models.roles import *
import os
import jwt
from .imports import *



# Forget password Request
@csrf_exempt
@api_view(['POST'])
def reseting_password_request(request):
    if request.method=="POST":
        # fetch email from form
        email_id = request.data.get('email')
        try:
            # fetch user with given email
            user = M_User.objects.get(username=email_id)
            payload = {'username':user.username}
            # create jwt token
            auth_token = encode_auth_token(payload)
            link = "http://127.0.0.1:8000/"+'setpassword/'+'\n'+'token='+str(auth_token)
            #  Send mail to input email-id 
            sendEmail = send_mail(
                'link for change password and token',
                link,
                'roshanfuse1998@gmail.com',
                ['roshanfuse98@gmail.com'],
                fail_silently=False,
                )
            if sendEmail:
                # if email send successfully
                return Response({"message":"Email sent successfully"},status=status.HTTP_200_OK)
            else:
                # if email sending fails
                return Response({"message":"Email could not sent.Please Try again Later."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            print(e)
            print('no such user found')
            return Response({"message":"User not found"},status=status.HTTP_404_NOT_FOUND)




# Reseting Password
@csrf_exempt
@api_view(['POST'])
def reseting_password_done(request):
    """
    This function is used to reset password in two case
    1. when user will login first time
    2. when user will reset password by forget password link
    """
    if request.method=="POST":
        try:
            # fetching password from request
            password = request.data.get('password','')
           
            # fetching password authentication token from header
            get_token = request.META['HTTP_AUTHORIZATION']
            token = get_token[6:].strip()
            
            # decode the token 
            resp = decode_auth_token(token)
           
            if "code" in resp.keys() and resp["code"] == 401:
                data = {"code": 401, "message": "Token expired. Please log in again."}
                dump = json.dumps(data)
                return Response(data, content_type="application/json",status=status.HTTP_401_UNAUTHORIZED)
            
            elif "code" in resp.keys() and resp["code"] == 403:
                data = {"code": 401, "message": "Invalid token. Please log in again."}
                dump = json.dumps(data)
                return Response(data, content_type="application/json",status=status.HTTP_401_UNAUTHORIZED)

            else:
                # if token is valid 
                request.username = resp["username"]
                
                if password:
                    # if new password is non-empty string fetch user
                    user = M_User.objects.get(username = resp["username"])
                    same_password = user.check_password(password)
                    if same_password:
                        return Response({"message":"Password could not be same as old Password."}, status=status.HTTP_400_BAD_REQUEST)
                    user.set_password(password)
                    user.first_login = 'No'
                    user.save()
                    login(request,user)
                    payload = {"username":user.username}
                    auth_token = encode_auth_token(payload)  # create a token
                    #  success mail
                    send_mail(
                    'change password',
                    'Password Changed Successfully'+'\n'+'token='+auth_token,
                    'roshanfuse1998@gmail.com',
                    ['roshanfuse98@gmail.com'],
                    fail_silently=False,
                    )
                    return Response({"message":"Password Changed Successfully.Redirecting to Dashboard.", "token": str(auth_token),"first_login":False}, status=status.HTTP_200_OK)
            

        except ValidationError:
            data = {
                    'status': 'Failed',
                    'message': "Permission Denied",
                    "code": 401,
                    "error": "Invalid Authorization details"
                }
            
            return Response(data, content_type="application/json",status=status.HTTP_401_UNAUTHORIZED)

        except KeyError:
            data = {
                    'status': 'Failed',
                    'message': "Unauthorized",
                    "code": 403,
                    "error": "Authorization Credentials were not provided"
                }
            
            return Response(data, content_type="application/json",status=status.HTTP_401_UNAUTHORIZED)
        return Response({"message":"Something went wrong.Please try again Later."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# change password from profile section 
@csrf_exempt
@api_view(['POST'])
def change_password(request):
    if request.method=="POST":
        # fetch old and new password from request
        old_password = request.data.get('old_password','')
        new_password = request.data.get('new_password','')
      
        # fetch token 
        get_token = request.META['HTTP_AUTHORIZATION']
        token = get_token[6:].strip()
        try:
            # decode token 
            resp = decode_auth_token(token)
            if "code" in resp.keys() and resp["code"] == 401:
                data = {"code": 401, "message": "Token expired. Please log in again."}
                return Response(data, content_type="application/json",status=status.HTTP_401_UNAUTHORIZED)
            elif "code" in resp.keys() and resp["code"] == 403:
                data = {"code": 401, "message": "Invalid token. Please log in again."}
                return Response(data, content_type="application/json",status=status.HTTP_401_UNAUTHORIZED)
            else:
                # if token is valid
                if old_password and new_password:
                    try:
                        # fetch user
                        user = M_User.objects.get(username=resp['username'])
                        
                        #  verify old password
                        password_verification = user.check_password(old_password)
                        if password_verification: 
                            # if old password match set new password
                            user.set_password(new_password)
                            user.save()
                            login(request,user)
                            # create a token
                            payload = {"username":user.username}
                          
                            # create token
                            auth_token = encode_auth_token(payload)
                            #  success mail
                            send_mail(
                            'change password',
                            'Password Changed Successfully'+'\n'+'token='+auth_token,
                            'roshanfuse1998@gmail.com',
                            ['roshanfuse98@gmail.com'],
                            fail_silently=False,
                            )
                            return Response({"message":"Password Changed Successfully.","token": str(auth_token)}, status=status.HTTP_200_OK)

                        else:
                            #! old password mismatch
                            return Response({"message":"You have enter a wrong Password."}, content_type="application/json",status=status.HTTP_403_FORBIDDEN)
                    except Exception as e:
                        print(e)
                        return Response({"message":"Something went wrong.Please try again Later."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                else:
                    return Response({"message":"Please send all required Inputs."}, status=status.HTTP_404_NOT_FOUND)

        except ValidationError:
            data = {
                    'status': 'Failed',
                    'message': "Permission Denied",
                    "code": 401,
                    "error": "Invalid Authorization details"
                }
            
            # dump = json.dumps(data)
            return Response(data, content_type="application/json",status=status.HTTP_401_UNAUTHORIZED)

        except KeyError:
            data = {
                    'status': 'Failed',
                    'message': "Unauthorized",
                    "code": 401,
                    "error": "Authorization Credentials were not provided"
                }
            
            # dump = json.dumps(data)
            return Response(data, content_type="application/json",status=status.HTTP_401_UNAUTHORIZED)

