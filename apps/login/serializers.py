from rest_framework import serializers, exceptions
from django.contrib.auth.hashers import check_password
from mysite_management.common_module.mainService import MainService
from apps.apis.UserApi.ApiMessages import UserApiMessages
from apps.apis.UserApi.service import UserQueryService
from apps.users.models import User

class LoginUserSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['email', 'password']

    # Fields Errors Message
    def __init__(self, *args, **kwargs):
        super(LoginUserSerializer, self).__init__(*args, **kwargs)
        # Override field required and blank message
        MainService.fieldRequiredMessage(self.fields)

    # Validate data
    def validate(self, data):
        errors = []
        email = data.get('email', None)
        password = data.get('password', None)

        if email == "" or email is None:
            error = {
                "field": "email",
                "message": UserApiMessages.email_field_is_required.value
            }
            errors.append(error)

        if password == "" or password is None:
            error = {
                "field": "password",
                "message": UserApiMessages.password_field_is_required.value
            }
            errors.append(error)

        user = UserQueryService.getUserByEmail(email)
        if user is None:
            error = {
                "field": "email",
                "message": UserApiMessages.email_is_not_exists.value
            }
            errors.append(error)
        else:
            if not check_password(password, user.password):
                error = {
                    "field": "password",
                    "message": UserApiMessages.password_not_match.value
                }
                errors.append(error)

        if len(errors) > 0:
            raise exceptions.ValidationError(errors)
        return data