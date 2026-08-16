from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.validators import FileExtensionValidator
from django.db.models import Q
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenRefreshSerializer

from apps.shared.utility import check_auth_type, send_email, check_login_type
from .models import (
    User,
    VIA_EMAIL,
    VIA_PHONE_NUMBER, CODE_VERIFIED, DONE, NEW, VIA_USERNAME, PHOTO_DONE,
)


class SignupSerializer(serializers.ModelSerializer):

    id = serializers.UUIDField(read_only=True)
    phone_number_or_email = serializers.CharField(
        required=True,
        write_only=True,
    )

    class Meta:
        model = User
        fields = (
            'id',
            'phone_number_or_email',
            'auth_type',
            'auth_status',
        )

        extra_kwargs = {
            'auth_type': {
                'read_only': True,
            },
            'auth_status': {
                'read_only': True,
            },
        }

    def validate(self, attrs):
        identifier = attrs.pop(
            'phone_number_or_email'
        )

        auth_type = check_auth_type(identifier)

        if auth_type == VIA_EMAIL:
            if User.objects.filter(email=identifier).exists():
                raise serializers.ValidationError(
                    {
                        'email': 'Email address is already in use',
                    }
                )
            attrs['email'] = identifier

        elif auth_type == VIA_PHONE_NUMBER:
            if User.objects.filter(phone_number=identifier).exists():
                raise serializers.ValidationError(
                    {
                        'phone_number': 'Phone number is already in use',
                    }
                )
            attrs['phone_number'] = identifier
        else:
            raise serializers.ValidationError(
                {
                    'phone_number_or_email': 'Phone number or email is invalid',
                }
            )

        attrs['auth_type'] = auth_type
        attrs['auth_status'] = NEW

        return attrs

    def create(self, validated_data):
        user = super().create(validated_data)

        if user.auth_type == VIA_EMAIL:
            code = user.create_verify_code(VIA_EMAIL)
            send_email(user.email, code)

        elif user.auth_type == VIA_PHONE_NUMBER:
            code = user.create_verify_code(VIA_PHONE_NUMBER)
            send_email(user.phone_number, code)
            # send_phone_number(user.phone_number, code)
        else:
            raise serializers.ValidationError(
                {
                    'phone_number_or_email': 'Phone number or email is invalid',
                }
            )

        return user

    def to_representation(self, instance):
        data = super(SignupSerializer, self).to_representation(instance)
        data.update(instance.tokens())
        return data

class VerifySerializer(serializers.Serializer):
    code = serializers.CharField(max_length=4, write_only=True)

class VerifyResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    auth_status = serializers.CharField()
    access = serializers.CharField()
    refresh = serializers.CharField()

class ChangeUserInformationSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    first_name = serializers.CharField(write_only=True, required=False)
    last_name = serializers.CharField(write_only=True, required=False)
    username = serializers.CharField(write_only=True, required=True, max_length=50, min_length=5)
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'gender', 'username', 'password', 'confirm_password']

    def validate(self, attrs):
        password = attrs.pop('password', None)
        confirm_password = attrs.pop('confirm_password', None)
        if password != confirm_password:
            raise serializers.ValidationError(
                {
                    'password': 'Password does not match',
                }
            )
        elif len(password) < 8 or password.isdigit() or password.isalpha():
            raise serializers.ValidationError(
                {
                    'password': 'Password is too short, alphanumeric',
                }
            )
        else:
            validate_password(password)
            validate_password(confirm_password)
        attrs['password'] = password
        return attrs

    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                {
                    'username': 'Username is already in use',
                }
            )
        elif len(username) < 4 or len(username) > 16:
            raise serializers.ValidationError(
                {
                    'username': 'Username is too short or longer than 16 characters',
                }
            )
        elif username.isdigit() or username.isnumeric():
            raise serializers.ValidationError(
                {
                    'username': 'Username is an invalid character',
                }
            )
        else:
            return username

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.password = validated_data.get('password', instance.password)
        if validated_data.get('password'):
            instance.set_password(validated_data.get('password'))
        if instance.auth_status == CODE_VERIFIED:
            instance.auth_status = DONE
        instance.save()
        return instance

