from django.test import TestCase
from personal_account.models import Income, Expense, Balance
from datetime import datetime, date, timedelta
from calendar import monthrange


class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_only_saves_items_when_necessary(self):
        self.client.get('/')
        self.assertEqual(Income.objects.count(), 0)


class BalanceIncomeAndExpensesModelTest(TestCase):

    def test_saving_and_retrieving_incomes(self):
        balance = Balance()
        balance.save()
        Income.objects.create(
                category='Salary',
                amount=1000,
                date=datetime.strptime('05/24/2017', '%m/%d/%Y'),
                balance=balance
                )
        balance.save(income_added=True)
        Income.objects.create(
                category='Bonus',
                amount=2000,
                date=datetime.strptime('05/24/2017', '%m/%d/%Y'),
                balance=balance
                )
        balance.save(income_added=True)
        saved_balance = Balance.objects.first()
        self.assertEqual(saved_balance, balance)

        saved_incomes = Income.objects.all()
        self.assertEqual(saved_incomes.count(), 2)

        first_saved_income = saved_incomes[0]
        second_saved_income = saved_incomes[1]
        self.assertEqual(first_saved_income.category, 'Salary')
        self.assertEqual(first_saved_income.amount, 1000)
        self.assertEqual(
                    first_saved_income.date,
                    date(2017, 5, 24)
        )
        self.assertEqual(first_saved_income.balance, balance)
        self.assertEqual(second_saved_income.category, 'Bonus')
        self.assertEqual(second_saved_income.amount, 2000)
        print(second_saved_income.date)
        self.assertEqual(
                second_saved_income.date,
                date(2017, 5, 24)
        )
        self.assertEqual(second_saved_income.balance, balance)

    def test_saving_and_retrieving_expenses(self):
        balance = Balance()
        balance.save()

        Expense.objects.create(
                category='Food',
                amount=10,
                date=datetime.strptime('05/24/2017', '%m/%d/%Y'),
                balance=balance
                )
        balance.save(expense_added=True)
        Expense.objects.create(
                category='Movie',
                amount=20,
                date=datetime.strptime('05/24/2017', '%m/%d/%Y'),
                balance=balance
                )
        balance.save(expense_added=True)
        saved_balance = Balance.objects.first()
        self.assertEqual(saved_balance, balance)
        saved_expenses = Expense.objects.all()
        self.assertEqual(saved_expenses.count(), 2)

        first_saved_expense = saved_expenses[0]
        second_saved_expense = saved_expenses[1]
        self.assertEqual(first_saved_expense.category, 'Food')
        self.assertEqual(first_saved_expense.amount, 10)
        print(first_saved_expense.date)
        self.assertEqual(
                    first_saved_expense.date,
                    date(2017, 5, 24)
        )
        self.assertEqual(first_saved_expense.balance, balance)
        self.assertEqual(second_saved_expense.category, 'Movie')
        self.assertEqual(second_saved_expense.amount, 20)
        self.assertEqual(
                second_saved_expense.date,
                date(2017, 5, 24)
        )
        self.assertEqual(second_saved_expense.balance, balance)


