"""
For encodig of jwt token 
"""
import jwt
import datetime
import os
from app.models.confi import M_List_of_Values
def encode_auth_token(subject):
    """
        Generates auth token 
        return: String
    """
    try:
        try:
            LOGIN_SESSION_TIME = int(M_List_of_Values.objects.get(lov_name='LOGIN_SESSION_TIME').lov_value)
        except:
            LOGIN_SESSION_TIME = 4
        payload = {
            'exp': str(datetime.datetime.utcnow() + datetime.timedelta(days=0, hours=LOGIN_SESSION_TIME, seconds=0)),
            'iat': str(datetime.datetime.utcnow()),
            'sub': subject
        }
        

        return jwt.encode(
            {'data': payload}, 
            'secreat',
            algorithm='HS256'
        )
        
    
    except Exception as e:
        return e