class ChangeUserAvatarSerializer(serializers.Serializer):
    avatar = serializers.ImageField(
        required=True,
        validators=[
            FileExtensionValidator(
                allowed_extensions=[
                    'jpg',
                    'png',
                    'jpeg',
                    'heic',
                    'heif',
                ]
            )
        ]
    )

    def update(self, instance, validated_data):
        if instance.auth_status in [DONE, PHOTO_DONE]:
            instance.avatar = validated_data['avatar']
            instance.auth_status = PHOTO_DONE
            instance.save(update_fields=['avatar', 'auth_status'])
            instance.save()
        else:
            raise serializers.ValidationError(
                {
                    "aith_status": "User not verified"
                }
            )

        return instance

class LoginSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_input'] = serializers.CharField()
        self.fields['password'] = serializers.CharField(
            write_only=True
        )

    def validate(self, attrs):
        attrs['user'] = self.auth_validate(attrs)
        return attrs

    @classmethod
    def auth_validate(cls, validated_data):
        user_input = validated_data.pop('user_input')
        password = validated_data.pop('password')

        login_type = check_login_type(user_input)

        if login_type == VIA_EMAIL:
            user_obj = User.objects.filter(
                email__iexact=user_input
            ).first()

            if not user_obj:
                raise serializers.ValidationError({
                    'user_input': 'Email not found'
                })

            if not (user_obj.auth_status == PHOTO_DONE or user_obj.auth_status == DONE):
                raise serializers.ValidationError({
                    'auth_type': 'Not full registration'
                })

            user = authenticate(
                username=user_obj.username,
                password=password
            )

            if user is not None:
                return user

            raise serializers.ValidationError({
                'password': 'Password error'
            })

        elif login_type == VIA_PHONE_NUMBER:
            user_obj = User.objects.filter(
                phone_number__iexact=user_input
            ).first()

            if not user_obj:
                raise serializers.ValidationError({
                    'user_input': 'Phone number not found'
                })

            if not (user_obj.auth_type == PHOTO_DONE or user_obj.auth_status == DONE):  # auth_type (photo_done yoki done) da bo'lmasa
                raise serializers.ValidationError({
                    'auth_type': 'Not full registration'
                })

            user = authenticate(
                username=user_obj.username,
                password=password
            )

            if user is not None:
                return user

            raise serializers.ValidationError({
                'password': 'Password error'
            })

        elif login_type == VIA_USERNAME:
            user_obj = User.objects.filter(
                username__iexact=user_input
            ).first()

            if not user_obj:
                raise serializers.ValidationError({
                    'user_input': 'Username not found'
                })

            if user_obj.auth_status not in [PHOTO_DONE, DONE]:
                raise serializers.ValidationError({
                    'auth_type': 'Not full registration'
                })

            user = authenticate(
                username=user_obj.username,
                password=password
            )

            if user is not None:
                return user

            raise serializers.ValidationError({
                'password': 'Password error'
            })

        raise serializers.ValidationError({
            'user_input': 'User not found'
        })

class LoginResponseSerializer(serializers.Serializer):
    message = serializers.CharField(read_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

class LoginRefreshSerializer(TokenRefreshSerializer):
    pass

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(write_only=True)

class ForgotPasswordSerializer(serializers.Serializer):
    phone_number_or_email = serializers.EmailField(required=True, write_only=True)

    def validate(self, attrs):
        phone_number_or_email = attrs['phone_number_or_email']

        auth_type = check_auth_type(phone_number_or_email)

        if auth_type not in (VIA_PHONE_NUMBER, VIA_EMAIL):
            raise serializers.ValidationError({
                'phone_number_or_email':
                    'Phone number or email is not valid.'
            })

        if auth_type == VIA_EMAIL:
            user = User.objects.filter(
                email__iexact=phone_number_or_email
            ).first()
        else:
            user = User.objects.filter(
                phone_number=phone_number_or_email
            ).first()

        if not user:
            raise serializers.ValidationError({
                'phone_number_or_email':
                    'User not found.'
            })

        attrs['user'] = user
        return attrs

class ResetPasswordSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.pop('confirm_password')
        if password != confirm_password:
            raise serializers.ValidationError({
                'password': 'Password mismatch'
            })
        elif len(password) < 8:
            raise serializers.ValidationError({
                'password': 'Password should be at least 8 characters'
            })
        elif password.isdigit() or password.isalpha():
            raise serializers.ValidationError({
                'password': 'Password should only contain digits or letters'
            })
        else:
            return attrs

    def update(self, instance, validated_data):
        password = validated_data.pop('password')
        instance.set_password(password)
        instance.save()
        return instance