from apps.users.models import User
from django.contrib.sites.shortcuts import get_current_site
import hashlib
import datetime
import time
import enum
from django.utils.translation import gettext as _
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import render


PROTOCOL = 'http://'
RESET_PASSWORD_URL = '/reset-password/'

class MainMessages(enum.Enum):
    the = _('The')
    field_is_required = _('Field is required.')

class MainService:
    def __init__(self, request):
        self.request = request
        self.currentSite = get_current_site(self.request)
        self.user = None

    def passwordForgotLink(self, user):
        self.user = user
        email = self.user.email
        timeStamp = time.mktime(datetime.datetime.today().timetuple())
        keyString = str(email) + str(timeStamp)
        res = hashlib.md5(keyString.encode())
        tokenString = res.hexdigest()
        user = self.saveForgotPasswordData(tokenString, None)
        return user

    def saveForgotPasswordData(self, tokenString, OTP):
        userObj = User.objects.get(id=self.user.id)
        if OTP is None:
            userObj.forgot_password_string = tokenString
            userObj.save()
        else:
            userObj.forgot_password_string = tokenString
            userObj.forgot_password_otp = OTP
            userObj.save()
        return userObj

    def createUrlString(self, tokenString):
        forgotPasswordUrl = str(self.currentSite) + RESET_PASSWORD_URL + tokenString + '/'
        return forgotPasswordUrl
    

    @staticmethod
    def getJwtToken(typeName, user):
        refresh = RefreshToken.for_user(user)
        data = {}
        if typeName == 'ACCESS_TOKEN':
            data['access_token'] = str(refresh.access_token)
        else:
            data['refresh_token'] = str(refresh)
        return data


    @staticmethod
    def fieldRequiredMessage(fields):
        for field in fields:
            fields[field].error_messages["required"] = MainMessages.the.value + ' ' + \
                                                       field.replace('_', ' ') + ' ' + \
                                                       MainMessages.field_is_required.value.lower()

            fields[field].error_messages["blank"] = MainMessages.the.value + ' ' + \
                                                    field.replace('_', ' ') + ' ' + \
                                                    MainMessages.field_is_required.value.lower()


    @staticmethod
    def error_404(request, exception):
        data = {}
        return render(request, 'errors/404.html', data)

    @staticmethod
    def error_500(request, *args, **argv):
        return render(request, 'errors/500.html', status=500)

    @staticmethod
    def error_400(request, *args, **argv):
        return render(request, 'errors/400.html', status=400)

    @staticmethod
    def error_403(request, *args, **argv):
        return render(request, 'errors/403.html', status=403)