from django.test import TestCase
from personal_account.models import Income, Expense


class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_can_save_a_POST_request(self):
        self.client.post('/',  data={
            'income_category': 'Salary',
            'income_amount': 1000
            })
        self.assertEqual(Income.objects.count(), 1)
        new_income = Income.objects.first()
        self.assertEqual(new_income.category, 'Salary')
        self.assertEqual(new_income.amount, 1000)

    def test_can_save_expense_POST_request(self):
        self.client.post('/', data={
            'expense_category': 'Food',
            'expense_amount': 10
            })
        self.assertEqual(Expense.objects.count(), 1)
        new_expense = Expense.objects.first()
        self.assertEqual(new_expense.category, 'Food')
        self.assertEqual(new_expense.amount, 10)

    # def test_can_save_account_balance_after_a_POST_request(self):
    #     self.client.post('/',  data={
    #         'income_category': 'Salary',
    #         'income_amount': 1000
    #         })
    #     self.assertEqual(Balance.objects.count(), 1)
    #     new_balance = Balance.objects.first()
    #     self.assertEqual(new_balance.total_income, 1000.00)
    #     self.assertEqual(new_balance.total_amount, 1000.00)
    #     self.assertEqual(new_balance.total_expenses, 0.00)

    def test_redirects_after_POST(self):
        response = self.client.post('/', data={
            'income_category': 'Salary',
            'income_amount': 1000
            })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
                response['location'],
                '/personal_account/the-only-balance-in-the-world/'
        )

    def test_only_saves_items_when_necessary(self):
        self.client.get('/')
        self.assertEqual(Income.objects.count(), 0)
        self.assertEqual(Expense.objects.count(), 0)


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


class BalanceViewTest(TestCase):

    def test_uses_balance_template(self):
        response = self.client.get(
                '/personal_account/the-only-balance-in-the-world/'
                )
        self.assertTemplateUsed(response, 'balance.html')

    def test_displays_all_items(self):
        Expense.objects.create(category='Food', amount=10)
        Expense.objects.create(category='Movie', amount=20)

        response = self.client.get(
                            '/personal_account/the-only-balance-in-the-world/'
                            )

        self.assertContains(response, 'Food: 10')
        self.assertContains(response, 'Movie: 20')
