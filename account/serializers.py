from rest_framework import serializers
from .models import AuthUser, UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
	image = serializers.ImageField(required=False, allow_null=True)
	class Meta:
		model = UserProfile
		fields = ['image', 'age', 'gender']


class AuthUserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer() 

    class Meta:
        model = AuthUser
        fields = ['id', 'first_name', 'last_name', 'email', 'profile']
        read_only_fields = ['email'] 

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)  
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if profile_data:
            user_profile = instance.profile
            for attr, value in profile_data.items():
                setattr(user_profile, attr, value)
            user_profile.save()
        return instance


class RegisterUserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, style={'input_type':'password'})
    class Meta:
        model = AuthUser
        fields = ['email', 'first_name', 'last_name', 'password', 'confirm_password']
        extra_kwargs = {
            'password': {'write_only': True, 'style': {'input_type': 'password'}}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError('confirm password does not match.')
        return attrs

    def create(self, validated_data):
        user = AuthUser.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user



class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, style={'input_type':'password'})
 

class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True, style={'input_type':'password'})
    new_password = serializers.CharField(write_only=True, style={'input_type':'password'})
    confirm_password = serializers.CharField(write_only=True, style={'input_type':'password'}) 

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError('confirm password does not match.')
        return attrs


class ForgetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

class NewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, style={'input_type':'password'})
    confirm_password = serializers.CharField(write_only=True, style={'input_type':'password'})