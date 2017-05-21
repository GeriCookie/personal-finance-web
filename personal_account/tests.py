from django.test import TestCase
from personal_account.models import Income, Expense, Balance


class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_only_saves_items_when_necessary(self):
        self.client.get('/')
        self.assertEqual(Income.objects.count(), 0)
        self.assertEqual(Expense.objects.count(), 0)


class BalanceIncomeAndExpensesModelTest(TestCase):

    def test_saving_and_retrieving_incomes(self):
        balance = Balance()
        balance.save()
        first_income = Income()
        first_income.category = 'Salary'
        first_income.amount = 1000
        first_income.balance = balance
        first_income.save()

        second_income = Income()
        second_income.category = 'Bonus'
        second_income.amount = 2000
        second_income.balance = balance
        second_income.save()

        saved_balance = Balance.objects.first()
        self.assertEqual(saved_balance, balance)

        saved_incomes = Income.objects.all()
        self.assertEqual(saved_incomes.count(), 2)

        first_saved_income = saved_incomes[0]
        second_saved_income = saved_incomes[1]
        self.assertEqual(first_saved_income.category, 'Salary')
        self.assertEqual(first_saved_income.amount, 1000)
        self.assertEqual(first_saved_income.balance, balance)
        self.assertEqual(second_saved_income.category, 'Bonus')
        self.assertEqual(second_saved_income.amount, 2000)
        self.assertEqual(second_saved_income.balance, balance)

    def test_saving_and_retrieving_expenses(self):
        balance = Balance()
        balance.save()

        first_expense = Expense()
        first_expense.category = 'Salary'
        first_expense.amount = 1000
        first_expense.balance = balance
        first_expense.save()

        second_expense = Expense()
        second_expense.category = 'Bonus'
        second_expense.amount = 2000
        second_expense.balance = balance
        second_expense.save()

        saved_balance = Balance.objects.first()
        self.assertEqual(saved_balance, balance)
        saved_expenses = Expense.objects.all()
        self.assertEqual(saved_expenses.count(), 2)

        first_saved_expense = saved_expenses[0]
        second_saved_expense = saved_expenses[1]
        self.assertEqual(first_saved_expense.category, 'Salary')
        self.assertEqual(first_saved_expense.amount, 1000)
        self.assertEqual(first_saved_expense.balance, balance)
        self.assertEqual(second_saved_expense.category, 'Bonus')
        self.assertEqual(second_saved_expense.amount, 2000)
        self.assertEqual(second_saved_expense.balance, balance)


class BalanceViewTest(TestCase):

    def test_uses_balance_template(self):
        balance = Balance.objects.create()
        response = self.client.get(
                f'/balance/{balance.id}/'
                )
        self.assertTemplateUsed(response, 'balance.html')

    def test_displays_only_items_for_that_balance(self):
        correct_balance = Balance.objects.create()
        Expense.objects.create(
                category='Food',
                amount=10,
                balance=correct_balance
                )
        Expense.objects.create(
                category='Movie',
                amount=20,
                balance=correct_balance
                )

        other_balance = Balance.objects.create()
        Expense.objects.create(
                category='Water',
                amount=3,
                balance=other_balance
                )
        Expense.objects.create(
                category='School',
                amount=10,
                balance=other_balance
                )

        response = self.client.get(
                f'/balance/{correct_balance.id}/'
                )

        self.assertContains(response, 'Food: 10')
        self.assertContains(response, 'Movie: 20')
        self.assertNotContains(response, 'Water: 3')
        self.assertNotContains(response, 'School: 10')

    def test_balance_values_are_calculated_right(self):
        balance = Balance()
        balance.save()
        first_income = Income()
        first_income.category = 'Salary'
        first_income.amount = 1000
        first_income.balance = balance
        first_income.save()
        balance.save(income_added=True)

        second_income = Income()
        second_income.category = 'Bonus'
        second_income.amount = 2000
        second_income.balance = balance
        second_income.save()
        balance.save(income_added=True)

        saved_balance = Balance.objects.first()
        self.assertEqual(saved_balance, balance)

        saved_incomes = Income.objects.all()
        self.assertEqual(saved_incomes.count(), 2)

        first_saved_income = saved_incomes[0]
        second_saved_income = saved_incomes[1]
        self.assertEqual(first_saved_income.category, 'Salary')
        self.assertEqual(first_saved_income.amount, 1000)
        self.assertEqual(first_saved_income.balance, balance)
        self.assertEqual(second_saved_income.category, 'Bonus')
        self.assertEqual(second_saved_income.amount, 2000)
        self.assertEqual(second_saved_income.balance, balance)
        self.assertEqual(saved_balance.total_income, 3000)
        self.assertEqual(saved_balance.total_amount, 3000)

        first_expense = Expense()
        first_expense.category = 'Food'
        first_expense.amount = 100
        first_expense.balance = balance
        first_expense.save()
        balance.save(expense_added=True)

        second_expense = Expense()
        second_expense.category = 'Present'
        second_expense.amount = 200
        second_expense.balance = balance
        second_expense.save()
        balance.save(expense_added=True)

        saved_balance = Balance.objects.first()
        self.assertEqual(saved_balance, balance)
        saved_expenses = Expense.objects.all()
        self.assertEqual(saved_expenses.count(), 2)

        first_saved_expense = saved_expenses[0]
        second_saved_expense = saved_expenses[1]
        self.assertEqual(first_saved_expense.category, 'Food')
        self.assertEqual(first_saved_expense.amount, 100)
        self.assertEqual(first_saved_expense.balance, balance)
        self.assertEqual(second_saved_expense.category, 'Present')
        self.assertEqual(second_saved_expense.amount, 200)
        self.assertEqual(second_saved_expense.balance, balance)
        self.assertEqual(saved_balance.total_income, 3000)
        self.assertEqual(saved_balance.total_expense, 300)
        self.assertEqual(saved_balance.total_amount, 2700)

    def test_passes_correct_balance_to_template(self):
        other_balance = Balance.objects.create()
        correct_balance = Balance.objects.create()
        response = self.client.get(f'/balance/{correct_balance.id}/')
        self.assertEqual(response.context['balance'], correct_balance)
        self.assertNotEqual(response.context['balance'], other_balance)


