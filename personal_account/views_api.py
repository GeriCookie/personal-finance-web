from personal_account.models import Balance
from personal_account.serializers import BalanceSerializer, IncomeSerializer,\
        IncomesByDatesSerializer, ExpensesByDatesSerializer, ExpenseSerializer
from personal_account.filters import IncomesFilter, ExpensesFilter
from rest_framework import generics
from django.db.models import Sum
from django_filters import rest_framework as filters


class BalanceList(generics.ListCreateAPIView):
    queryset = Balance.objects.all()
    serializer_class = BalanceSerializer


class BalanceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Balance.objects.all()
    serializer_class = BalanceSerializer


class IncomesList(generics.ListCreateAPIView):
    serializer_class = IncomeSerializer
    lookup_url_kwarg = 'balance_id'

    def get_queryset(self):
        balance_id = self.kwargs.get(self.lookup_url_kwarg)
        incomes = Balance.objects.get(id=balance_id).incomes.all()
        return incomes

    def get_serializer_context(self):
        return {"balance_id": self.kwargs.get(self.lookup_url_kwarg)}


class IncomesListByDate(generics.ListAPIView):
    serializer_class = IncomesByDatesSerializer
    lookup_url_kwarg = 'balance_id'
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = IncomesFilter

    def get_queryset(self):
        balance_id = self.kwargs.get(self.lookup_url_kwarg)
        incomes = Balance.objects.get(id=balance_id).incomes.values(
                'category__name').annotate(amount_per_category=Sum('amount'))
        return incomes

    def get_serializer_context(self):
        return {"balance_id": self.kwargs.get(self.lookup_url_kwarg)}


class ExpensesList(generics.ListCreateAPIView):
    serializer_class = ExpenseSerializer
    lookup_url_kwarg = 'balance_id'

    def get_queryset(self):
        balance_id = self.kwargs.get(self.lookup_url_kwarg)
        expenses = Balance.objects.get(id=balance_id).expenses.all()
        return expenses

    def get_serializer_context(self):
        return {"balance_id": self.kwargs.get(self.lookup_url_kwarg)}


class ExpensesListByDate(generics.ListAPIView):
    serializer_class = ExpensesByDatesSerializer
    lookup_url_kwarg = 'balance_id'
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = ExpensesFilter

    def get_queryset(self):
        balance_id = self.kwargs.get(self.lookup_url_kwarg)
        expenses = Balance.objects.get(id=balance_id).expenses.values(
                'category__name').annotate(amount_per_category=Sum('amount'))
        return expenses

    def get_serializer_context(self):
        return {"balance_id": self.kwargs.get(self.lookup_url_kwarg)}
