"""
Middle ware file to check the token for every request for secure APIs
"""

from django.core.exceptions import ValidationError
from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from app.encode import encode_auth_token
from app.decode import decode_auth_token

import json 


class CheckTokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # one time configuration and initialization 


    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called 
        response = self.get_response(request)

        # code to be executed for each request/response after 
        # the view is called 
        return response

    # request from secure/ will accesss securly by using this middleware 
    #  by using token we can access data
    def process_view(self, request, *args, **kwargs):
        # print(("/app"+request.META['PATH_INFO'])[4:12])
        if "/secure/" in request.META['PATH_INFO'] or "/search/" in request.META['PATH_INFO']:
            try:
                print('checking token')
                get_token = request.META['HTTP_AUTHORIZATION']
                token = get_token[6:].strip()
                print(token,'okkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk')
                resp = decode_auth_token(token)
                print(resp,'respo')

                if "code" in resp.keys() and resp["code"] == 401:
                    data = {
                            "code": 401,
                            "message": "Token expired. Please log in again."
                            }
                    dump = json.dumps(data)

                    return HttpResponse(dump, content_type="application/json",status = 401)
                
                elif "code" in resp.keys() and resp["code"] == 403:
                    data = {
                            "code": 401,
                            "message": "Invalid token. Please log in again."
                            }
                    dump = json.dumps(data)

                    return HttpResponse(dump, content_type="application/json",status = 401)

                else:
                    request.api_user = resp["username"]
                    print(request.api_user)
                    return None
                

            except ValidationError:
                data = {
                        'status': 'Failed',
                        'message': "Permission Denied",
                        "code": 401,
                        "error": "Invalid Authorization details"
                    }
                
                dump = json.dumps(data)
                return HttpResponse(dump, content_type="application/json",status = 401)

            except KeyError:
                data = {
                        'status': 'Failed',
                        'message': "Unauthorized",
                        "code": 401,
                        "error": "Authorization Credentials were not provided"
                    }
                
                dump = json.dumps(data)
                return HttpResponse(dump, content_type="application/json",status = 401)

        else:
            return None



