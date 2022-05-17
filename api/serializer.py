from rest_framework import serializers
from app.models.user import M_User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = M_User
        fields='__all__'