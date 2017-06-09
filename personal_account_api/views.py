from models.models import Balance
from .serializers import BalanceSerializer, IncomeSerializer,\
        IncomesByDatesSerializer, ExpensesByDatesSerializer,\
        ExpenseSerializer, SavingsGoalSerializer, BudgetSerializer
from .filters import IncomesFilter, ExpensesFilter

from rest_framework import permissions
from django.db.models import Sum
from django_filters import rest_framework as filters
from rest_framework import viewsets


class BalanceViewSet(viewsets.ModelViewSet):
    serializer_class = BalanceSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Balance.objects.filter(owner=self.request.user)


class IncomesViewSet(viewsets.ModelViewSet):
    serializer_class = IncomeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        incomes = self.request.user.balance.incomes.all()
        return incomes


class IncomesByDateViewSet(viewsets.ModelViewSet):
    serializer_class = IncomesByDatesSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = IncomesFilter
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        incomes = self.request.user.balance.incomes.values(
                'category__name').annotate(amount_per_category=Sum('amount'))
        return incomes


class ExpensesViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        expenses = self.request.user.balance.expenses.all()
        return expenses


class ExpensesByDateViewSet(viewsets.ModelViewSet):
    serializer_class = ExpensesByDatesSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = ExpensesFilter
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        expenses = self.request.user.balance.expenses.values(
                'category__name').annotate(amount_per_category=Sum('amount'))
        return expenses


class SavingsGoalViewSet(viewsets.ModelViewSet):
    serializer_class = SavingsGoalSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        savings_goals = self.request.user.balance.savings_goals.all()
        return savings_goals


class BudgetViewSet(viewsets.ModelViewSet):
    serializer_class = BudgetSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        budget = self.request.user.balance.budget.all()
        return budget