class BalanceViewTest(TestCase):

    def test_uses_balance_template(self):
        balance = Balance.objects.create()
        response = self.client.get(
                f'/balance/{balance.id}/'
                )
        self.assertTemplateUsed(response, 'balance.html')

    def test_displays_only_expenses_for_that_balance(self):
        correct_balance = Balance.objects.create()
        Expense.objects.create(
                category='Food',
                amount=10,
                date=datetime.strptime('05/24/2017', '%m/%d/%Y'),
                balance=correct_balance
                )
        correct_balance.save(expense_added=True)
        Expense.objects.create(
                category='Movie',
                amount=20,
                date=datetime.strptime('05/24/2017', '%m/%d/%Y'),
                balance=correct_balance
                )
        correct_balance.save(expense_added=True)
        other_balance = Balance.objects.create()
        Expense.objects.create(
                category='Water',
                amount=3,
                date=datetime.strptime('05/24/2017', '%m/%d/%Y'),
                balance=other_balance
                )
        other_balance.save(expense_added=True)
        Expense.objects.create(
                category='School',
                amount=10,
                date=datetime.strptime('05/24/2017', '%m/%d/%Y'),
                balance=other_balance
                )
        other_balance.save(expense_added=True)

        response = self.client.get(
                f'/balance/{correct_balance.id}/expenses/'
                )

        self.assertContains(response, '24 May 2017 || Food: 10')
        self.assertContains(response, '24 May 2017 || Movie: 20')
        self.assertNotContains(response, '24 May 2017 || Water: 3')
        self.assertNotContains(response, '24 May 2017 || School: 10')

    def test_balance_values_are_calculated_right(self):
        balance = Balance()
        balance.save()
        Income.objects.create(
                category='Salary',
                amount=1000,
                date=datetime.strptime('05/24/2017', '%m/%d/%Y'),
                balance=balance
                )
        balance.save(income_added=True)
        Income.objects.create(
                category='Bonus',
                amount=2000,
                date=datetime.strptime('05/24/2017', '%m/%d/%Y'),
                balance=balance
                )
        balance.save(income_added=True)

        saved_balance = Balance.objects.first()
        self.assertEqual(saved_balance, balance)

        self.assertEqual(saved_balance.total_income, 3000)
        self.assertEqual(saved_balance.total_amount, 3000)

        Expense.objects.create(
                category='Food',
                amount=100,
                date=datetime.strptime('05/24/2017', '%m/%d/%Y'),
                balance=balance
                )
        balance.save(expense_added=True)
        Expense.objects.create(
                category='Present',
                amount=200,
                date=datetime.strptime('05/24/2017', '%m/%d/%Y'),
                balance=balance
                )
        balance.save(expense_added=True)

        saved_balance = Balance.objects.first()
        self.assertEqual(saved_balance, balance)
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
            'income_amount': 1000,
            'income_date': '05/24/2017'
            })
        self.assertEqual(Income.objects.count(), 1)
        new_income = Income.objects.first()
        self.assertEqual(new_income.category, 'Salary')
        self.assertEqual(new_income.amount, 1000)
        self.assertEqual(new_income.date, date(2017, 5, 24))

    def test_can_save_account_balance_after_a_POST_request(self):
        self.client.post('/balance/new',  data={
            'income_category': 'Salary',
            'income_amount': 1000,
            'income_date': '05/24/2017'
            })
        self.assertEqual(Balance.objects.count(), 1)
        new_balance = Balance.objects.first()
        self.assertEqual(new_balance.total_income, 1000.00)
        self.assertEqual(new_balance.total_amount, 1000.00)
        self.assertEqual(new_balance.total_expense, 0.00)

    def test_redirects_after_POST(self):
        response = self.client.post('/balance/new', data={
            'income_category': 'Salary',
            'income_amount': 1000,
            'income_date': '05/24/2017'
            })
        self.assertEqual(response.status_code, 302)
        new_balance = Balance.objects.first()
        self.assertRedirects(
                response,
                f'/balance/{new_balance.id}/income/'
                )


class NewIncomeTest(TestCase):

    def test_can_save_a_income_POST_request_to_an_existing_balance(self):
        other_balance = Balance.objects.create()
        correct_balance = Balance.objects.create()

        self.client.post(
                f'/balance/{correct_balance.id}/income/',
                data={
                    'income_category': 'Salary',
                    'income_amount': 1000,
                    'income_date': '05/24/2017'
                }
            )

        self.assertEqual(Income.objects.count(), 1)
        new_income = Income.objects.first()
        self.assertEqual(new_income.category, 'Salary')
        self.assertEqual(new_income.amount, 1000.00)
        self.assertEqual(new_income.date, date(2017, 5, 24))
        self.assertEqual(new_income.balance, correct_balance)
        self.assertNotEqual(new_income.balance, other_balance)

    def test_redirects_to_balance_view(self):
        Balance.objects.create()
        correct_balance = Balance.objects.create()

        response = self.client.post(
                f'/balance/{correct_balance.id}/income/',
                data={
                    'income_category': 'Salary',
                    'income_amount': 500.00,
                    'income_date': '05/24/2017'
                }
            )

        self.assertRedirects(
                response,
                f'/balance/{correct_balance.id}/income/'
                )


