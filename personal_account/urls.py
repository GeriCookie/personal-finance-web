from django.conf.urls import url
from personal_account import views


urlpatterns = [
    url(r'^$',
        views.view_balance, name='view_balance'),
    url(r'^income/$', views.income,
        name='income'),
    url(r'^income/(?P<date>\d{4}-\d{2}-\d{2})/$',
        views.daily_income,
        name='daily_income'),
    url(
        r'^income/(?P<start_date>\d{4}-\d{2}-\d{2})/(?P<end_date>\d{4}-\d{2}-\d{2})/$',
        views.weekly_income,
        name='weekly_income'),
    url(
        r'^income/m/(?P<start_date>\d{4}-\d{2}-\d{2})/(?P<end_date>\d{4}-\d{2}-\d{2})/$',
        views.montly_income,
        name='montly_income'),
    url(
        r'^income/y/(?P<start_date>\d{4}-\d{2}-\d{2})/(?P<end_date>\d{4}-\d{2}-\d{2})/$',
        views.yearly_income,
        name='yearly_income'),
    url(r'^expenses/$', views.expenses,
        name='expenses'),
    url(r'^expenses/(?P<date>\d{4}-\d{2}-\d{2})/$',
        views.daily_expenses,
        name='daily_expenses'),
    url(
        r'^expenses/(?P<start_date>\d{4}-\d{2}-\d{2})/(?P<end_date>\d{4}-\d{2}-\d{2})/$',
        views.weekly_expenses,
        name='weekly_expenses'),
    url(
        r'^expenses/m/(?P<start_date>\d{4}-\d{2}-\d{2})/(?P<end_date>\d{4}-\d{2}-\d{2})/$',
        views.montly_expenses,
        name='montly_expenses'),
    url(
        r'^expenses/y/(?P<start_date>\d{4}-\d{2}-\d{2})/(?P<end_date>\d{4}-\d{2}-\d{2})/$',
        views.yearly_expenses,
        name='yearly_expenses'),
]
