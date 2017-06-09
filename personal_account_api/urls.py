from django.conf.urls import url, include

from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register(r'balance', views.BalanceViewSet, base_name='balance')
router.register(r'incomes', views.IncomesViewSet, base_name='incomes')
router.register(r'expenses', views.ExpensesViewSet, base_name='expenses')
router.register(
        r'savings-goals',
        views.SavingsGoalViewSet,
        base_name='savings_goals')
router.register(r'budget', views.BudgetViewSet, base_name='budget')
router.register(
        r'expenses-by-date',
        views.ExpensesByDateViewSet,
        base_name='expenses-by-date')
router.register(
        r'incomes-by-date',
        views.IncomesByDateViewSet,
        base_name='incomes-by-date')


urlpatterns = [
            url(r'^', include(router.urls)),
            ]
