from .serializers import *
from .models import UserProfile, AuthUser, BlacklistedToken
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib import auth
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import get_tokens_for_user, send_activation_email, send_password_reset_email
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import ValidationError
# Create your views here.

# Register User View
@extend_schema(tags=["Authentication and User"])
class RegisterView(APIView):
	serializer_class = RegisterUserSerializer
	permission_classes = [AllowAny]

	@extend_schema(
        responses={
            200: RegisterUserSerializer,
        },
        request=RegisterUserSerializer,
        description='Register a user with user profile.'
    )
	def post(self, request):
		serializer = self.serializer_class(data=request.data)
		if serializer.is_valid():
			user = serializer.save()
			
			send_activation_email(user, request)
			return Response({'messages':'A verification email has been sended to your mail, Please verify your email to complete registration.'},
				status=status.HTTP_201_CREATED
				)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["Authentication and User"])
class EmailVerificationView(APIView):
	permission_classes = [AllowAny]


	@extend_schema(
		responses={
            200: {
                'description': 'Email verified successfully.'
            },
            400: {
                'description': 'Invalid or expired token.'
            }
        },
		description='This endpoint enables users to confirm their email address and activate their account.'
	)
	def get(self, request, uidb64, token):
		try:
			uid = force_str(urlsafe_base64_decode(uidb64))
			user = get_user_model().objects.get(pk=uid)

			if default_token_generator.check_token(user, token):
				if user.mail_verified is True:
					return Response({'messages':'Your email is already verified!'}, status=status.HTTP_200_OK)

				user.mail_verified = True
				user.save()
				return Response({'messages':'Your email has been verified !'}, status=status.HTTP_200_OK)
			else:
				return Response({'errors':'Invalid or expired token.'}, status=status.HTTP_400_BAD_REQUEST)
		
		except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
			return Response({"error": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)


# Update User Information and Retrieve User
@extend_schema(tags=["Authentication and User"])
class UserView(APIView):
	serializer_class = AuthUserSerializer
	permission_classes = [IsAuthenticated]


	@extend_schema(
		responses={
			200:AuthUserSerializer,
		},
		request=AuthUserSerializer,
		description='Get user information.'
	)
	def get(self, request):
		user = request.user
		serializer = self.serializer_class(user)
		return Response(serializer.data, status=status.HTTP_200_OK)


	@extend_schema(
		responses={
			200:AuthUserSerializer,
		},
		request=AuthUserSerializer,
		description='Update user & profile information.'
	)
	def patch(self, request):
		user = request.user
		serializer = self.serializer_class(user, data=request.data, partial=True)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_200_OK)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["Authentication and User"])
class LoginView(APIView):
	serializer_class = LoginSerializer
	permission_classes = [AllowAny]

	@extend_schema(
		responses={
			200:LoginSerializer,
		},
		request=LoginSerializer,
		description='login user with email and password.'
	)
	def post(self, request):
		serializer = self.serializer_class(data=request.data)
		if serializer.is_valid():
			email = request.data.get('email')
			password = request.data.get('password')
			user = auth.authenticate(email=email, password=password)
			if user is not None:
				token = get_tokens_for_user(user)
				user_serializer = AuthUserSerializer(user)
				return Response({'token':token, 'user':user_serializer.data}, status=status.HTTP_200_OK)
			else:
				return Response({'errors':'your login credentials are not valid'}, status=status.HTTP_404_NOT_FOUND)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)		


@extend_schema(tags=["Authentication and User"])
class LogoutView(APIView):
	permission_classes = [IsAuthenticated]

	@extend_schema(
        responses={
            200: {
                'description': 'Successfully logged out.'
            },
            400: {
                'description': 'Invalid request!'
            }
        },
        description="Log out user by blacklisting their tokens."
    )
	def post(self, request):
		refresh_token = request.headers.get('Refresh')
		access_token = request.headers.get('Authorization', None)

		if refresh_token:
			try:
				refresh = RefreshToken(refresh_token)
				refresh.blacklist()
			except Exception as e:
				return Response({f'errors':'Invalid refresh token: {e}.'}, status=status.HTTP_400_BAD_REQUEST)

		if access_token:
			try:
				parts = access_token.split()
				if len(parts) == 2 and parts[0].lower() == 'bearer':
					token = parts[1]
					BlacklistedToken.objects.create(token=token)
				else:
					return Response({"detail": "Invalid access token format"}, status=status.HTTP_400_BAD_REQUEST)
			except Exception as e:
				return Response({'errors':f'Invalid access token: {e}'}, status=status.HTTP_400_BAD_REQUEST)
		return Response({'messages':'successfully logged out.'}, status=status.HTTP_200_OK)


@extend_schema(tags=["Authentication and User"])
class ChangePasswordView(APIView):
	serializer_class = ChangePasswordSerializer
	permission_classes = [IsAuthenticated]

	@extend_schema(
		responses={
			200:ChangePasswordSerializer,
		},
		request=ChangePasswordSerializer,
		description='Change authenticated user password.'
	)
	def patch(self, request):
		serializer = self.serializer_class(data=request.data)
		if serializer.is_valid():
			user = request.user
			current_password = request.data.get('current_password')
			new_password = request.data.get('new_password')

			if not user.check_password(current_password):
				return Response({'messages':'Current password is incorrect'}, status=status.HTTP_404_NOT_FOUND)

			try:
				validate_password(new_password, user)
			except ValidationError as e:
				return Response({'errors':e}, status=status.HTTP_400_BAD_REQUEST)


			user.set_password(new_password)
			user.save()
			return Response({'messages':'Password Updated successfully.'}, status=status.HTTP_200_OK)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Authentication and User'])
class ForgetPasswordView(APIView):
	serializer_class = ForgetPasswordSerializer
	permission_classes = [AllowAny]

	@extend_schema(
		responses={
			200:ForgetPasswordSerializer,
			400:ForgetPasswordSerializer
		},
		request=ForgetPasswordSerializer,
		description='Reset user password by email.'
	)
	def post(self, request):
		serializer = self.serializer_class(data=request.data)
		if serializer.is_valid():
			email = request.data.get('email')
			try:
				user = get_user_model().objects.get(email=email)
				send_password_reset_email(user, request)
				return Response(
					{'messages':'A reset password email has been sended to your mail, Please follow the instructions mentioned on the mail body to reset your password'},
					status=status.HTTP_200_OK
				)
			except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist): 
				return Response({'messages':'No user account is found with this mail.'}, status=status.HTTP_404_NOT_FOUND)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
