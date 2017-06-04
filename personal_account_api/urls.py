from django.conf.urls import url

from .views import BalanceList, BalanceDetail, IncomesList, ExpensesList, \
        SavingsGoalList, BudgetList, ExpensesListByDate, IncomesListByDate

urlpatterns = [
        url(r'^balance/all/$', BalanceList.as_view()),
        url(r'^balance/detail/$', BalanceDetail.as_view()),
        url(r'^balance/incomes/$', IncomesList.as_view()),
        url(r'^balance/expenses/$', ExpensesList.as_view()),
        url(r'^balance/savings-goals/$', SavingsGoalList.as_view()),
        url(r'^balance/budget/$', BudgetList.as_view()),
        url(r'^balance/expenses-by-date/$', ExpensesListByDate.as_view()),
        url(r'^balance/incomes-by-date/$', IncomesListByDate.as_view()),
        ]
