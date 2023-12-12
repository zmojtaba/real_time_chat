from rest_framework.views import APIView
from rest_framework.response import Response
from ..api.serializer import *
from django.contrib.auth import get_user_model, authenticate
from rest_framework import status
from mail_templated import EmailMessage

from .user_auth import *
from utilss.user_token import custome_refresh_token as ctoken
from utilss.user_email import EmailThreading
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenBlacklistView)
from django.conf import settings
from utilss.user_message import io

User = get_user_model()

class UserRegistrationApiView(APIView):
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):       
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # send email to created user
        refresh_token, access_token = ctoken.get_tokens_for_user(user)

        if user.email:
            code = user_utils.create_verification_code()
            verification_refresh_token, verification_access_token = ctoken.get_token_for_email_verification(user, code)

            verification_email = EmailMessage('emails/email_varification.html', 
                                        {'verification_code':code}, 
                                        settings.EMAIL_HOST_USER, 
                                        [user.email])
            
            EmailThreading(verification_email).start()
            return Response({
                'message':"sign up successfully",
                'refresh_token' : refresh_token,
                'access_token' : access_token,
                'verification_refresh_token': verification_refresh_token
            }, status=status.HTTP_201_CREATED)

class UserLoginView(TokenObtainPairView):
    serializer_class = UserLoginSerializer

class LogoutView(APIView):
    permission_classes = (IsAuthenticated, )
    # serializer_class = LogoutSerializer
    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(io._success('You have logged out successfully'), status=status.HTTP_205_RESET_CONTENT)
        except:
            io._error("Token is blacklisted")