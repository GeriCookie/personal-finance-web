from django.conf.urls import url
from personal_account import views, views_api

urlpatterns = [
    url(r'^new$', views.new_balance, name='new_balance'),
    url(r'^(\d+)/$',
        views.view_balance, name='view_balance'),
    url(r'^(\d+)/income/$', views.income,
        name='income'),
    url(r'^(?P<balance_id>\d+)/income/(?P<date>\d{4}-\d{2}-\d{2})/$',
        views.daily_income,
        name='daily_income'),
    url(
        r'^(?P<balance_id>\d+)/income/(?P<start_date>\d{4}-\d{2}-\d{2})/(?P<end_date>\d{4}-\d{2}-\d{2})/$',
        views.weekly_income,
        name='weekly_income'),
    url(
        r'^(?P<balance_id>\d+)/income/m/(?P<start_date>\d{4}-\d{2}-\d{2})/(?P<end_date>\d{4}-\d{2}-\d{2})/$',
        views.montly_income,
        name='montly_income'),
    url(
        r'^(?P<balance_id>\d+)/income/y/(?P<start_date>\d{4}-\d{2}-\d{2})/(?P<end_date>\d{4}-\d{2}-\d{2})/$',
        views.yearly_income,
        name='yearly_income'),
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
    url(r'^api/balance/$', views_api.BalanceList.as_view()),
    url(r'^api/balance/(?P<pk>[0-9]+)/$', views_api.BalanceDetail.as_view()),
    url(r'^api/balance/(?P<balance_id>[0-9]+)/incomes/$', views_api.IncomesList.as_view()),
    url(r'^api/balance/(?P<balance_id>[0-9]+)/expenses/$', views_api.ExpensesList.as_view()),
    url(r'^api/balance/(?P<balance_id>[0-9]+)/expenses-by-date/$', views_api.ExpensesListByDate.as_view()),
    url(r'^api/balance/(?P<balance_id>[0-9]+)/incomes-by-date/$', views_api.IncomesListByDate.as_view()),
]
