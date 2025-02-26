import os
from .serializers import UserSerializer
from rest_framework import status
from django.core.mail import send_mail
from backend.settings import FRONTEND_URL, EMAIL_HOST_USER
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.response import Response
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes

@api_view(['POST'])
def signup(request):
	"""
    Endpoint to sign up users.
    """

	serializer = UserSerializer(data=request.data)

	if serializer.is_valid():
		user = serializer.save()
		return Response( {
				"message": "sign up successfully",
				"user": serializer.data
			},
			status=status.HTTP_201_CREATED
		)
	return Response(
		serializer.errors,
		status=status.HTTP_400_BAD_REQUEST
	)



@api_view(['POST'])
def signin(request):
	"""
    Endpoint to sign in users.
    """

	try:
		user = authenticate(username=request.data.get('username', None), password=request.data.get('password', None))
		if (user is None):
			return Response( {
					"message": "Invalid credentials"
				},
				status=status.HTTP_401_UNAUTHORIZED
			)
		refresh = RefreshToken.for_user(user)
		response = Response({
			"message": "sign in successfully",
			"super_user": user.is_superuser,
			"access_token": str(refresh.access_token),
			"refresh_token": str(refresh)
		}, status=status.HTTP_200_OK)

		return response
	except Exception as e:
		return Response( {
				"message": str(e)
			},
			status=status.HTTP_400_BAD_REQUEST
		)



@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def signout(request):
	"""
	Endpoint to sign out the current user.
	"""


	return Response( {
			"message": "User logged out successfully"
		},
		status=status.HTTP_200_OK
	)



@api_view(['POST'])
def forget_password(request):
	"""
    Endpoint to initiate password reset process by sending an email to the user.
    """

	username = request.data.get('username', None)
	try:
		user = User.objects.get(username=username)
		uid = urlsafe_base64_encode(force_bytes(user.pk))
		token = default_token_generator.make_token(user)
		reset_password_url = f"{FRONTEND_URL}/reset-password/{uid}/{token}/"

		subject = "Password Reset"
		message = f"Hello,\n\nYou recently requested to reset your password for your account. " \
					f"Please click the link below to reset it:\n\n{reset_password_url}\n\n" \
					f"If you did not request a password reset, please ignore this email or contact support.\n\n" \
					f"Thank you!"
		
		send_mail(subject, message, EMAIL_HOST_USER, [user.email])

		return Response( {
				"message": "Password reset instructions sent successfully."
			},
			status=status.HTTP_200_OK
		)
	except User.DoesNotExist:
		return Response( {
				"message": "No user found with this username."
			},
			status=status.HTTP_404_NOT_FOUND
		)



@api_view(['POST'])
def reset_password(request, uidb64, token):
	"""
	Endpoint to reset user's password using a reset token.
	"""

	try:
		uid = urlsafe_base64_decode(uidb64).decode()
		password = request.data.get('password')
		user = User.objects.get(pk=uid)
	except (TypeError, ValueError, OverflowError, User.DoesNotExist):
		user = None

	if user and default_token_generator.check_token(user, token) and password:
		user.set_password(password)
		user.save()
		return Response( {
				"message": "Password reset successfully"
			},
			status=status.HTTP_200_OK
		)
	else:
		return Response( {
				"message": "Invalid reset link"
			},
			status=status.HTTP_400_BAD_REQUEST
		)



@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_user_info(request):
	"""
	Endpoint to get user information.
	"""

	return Response( {
			"username": request.user.username,
			"email": request.user.email,
			"super_user": request.user.is_superuser
		},
		status=status.HTTP_200_OK
	)