class NewBalanceTest(TestCase):

    def test_can_save_a_POST_request(self):
        self.client.post('/balance/new',  data={
            'income_category': 'Salary',
            'income_amount': 1000
            })
        self.assertEqual(Income.objects.count(), 1)
        new_income = Income.objects.first()
        self.assertEqual(new_income.category, 'Salary')
        self.assertEqual(new_income.amount, 1000)

    def test_can_save_account_balance_after_a_POST_request(self):
        self.client.post('/balance/new',  data={
             'income_category': 'Salary',
             'income_amount': 1000
             })
        self.assertEqual(Balance.objects.count(), 1)
        new_balance = Balance.objects.first()
        self.assertEqual(new_balance.total_income, 1000.00)
        self.assertEqual(new_balance.total_amount, 1000.00)
        self.assertEqual(new_balance.total_expense, 0.00)

    def test_redirects_after_POST(self):
        response = self.client.post('/balance/new', data={
            'income_category': 'Salary',
            'income_amount': 1000
            })
        self.assertEqual(response.status_code, 302)
        new_balance = Balance.objects.first()
        self.assertRedirects(
                response,
                f'/balance/{new_balance.id}/'
                )


class NewIncomeTest(TestCase):

    def test_can_save_a_income_POST_request_to_an_existing_balance(self):
        other_balance = Balance.objects.create()
        correct_balance = Balance.objects.create()

        self.client.post(
                f'/balance/{correct_balance.id}/add_income',
                data={'income_category': 'Salary', 'income_amount': 1000}
                )

        self.assertEqual(Income.objects.count(), 1)
        new_income = Income.objects.first()
        self.assertEqual(new_income.category, 'Salary')
        self.assertEqual(new_income.amount, 1000.00)
        self.assertEqual(new_income.balance, correct_balance)
        self.assertNotEqual(new_income.balance, other_balance)

    def test_redirects_to_balance_view(self):
        Balance.objects.create()
        correct_balance = Balance.objects.create()

        response = self.client.post(
                f'/balance/{correct_balance.id}/add_income',
                data={'income_category': 'Salary', 'income_amount': 500.00}
                )

        self.assertRedirects(
                response,
                f'/balance/{correct_balance.id}/'
        )


class NewExpenseTest(TestCase):

    def test_can_save_a_expense_POST_request_to_an_existing_balance(self):
        other_balance = Balance.objects.create()
        correct_balance = Balance.objects.create()

        self.client.post(
                f'/balance/{correct_balance.id}/add_expense',
                data={'expense_category': 'Food', 'expense_amount': 10}
                )

        self.assertEqual(Expense.objects.count(), 1)
        new_expense = Expense.objects.first()
        self.assertEqual(new_expense.category, 'Food')
        self.assertEqual(new_expense.amount, 10.00)
        self.assertEqual(new_expense.balance, correct_balance)
        self.assertNotEqual(new_expense.balance, other_balance)

    def test_redirects_to_balance_view(self):
        Balance.objects.create()
        correct_balance = Balance.objects.create()

        response = self.client.post(
                f'/balance/{correct_balance.id}/add_expense',
                data={'expense_category': 'Food', 'expense_amount': 10.00}
                )

        self.assertRedirects(
                response,
                f'/balance/{correct_balance.id}/'
        )
