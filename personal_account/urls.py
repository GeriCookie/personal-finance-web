from django.conf.urls import url
from personal_account import views

urlpatterns = [
    url(r'^new$', views.new_balance, name='new_balance'),
    url(r'^(\d+)/$',
        views.view_balance, name='view_balance'),
    url(r'^(\d+)/add_income$', views.add_income,
        name='add_income'),
    url(r'^(\d+)/add_expense$', views.add_expense,
        name='add_expense'),
]
