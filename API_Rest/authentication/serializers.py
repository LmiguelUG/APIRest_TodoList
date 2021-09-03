from rest_framework import serializers
from authentication.models import User

class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(max_length = 80, min_length = 8, write_only = True)

    class Meta:
        model = User
        fields = ('id','username','email','password')
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)