from rest_framework import serializers
from .models import Profile
from django.contrib.auth.models import User



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ('id','first_name','last_name','email','username')

class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    class Meta:
        model = Profile
        fields = ['user','image']
    
    def get_user(self, obj): 
        print(dir(obj.user))
        serializer = UserSerializer(obj)
        return serializer.data 
    

