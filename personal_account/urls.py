from django.conf.urls import url
from personal_account import views

urlpatterns = [
    url(r'^new$', views.new_balance, name='new_balance'),
    url(r'^(\d+)/$',
        views.view_balance, name='view_balance'),
    url(r'^(\d+)/income/$', views.income,
        name='income'),
    url(r'^(\d+)/expenses/$', views.expenses,
        name='expenses'),
]