class IncomesByDayView(TestCase):

    def test_incomes_daily_view(self):
        balance = Balance.objects.create()
        Income.objects.create(
                category='Food',
                amount=10,
                date=datetime.today(),
                balance=balance
                )
        balance.save(income_added=True)
        Income.objects.create(
                category='Movie',
                amount=20,
                date=datetime.today(),
                balance=balance
                )
        balance.save(income_added=True)
        Income.objects.create(
                category='Water',
                amount=3,
                date=datetime.today(),
                balance=balance
                )
        balance.save(income_added=True)
        Income.objects.create(
                category='School',
                amount=10,
                date=datetime.today(),
                balance=balance
                )
        balance.save(income_added=True)
        today_str = datetime.strftime(datetime.today(), '%Y-%m-%d')
        response = self.client.get(
                f'/balance/{balance.id}/income/{today_str}/'
                )
        today_str_view = datetime.strftime(datetime.today(), '%d %b %Y')
        self.assertContains(response, f'{today_str_view} || Food: 10')
        self.assertContains(response, f'{today_str_view} || Movie: 20')
        self.assertContains(response, f'{today_str_view} || Water: 3')
        self.assertContains(response, f'{today_str_view} || School: 10')

    def test_incomes_weekly_view(self):
        balance = Balance.objects.create()
        prev_week_day = datetime.today() - timedelta(days=7)
        Income.objects.create(
                category='Food',
                amount=10,
                date=prev_week_day,
                balance=balance
                )
        balance.save(income_added=True)
        Income.objects.create(
                category='Movie',
                amount=20,
                date=prev_week_day,
                balance=balance
                )
        balance.save(income_added=True)
        Income.objects.create(
                category='Water',
                amount=3,
                date=prev_week_day,
                balance=balance
                )
        balance.save(income_added=True)
        Income.objects.create(
                category='School',
                amount=10,
                date=prev_week_day,
                balance=balance
                )
        balance.save(income_added=True)
        start_week = prev_week_day - timedelta(days=prev_week_day.weekday())
        end_week = start_week + timedelta(days=6)
        start_week_str = datetime.strftime(start_week, '%Y-%m-%d')
        end_week_str = datetime.strftime(end_week, '%Y-%m-%d')
        response = self.client.get(
            f'/balance/{balance.id}/income/{start_week_str}/{end_week_str}/'
                )
        prev_week_day_str_view = datetime.strftime(prev_week_day, '%d %b %Y')
        self.assertContains(response, f'{prev_week_day_str_view} || Food: 10')
        self.assertContains(response, f'{prev_week_day_str_view} || Movie: 20')
        self.assertContains(response, f'{prev_week_day_str_view} || Water: 3')
        self.assertContains(
                response, f'{prev_week_day_str_view} || School: 10')

    def test_income_monthly_view(self):
        balance = Balance.objects.create()
        prev_month_day = datetime.today() - timedelta(days=30)
        Income.objects.create(
                category='Food',
                amount=10,
                date=prev_month_day,
                balance=balance
                )
        balance.save(income_added=True)
        Income.objects.create(
                category='Movie',
                amount=20,
                date=prev_month_day,
                balance=balance
                )
        balance.save(income_added=True)
        Income.objects.create(
                category='Water',
                amount=3,
                date=prev_month_day,
                balance=balance
                )
        balance.save(income_added=True)
        Income.objects.create(
                category='School',
                amount=10,
                date=prev_month_day,
                balance=balance
                )
        balance.save(income_added=True)
        monthdays = monthrange(
                prev_month_day.year, prev_month_day.month)
        start_month_date = date(
                prev_month_day.year, prev_month_day.month, 1)
        start_prev_m = datetime.strftime(start_month_date, '%Y-%m-%d')
        end_month_date = date(
                prev_month_day.year, prev_month_day.month, monthdays[1])
        end_prev_m = datetime.strftime(end_month_date, '%Y-%m-%d')
        response = self.client.get(
            f'/balance/{balance.id}/income/m/{start_prev_m}/{end_prev_m}/'
                )
        prev_month_day_str_view = datetime.strftime(prev_month_day, '%d %b %Y')
        self.assertContains(response, f'{prev_month_day_str_view} || Food: 10')
        self.assertContains(
                response, f'{prev_month_day_str_view} || Movie: 20')
        self.assertContains(response, f'{prev_month_day_str_view} || Water: 3')
        self.assertContains(
                response, f'{prev_month_day_str_view} || School: 10')


