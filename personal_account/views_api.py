from personal_account.models import Balance, Income, Expense, Category
from personal_account.serializers import BalanceSerializer, IncomeSerializer, \
                                        ExpenseSerializer, CategorySerializer
from rest_framework import generics


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
