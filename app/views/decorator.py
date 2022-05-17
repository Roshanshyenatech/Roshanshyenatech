
from .imports import *

# this is decorator for login  
#  using this decorator we can login secure or we can securely access the data    
def permission_check(submenu):

    def _method_wrapper(view_method):
        
        def _arguments_wrapper(request, *args, **kwargs) :
            """
            Wrapper with arguments to invoke the method
            """
            if "/secure/" in request.META['PATH_INFO'] or "/search/" in request.META['PATH_INFO']:
                try:
                    print('checking token')
                    get_token = request.META['HTTP_AUTHORIZATION']
                    token = get_token[6:].strip()
                    resp = decode_auth_token(token)
                    # resp = decode_password_token(token)/
                    print(resp,'jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj')

                    if "code" in resp.keys() and resp["code"] == 401:
                        data = {
                                "code": 401,
                                "message": "Token expired. Please log in again."
                                }
                        dump = json.dumps(data)

                        return HttpResponse(dump, content_type="application/json",status = 401)
                    
                    elif "code" in resp.keys() and resp["code"] == 403:
                        data = {
                                "code": 403,
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
        return _arguments_wrapper

    return _method_wrapper