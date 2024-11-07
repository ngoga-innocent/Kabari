from rest_framework import serializers
from .models import Users

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'username', 'email','first_name','last_name', 'password', 'phone_number', 'profile_picture']
        extra_kwargs = {'password': {'write_only': True}}  # Make password write-only

    def create(self, validated_data):
        # Remove the password from validated data and use `set_password`
        password = validated_data.pop('password', None)
        user = Users(**validated_data)
        if password is not None:
            user.set_password(password)  # Hash the password
        user.save()
        return user
