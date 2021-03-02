from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    profile_pic = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['username', 'profile_pic']
    
    def get_profile_pic(self, user):
        request = self.context.get('request')
        profile_pic = user.profile_pic.url
        return request.build_absolute_uri(profile_pic)

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def create(self, validated_data):
        return User.objects.create_user(email=validated_data['email'], username=validated_data['username'], password=validated_data['password'])

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, write_only=True)
    password = serializers.CharField(write_only=True)
   
    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)

        if email is None:
            raise serializers.ValidationError('Email is required.')
        if password is None:
            raise serializers.ValidationError('Password is required.')

        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError('Invalid Credentials.')
        
        if not user.is_active:
            raise serializers.ValidationError('User inactive or deleted.')

        return user