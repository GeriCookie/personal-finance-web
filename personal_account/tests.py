from django.test import TestCase
from personal_account.models import Income, Expense


class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_can_save_a_POST_request(self):
        response_income = self.client.post('/',  data={
                    'income_category': 'Salary',
                    'income_amount': 1000
                })
        self.assertIn('Salary: 1000', response_income.content.decode())
        self.assertTemplateUsed(response_income, 'home.html')


class IncomeModelTest(TestCase):

    def test_saving_and_retrieving_incomes(self):
        first_income = Income()
        first_income.category = 'Salary'
        first_income.amount = 1000
        first_income.save()

        second_income = Income()
        second_income.category = 'Bonus'
        second_income.amount = 2000
        second_income.save()

        saved_incomes = Income.objects.all()
        self.assertEqual(saved_incomes.count(), 2)

        first_saved_income = saved_incomes[0]
        second_saved_income = saved_incomes[1]
        self.assertEqual(first_saved_income.category, 'Salary')
        self.assertEqual(first_saved_income.amount, 1000)
        self.assertEqual(second_saved_income.category, 'Bonus')
        self.assertEqual(second_saved_income.amount, 2000)

    def test_saving_and_retrieving_expenses(self):
        first_expense = Expense()
        first_expense.category = 'Salary'
        first_expense.amount = 1000
        first_expense.save()

        second_expense = Expense()
        second_expense.category = 'Bonus'
        second_expense.amount = 2000
        second_expense.save()

        saved_expenses = Expense.objects.all()
        self.assertEqual(saved_expenses.count(), 2)

        first_saved_expense = saved_expenses[0]
        second_saved_expense = saved_expenses[1]
        self.assertEqual(first_saved_expense.category, 'Salary')
        self.assertEqual(first_saved_expense.amount, 1000)
        self.assertEqual(second_saved_expense.category, 'Bonus')
        self.assertEqual(second_saved_expense.amount, 2000)
