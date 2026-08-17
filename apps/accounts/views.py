from django.utils import timezone
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status, serializers, generics
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView

from apps.shared.utility import send_email, check_auth_type
from .models import CODE_VERIFIED, NEW, UserConfirmation, VIA_EMAIL, VIA_PHONE_NUMBER, User
from .serializers import SignupSerializer, VerifySerializer, VerifyResponseSerializer, ChangeUserInformationSerializer, \
    ChangeUserAvatarSerializer, LoginSerializer, LoginRefreshSerializer, LoginResponseSerializer, LogoutSerializer, \
    ForgotPasswordSerializer, ResetPasswordSerializer, UserSerializer


class SignupAPIView(APIView):

    permission_classes = [
        permissions.AllowAny
    ]

    serializer_class = SignupSerializer

    @swagger_auto_schema(
        request_body=SignupSerializer,
        responses={
            201: "User created successfully",
            400: "Bad request",
        }
    )
    def post(self, request):

        serializer = self.serializer_class(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

class VerifyAPIView(APIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]

    @swagger_auto_schema(
        request_body=VerifySerializer,
        responses={
            200: openapi.Response(
                description="Verification successful",
                schema=VerifyResponseSerializer
            ),
            400: "Invalid verification code",
        }
    )
    def post(self, request):
        user = request.user

        serializer = VerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        code = serializer.validated_data["code"]

        self.check_verify_code(user, code)

        return Response(
            data={
                "success": True,
                "auth_status": user.auth_status,
                # "access": user.access_token,
                # "refresh": user.refresh_token,
            },
            status=status.HTTP_200_OK
        )

    @classmethod
    def check_verify_code(cls, user, code):
        verifies = UserConfirmation.objects.filter(
            user=user,
            expiration_time__gte=timezone.now(),
            code=code,
            is_confirmed=False
        )

        if not verifies.exists():
            raise serializers.ValidationError({
                "code": "Verification code expired or not available"
            })
        else:
            verifies.update(is_confirmed=True)

        if user.auth_status == NEW:
            user.auth_status = CODE_VERIFIED
            user.save(update_fields=["auth_status"])

        return True

class GetNewVerifyAPIView(APIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]
    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                succes=True,
                description="Verification successful",
            )
        }
    )
    def get(self, request):
        if self.is_none_check_verify_code(request.user):
            code = request.user.create_verify_code(request.user.auth_type)
            if request.user.auth_type == VIA_EMAIL:
                send_email(request.user.email, code)
            elif request.user.auth_type == VIA_PHONE_NUMBER:
                send_email(request.user.phone_number, code)
                # send_phone_number(request.user.phone_number, code)
            return Response(
                data={
                    "success": True,
                    "message": "Verification successful",
                    'auth_status': request.user.auth_status,
                }
            )
        else:
            return Response(
                data={
                    "success": False,
                    "message": "You have an active code."
                }
            )

    @classmethod
    def is_none_check_verify_code(cls, user):
        verifies = UserConfirmation.objects.filter(
            user=user,
            expiration_time__gte=timezone.now(),
            is_confirmed=False
        )
        if verifies.exists():
            raise serializers.ValidationError({
                'message': "You have an active code."
            })
        return True

