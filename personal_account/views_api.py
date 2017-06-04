from personal_account.models import Balance
from personal_account.serializers import BalanceSerializer, IncomeSerializer,\
        IncomesByDatesSerializer, ExpensesByDatesSerializer,\
        ExpenseSerializer, SavingsGoalSerializer, BudgetSerializer
from personal_account.filters import IncomesFilter, ExpensesFilter
from rest_framework import generics, permissions
from django.db.models import Sum
from django_filters import rest_framework as filters


class BalanceList(generics.ListCreateAPIView):
    queryset = Balance.objects.all()
    serializer_class = BalanceSerializer
    permission_classes = (permissions.IsAuthenticated,)


class BalanceDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BalanceSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user.balance


class IncomesList(generics.ListCreateAPIView):
    serializer_class = IncomeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        incomes = self.request.user.balance.incomes.all()
        return incomes


class IncomesListByDate(generics.ListAPIView):
    serializer_class = IncomesByDatesSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = IncomesFilter
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        incomes = self.request.user.balance.incomes.values(
                'category__name').annotate(amount_per_category=Sum('amount'))
        return incomes


class ExpensesList(generics.ListCreateAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        expenses = self.request.user.balance.expenses.all()
        return expenses


class ExpensesListByDate(generics.ListAPIView):
    serializer_class = ExpensesByDatesSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = ExpensesFilter
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        expenses = self.request.user.balance.expenses.values(
                'category__name').annotate(amount_per_category=Sum('amount'))
        return expenses


class SavingsGoalList(generics.ListCreateAPIView):
    serializer_class = SavingsGoalSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        savings_goals = self.request.user.balance.savings_goals.all()
        return savings_goals


class BudgetList(generics.ListCreateAPIView):
    serializer_class = BudgetSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        budget = self.request.user.balance.budget.all()
        return budget