class NewExpenseTest(TestCase):

    def test_can_save_a_expense_POST_request_to_an_existing_balance(self):
        other_balance = Balance.objects.create()
        correct_balance = Balance.objects.create()

        self.client.post(
                f'/balance/{correct_balance.id}/expenses/',
                data={
                    'expense_category': 'Food',
                    'expense_amount': 10,
                    'expense_date': '05/24/2017'
                }
            )

        self.assertEqual(Expense.objects.count(), 1)
        new_expense = Expense.objects.first()
        self.assertEqual(new_expense.category, 'Food')
        self.assertEqual(new_expense.amount, 10.00)
        self.assertEqual(
                new_expense.date,
                date(2017, 5, 24)
        )
        self.assertEqual(new_expense.balance, correct_balance)
        self.assertNotEqual(new_expense.balance, other_balance)

    def test_redirects_to_balance_view(self):
        Balance.objects.create()
        correct_balance = Balance.objects.create()

        response = self.client.post(
                f'/balance/{correct_balance.id}/expenses/',
                data={
                    'expense_category': 'Food',
                    'expense_amount': 10.00,
                    'expense_date': '05/24/2017'
                }
            )

        self.assertRedirects(
                response,
                f'/balance/{correct_balance.id}/expenses/'
                )


class ExpensesByDayView(TestCase):

    def test_expenses_daily_view(self):
        correct_balance = Balance.objects.create()
        Expense.objects.create(
                category='Food',
                amount=10,
                date=datetime.today(),
                balance=correct_balance
                )
        correct_balance.save(expense_added=True)
        Expense.objects.create(
                category='Movie',
                amount=20,
                date=datetime.today(),
                balance=correct_balance
                )
        correct_balance.save(expense_added=True)
        Expense.objects.create(
                category='Water',
                amount=3,
                date=datetime.today(),
                balance=correct_balance
                )
        correct_balance.save(expense_added=True)
        Expense.objects.create(
                category='School',
                amount=10,
                date=datetime.today(),
                balance=correct_balance
                )
        correct_balance.save(expense_added=True)
        today_str = datetime.strftime(datetime.today(), '%Y-%m-%d')
        response = self.client.get(
                f'/balance/{correct_balance.id}/expenses/{today_str}/'
                )
        today_str_view = datetime.strftime(datetime.today(), '%d %b %Y')
        self.assertContains(response, f'{today_str_view} || Food: 10')
        self.assertContains(response, f'{today_str_view} || Movie: 20')
        self.assertContains(response, f'{today_str_view} || Water: 3')
        self.assertContains(response, f'{today_str_view} || School: 10')

    def test_expenses_weekly_view(self):
        balance = Balance.objects.create()
        prev_week_day = datetime.today() - timedelta(days=7)
        Expense.objects.create(
                category='Food',
                amount=10,
                date=prev_week_day,
                balance=balance
                )
        balance.save(expense_added=True)
        Expense.objects.create(
                category='Movie',
                amount=20,
                date=prev_week_day,
                balance=balance
                )
        balance.save(expense_added=True)
        Expense.objects.create(
                category='Water',
                amount=3,
                date=prev_week_day,
                balance=balance
                )
        balance.save(expense_added=True)
        Expense.objects.create(
                category='School',
                amount=10,
                date=prev_week_day,
                balance=balance
                )
        balance.save(expense_added=True)
        start_week = prev_week_day - timedelta(days=prev_week_day.weekday())
        end_week = start_week + timedelta(days=6)
        start_week_str = datetime.strftime(start_week, '%Y-%m-%d')
        end_week_str = datetime.strftime(end_week, '%Y-%m-%d')
        response = self.client.get(
            f'/balance/{balance.id}/expenses/{start_week_str}/{end_week_str}/'
                )
        prev_week_day_str_view = datetime.strftime(prev_week_day, '%d %b %Y')
        self.assertContains(response, f'{prev_week_day_str_view} || Food: 10')
        self.assertContains(response, f'{prev_week_day_str_view} || Movie: 20')
        self.assertContains(response, f'{prev_week_day_str_view} || Water: 3')
        self.assertContains(
                response, f'{prev_week_day_str_view} || School: 10')

    def test_expenses_monthly_view(self):
        balance = Balance.objects.create()
        prev_month_day = datetime.today() - timedelta(days=30)
        Expense.objects.create(
                category='Food',
                amount=10,
                date=prev_month_day,
                balance=balance
                )
        balance.save(expense_added=True)
        Expense.objects.create(
                category='Movie',
                amount=20,
                date=prev_month_day,
                balance=balance
                )
        balance.save(expense_added=True)
        Expense.objects.create(
                category='Water',
                amount=3,
                date=prev_month_day,
                balance=balance
                )
        balance.save(expense_added=True)
        Expense.objects.create(
                category='School',
                amount=10,
                date=prev_month_day,
                balance=balance
                )
        balance.save(expense_added=True)
        monthdays = monthrange(
                prev_month_day.year, prev_month_day.month)
        start_month_date = date(
                prev_month_day.year, prev_month_day.month, 1)
        start_prev_m = datetime.strftime(start_month_date, '%Y-%m-%d')
        end_month_date = date(
                prev_month_day.year, prev_month_day.month, monthdays[1])
        end_prev_m = datetime.strftime(end_month_date, '%Y-%m-%d')
        response = self.client.get(
            f'/balance/{balance.id}/expenses/m/{start_prev_m}/{end_prev_m}/'
                )
        prev_month_day_str_view = datetime.strftime(prev_month_day, '%d %b %Y')
        self.assertContains(response, f'{prev_month_day_str_view} || Food: 10')
        self.assertContains(
                response, f'{prev_month_day_str_view} || Movie: 20')
        self.assertContains(response, f'{prev_month_day_str_view} || Water: 3')
        self.assertContains(
                response, f'{prev_month_day_str_view} || School: 10')

    def test_expenses_yearly_view(self):
        balance = Balance.objects.create()
        prev_year_day = datetime.today() - timedelta(days=365)
        Expense.objects.create(
                category='Food',
                amount=10,
                date=prev_year_day,
                balance=balance
                )
        balance.save(expense_added=True)
        Expense.objects.create(
                category='Movie',
                amount=20,
                date=prev_year_day,
                balance=balance
                )
        balance.save(expense_added=True)
        Expense.objects.create(
                category='Water',
                amount=3,
                date=prev_year_day,
                balance=balance
                )
        balance.save(expense_added=True)
        Expense.objects.create(
                category='School',
                amount=10,
                date=prev_year_day,
                balance=balance
                )
        balance.save(expense_added=True)
        start_year_date = date(
                prev_year_day.year, 1, 1)
        start_prev_y = datetime.strftime(start_year_date, '%Y-%m-%d')
        end_year_date = date(
                prev_year_day.year, 12, 31)
        end_prev_y = datetime.strftime(end_year_date, '%Y-%m-%d')
        response = self.client.get(
            f'/balance/{balance.id}/expenses/y/{start_prev_y}/{end_prev_y}/'
                )
        prev_year_day_str_view = datetime.strftime(prev_year_day, '%d %b %Y')
        self.assertContains(response, f'{prev_year_day_str_view} || Food: 10')
        self.assertContains(
                response, f'{prev_year_day_str_view} || Movie: 20')
        self.assertContains(response, f'{prev_year_day_str_view} || Water: 3')
        self.assertContains(
                response, f'{prev_year_day_str_view} || School: 10')
