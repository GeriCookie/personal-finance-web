from django.conf.urls import url
from personal_account import views

urlpatterns = [
    url(r'^new$', views.new_balance, name='new_balance'),
    url(r'^(\d+)/$',
        views.view_balance, name='view_balance'),
    url(r'^(\d+)/income/$', views.income,
        name='income'),
    url(r'^(?P<balance_id>\d+)/income/(?P<date>\d{4}-\d{2}-\d{2})/$',
        views.daily_income,
        name='daily_income'),
    url(r'^(\d+)/expenses/$', views.expenses,
        name='expenses'),
    url(r'^(?P<balance_id>\d+)/expenses/(?P<date>\d{4}-\d{2}-\d{2})/$',
        views.daily_expenses,
        name='daily_expenses'),
    url(
        r'^(?P<balance_id>\d+)/expenses/(?P<start_date>\d{4}-\d{2}-\d{2})/(?P<end_date>\d{4}-\d{2}-\d{2})/$',
        views.weekly_expenses,
        name='weekly_expenses'),
    url(
        r'^(?P<balance_id>\d+)/expenses/m/(?P<start_date>\d{4}-\d{2}-\d{2})/(?P<end_date>\d{4}-\d{2}-\d{2})/$',
        views.montly_expenses,
        name='montly_expenses'),
    url(
        r'^(?P<balance_id>\d+)/expenses/y/(?P<start_date>\d{4}-\d{2}-\d{2})/(?P<end_date>\d{4}-\d{2}-\d{2})/$',
        views.yearly_expenses,
        name='yearly_expenses'),
]
