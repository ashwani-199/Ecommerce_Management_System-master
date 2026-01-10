from rest_framework import serializers, exceptions
from mysite_management.common_module.mainService import MainService
from apps.apis.UserApi.ApiMessages import UserApiMessages
from apps.apis.UserApi.service import UserQueryService
from apps.users.models import User

class RegisterUserSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'confirm_password']

    # Fields Errors Message
    def __init__(self, *args, **kwargs):
        super(RegisterUserSerializer, self).__init__(*args, **kwargs)
        # Override field required and blank message
        MainService.fieldRequiredMessage(self.fields)

    # Validate data
    def validate(self, data):
        errors = []


        if data.get('username', None) == "" or data.get('username', None) is None:
            error = {
                "field": "username",
                "message": UserApiMessages.username_field_is_required.value
            }
            errors.append(error)
        else:
            user = UserQueryService.getUserByUsername(data.get('username', None))
            if user is not None:
                error = {
                    "field": "username",
                    "message": UserApiMessages.username_is_exist.value
                }
                errors.append(error)

        if data.get('first_name', None) == "" or data.get('first_name', None) is None:
            error = {
                "field": "first_name",
                "message": UserApiMessages.first_name_field_is_required.value
            }
            errors.append(error)

        if data.get('last_name', None) == "" or data.get('last_name', None) is None:
            error = {
                "field": "last_name",
                "message": UserApiMessages.last_name_field_is_required.value
            }
            errors.append(error)

        

        if data.get('email', None) == "" or data.get('email', None) is None:
            error = {
                "field": "email",
                "message": UserApiMessages.email_field_is_required.value
            }
            errors.append(error)
        else:
            user = UserQueryService.getUserByEmail(data.get('email', None))
            if user is not None:
                error = {
                    "field": "email",
                    "message": UserApiMessages.email_is_exist.value
                }
                errors.append(error)

        if data.get('password', None) == "" or data.get('password', None) is None:
            error = {
                "field": "password",
                "message": UserApiMessages.password_field_is_required.value
            }
            errors.append(error)

        if data.get('confirm_password', None) == "" or data.get('confirm_password', None) is None:
            error = {
                "field": "confirm_password",
                "message": UserApiMessages.confirm_password_field_is_required.value
            }
            errors.append(error)

        if data.get('password', None) != data.get('confirm_password', None):
            error = {
                "field": "password",
                "message": UserApiMessages.password_not_match.value
            }
            errors.append(error)

        if len(errors) > 0:
            raise exceptions.ValidationError(errors)
        return data

    # Create UserApi
    def create(self, validated_data):
        UserQueryService.createUser(validated_data)
        return validated_data
    


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'mobile_number', 'image',
                  'user_role_id', 'city', 'state', 'country', 'zip_code',
                  'address1', 'address2', 'is_active']


class UpdateUserSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    username = serializers.CharField(required=True)
    email = serializers.CharField(required=True)
    mobile_number = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'mobile_number', 'gender', 'image',
                  'address1', 'address2', 'city', 'country', 'state', 'zip_code']

    # Fields Errors Message
    def __init__(self, *args, **kwargs):
        super(UpdateUserSerializer, self).__init__(*args, **kwargs)
        # Override field required and blank message
        MainService.fieldRequiredMessage(self.fields)

    # Validate data
    def validate(self, data):
        try:
            user = self.context.get('request', None).user
        except Exception as e:
            print(f"Exception --> {e}")
            user = None
        errors = []

        # Validation Errors
        if data.get('image', None):
            image = data.get('image', None)
            allowedImageFormats = ['jpg', 'png', 'PNG', 'JPEG', 'jpeg']
            fileFormat = str(image).split('.')[-1]
            if fileFormat not in allowedImageFormats:
                error = {
                    "field": "image",
                    "message": UserApiMessages.image_format_not_allowed.value
                }
                errors.append(error)

        if data.get('first_name', None) == "" or data.get('first_name', None) is None:
            error = {
                "field": "first_name",
                "message": UserApiMessages.first_name_field_is_required.value
            }
            errors.append(error)

        if data.get('last_name', None) == "" or data.get('last_name', None) is None:
            error = {
                "field": "last_name",
                "message": UserApiMessages.last_name_field_is_required.value
            }
            errors.append(error)

        if data.get('gender', None) == "" or data.get('gender', None) is None:
            error = {
                "field": "gender",
                "message": UserApiMessages.gender_field_required.value
            }
            errors.append(error)

        if data.get('username', None) == "" or data.get('username', None) is None:
            error = {
                "field": "username",
                "message": UserApiMessages.username_field_is_required.value
            }
            errors.append(error)
        else:
            if user and user.username != data.get('username', None):
                user = UserQueryService.getUserByUsername(data.get('username', None))
                if user is not None:
                    error = {
                        "field": "username",
                        "message": UserApiMessages.username_is_exist.value
                    }
                    errors.append(error)

        if data.get('email', None) == "" or data.get('email', None) is None:
            error = {
                "field": "email",
                "message": UserApiMessages.email_field_is_required.value
            }
            errors.append(error)
        else:
            if user and user.email != data.get('email', None):
                user = UserQueryService.getUserByEmail(data.get('email', None))
                if user is not None:
                    error = {
                        "field": "email",
                        "message": UserApiMessages.email_is_exist.value
                    }
                    errors.append(error)

        if data.get('mobile_number', None) == "" or data.get('mobile_number', None) is None:
            error = {
                "field": "mobile_number",
                "message": UserApiMessages.mobile_number_field_required.value
            }
            errors.append(error)
        else:
            if user and user.mobile != data.get('mobile_number', None):
                user = UserQueryService.getUserByMobile(data.get('mobile_number', None))
                if user is not None:
                    error = {
                        "field": "mobile_number",
                        "message": UserApiMessages.mobile_number_exist.value
                    }
                    errors.append(error)

        if len(errors) > 0:
            raise exceptions.ValidationError(errors)
        return data

    # Update user
    def update(self, instance, validated_data):
        UserQueryService.updateUser(instance.id, validated_data)
        return validated_data