class ChangeUserInformationAPIView(APIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = ChangeUserInformationSerializer
    http_method_names = ['post']
    @swagger_auto_schema(
        request_body=ChangeUserInformationSerializer,
        responses={
            200: openapi.Response(
                description="Change user info",
                schema=ChangeUserInformationSerializer
            )
        }
    )
    def post(self, request):
        serializer = self.serializer_class(instance=request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {
                "success": True,
                "message": "User changed successfully",
                'data': serializer.data,
                'auth_status': request.user.auth_status,
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            raise serializers.ValidationError(serializer.errors)

class ChangeUserAvatarAPIView(APIView):
    http_method_names = ['put', 'patch']

    permission_classes = [
        permissions.IsAuthenticated
    ]

    serializer_class = ChangeUserAvatarSerializer

    @swagger_auto_schema(
        request_body=ChangeUserAvatarSerializer,
        responses={
            200: openapi.Response(
                description="Change user avatar",
                schema=ChangeUserAvatarSerializer
            )
        }
    )
    def put(self, request):
        serializer = self.serializer_class(
            instance=request.user,
            data=request.data
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                "success": True,
                "message": "User avatar changed successfully",
                "data": serializer.data,
                "auth_status": request.user.auth_status,
            },
            status=status.HTTP_200_OK
        )

    @swagger_auto_schema(
        request_body=ChangeUserAvatarSerializer,
        responses={
            200: openapi.Response(
                description="Change user avatar",
                schema=ChangeUserAvatarSerializer
            )
        }
    )
    def patch(self, request):
        serializer = self.serializer_class(
            instance=request.user,
            data=request.data,
            partial=True
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                "success": True,
                "message": "User avatar changed successfully",
                "data": serializer.data,
                "auth_status": request.user.auth_status,
            },
            status=status.HTTP_200_OK
        )

class CustomLoginAPIView(APIView):
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = LoginSerializer
    http_method_names = ['post']
    @swagger_auto_schema(
        request_body=LoginSerializer,
        responses={
            200: openapi.Response(
                description="Login successful",
                schema=LoginResponseSerializer
            )
        }
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        tokens = user.tokens()
        tokens.update({
            'message': 'Login successful',
            'username': user.username,
        })
        return Response(tokens, status=status.HTTP_200_OK)

class LoginRefreshAPIView(TokenRefreshView):
    serializer_class = LoginRefreshSerializer

class LogoutAPIView(APIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = LogoutSerializer
    @swagger_auto_schema(
        request_body=LogoutSerializer,
        responses={
            200: openapi.Response(
                description="Logout successful",
            )
        }
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            refresh = request.data['refresh']
            token = RefreshToken(refresh)
            token.blacklist()
            data = {
                "success": True,
                "message": "Logout successful",
            }
            return Response(data, status=status.HTTP_204_NO_CONTENT)
        except TokenError as e:
            raise TokenError(e.args[0])

class ForgotPasswordAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ForgotPasswordSerializer
    @swagger_auto_schema(
        request_body=ForgotPasswordSerializer,
        responses={
            200: openapi.Response(
                description="Forgot password successful",
                schema=ForgotPasswordSerializer
            )
        }
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number_or_email = serializer.validated_data['phone_number_or_email']
        user = serializer.validated_data['user']
        token = user.tokens()
        if check_auth_type(phone_number_or_email) == VIA_EMAIL:
            code = user.create_verify_code(VIA_EMAIL)
            send_email(user.email, code)
            data = {
                "success": True,
                "message": "A code has been sent to your email!",
                'access': token['access'],
                'refresh': token['refresh'],
            }
        elif check_auth_type(phone_number_or_email) == VIA_PHONE_NUMBER:
            code = user.create_verify_code(VIA_PHONE_NUMBER)
            send_email(user.email, code)
            data = {
                "success": True,
                "message": "A code has been sent to your email!",
                'access': token['access'],
                'refresh': token['refresh'],
            }
        else:
            data = {
                "success": False,
                "message": "Invalid phone number or phone number. Please try again. Not found user",
            }
            raise NotFound(data)
        return Response(data, status=status.HTTP_200_OK)

class ResetPasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ResetPasswordSerializer
    @swagger_auto_schema(
        request_body=ResetPasswordSerializer,
        responses={
            200: openapi.Response(
                description="Reset password successful",
                schema=ResetPasswordSerializer
            )
        }
    )
    def put(self, request):
        serializer = self.serializer_class(instance=request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {
            "success": True,
            "message": "Reset password successful",
            "auth_status": request.user.auth_status,
            "username": request.user.username,
        }
        return Response(data, status=status.HTTP_200_OK)

class GetMeGenericAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        request = self.request
        return request.user

class ChangeUserAPIView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()

    def get_object(self):
        return self.request.user

    @swagger_auto_schema(
        request_body=UserSerializer,
        responses={
            200: openapi.Response(
                description="Change user details",
                schema=UserSerializer
            )
        }
    )
    def update(self, request,  *args, **kwargs):
        serializer = self.serializer_class(instance=request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {
            "success": True,
            "message": "Change user details successful",
            "data": serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)