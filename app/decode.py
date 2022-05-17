"""
This file is responsible for the jwt token decoding
"""


import jwt 
import json
import datetime
import os,sys

def decode_auth_token(auth_token):
   
    """
        Decodes the auth token
        return String
    """
    try:
        # todo save the key in lov table or env variable
        payload = jwt.decode(auth_token, 'secreat',
            algorithms='HS256')
        return payload['data']['sub'] 
    
    except jwt.ExpiredSignatureError:
        return {"error": 'Token expired. Please log in again.', "code": 401}

    except jwt.InvalidTokenError:
        return {"error": "Invalid token. Please log in again.", "code": 403}
    except Exception as e:
        print(e)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return {"error": "exception at decoding token. Please log in again.", "code": 403}