


from app.models.user import M_User
from .serializer import UserSerializer
from rest_framework.response import Response

from app.views.imports import *
# this is for sessions authentications
   
@api_view(['GET','POST','PUT','PATCH','DELETE'])
# @permission_check(submenu='/secure/')
def student_api(request):
    if request.method == 'GET':
        get_token = request.META['HTTP_AUTHORIZATION']
        token = get_token[6:].strip()
        resp = decode_auth_token(token)
        user = M_User.objects.get(username=resp['username'])
        serializer = UserSerializer(user)
        return Response(serializer.data)        
    if request.method == 'PATCH':
        get_token = request.META['HTTP_AUTHORIZATION']
        token = get_token[6:].strip()
        resp = decode_auth_token(token)
        user = M_User.objects.get(username=resp['username'])
        serializer = UserSerializer(user, data=request.data,partial=True)
        if serializer.is_valid():
             serializer.save()
             return Response({'msg':'data updated successfully'})
  
       

    