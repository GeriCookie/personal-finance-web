from django.conf.urls import url
from personal_account import views, views_api


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
    url(r'^api/balance/all/$', views_api.BalanceList.as_view()),
    url(r'^api/balance/detail/$', views_api.BalanceDetail.as_view()),
    url(r'^api/balance/incomes/$', views_api.IncomesList.as_view()),
    url(r'^api/balance/expenses/$', views_api.ExpensesList.as_view()),
    url(r'^api/balance/savings-goals/$',
        views_api.SavingsGoalList.as_view()),
    url(r'^api/balance/expenses-by-date/$', views_api.ExpensesListByDate.as_view()),
    url(r'^api/balance/incomes-by-date/$', views_api.IncomesListByDate.as_view()),
]
