from rest_framework.authentication import TokenAuthentication
from rest_auth.registration.views import LoginView, RegisterView


class RegisterViewCustom(RegisterView):
    authentication_classes = (TokenAuthentication,)


class LoginViewCustom(LoginView):
    authentication_classes = (TokenAuthentication, )
