from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import CustomUser

CustomUser = get_user_model()

class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = '__all__'

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=500)
    new_password = serializers.CharField(max_length=500)
    re_password = serializers.CharField(max_length=500)

    def check_pass(self):
        """ checks if both passwords are the same """
        if self.validated_data['new_password'] != self.validated_data['confirm_password']:
            raise serializers.ValidationError({"error":"Please enter matching passwords"})
        return True


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=500)
    password = serializers.CharField(max_length=500)
   

    # def password_validate(self):
    #     if self.initial_data['new_password'] != self.initial_data['re_password']:
    #         raise serializers.ValidationError("Please enter matching passwords")
    #     return True    

    # def validate_new_password(self, value):
    #     if value != self.initial_data['re_password']:
    #         raise serializers.ValidationError("Please enter matching passwords")
    #     return value