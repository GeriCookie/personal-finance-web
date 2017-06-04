from django.conf.urls import url, include

from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import views

urlpatterns = [
    url(r'^signup/', CreateView.as_view(
            template_name='signup.html',
            form_class=UserCreationForm,
            success_url='/'
    )),
    url(r'^signin/', views.login, {'template_name': 'signin.html'}),
    url(r'^signout/', views.logout, {'next_page': '/'}),

]

urlpatterns += [
        url(r'^rest-auth/', include('rest_auth.urls')),
        url(r'^rest-auth/registration/',
            include('rest_auth.registration.urls')),
        url(r'^account/', include('allauth.urls')),
        ]
