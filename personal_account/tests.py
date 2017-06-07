from django.test import TestCase, TransactionTestCase
from datetime import datetime, date, timedelta
from calendar import monthrange

from django.contrib.auth import get_user_model
import uuid
from models.models import Balance, Income, Expense, Category


class BaseTestCase(TransactionTestCase):

    def init_force_login(self):
        User = get_user_model()
        random_user = self.get_random_user()
        self.user = User.objects.create_user(username=random_user['username'],
                password=random_user['password'])

        self.client.force_login(self.user)        

    def get_random_user(self):
        username = 'user-%s' % uuid.uuid4().__str__().replace('-', '')
        # username = 'user-%d' % self.users_count
        password = '123456qw'
        return {
            'username': username,
            'password': password,
        }

    def setUp(self):
        self.init_force_login()

    def tearDown(self):
        self.client.logout()


class HomePageTest(BaseTestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_only_saves_items_when_necessary(self):
        self.client.get('/balance/income/')
        self.assertEqual(Income.objects.count(), 0)


class BalanceIncomeAndExpensesModelTest(BaseTestCase):

    def test_saving_and_retrieving_incomes(self):
        balance = Balance.objects.get(owner=self.user)
        category = Category.objects.create_category('Salary')
        Balance.objects.create_income(
                category=category,
                amount=1000,
                date='05/24/2017',
                balance=balance
                )
        category = Category.objects.create_category('Bonus')
        Balance.objects.create_income(
                category=category,
                amount=2000,
                date='05/24/2017',
                balance=balance
                )
        saved_balance = Balance.objects.first()
        self.assertEqual(saved_balance, balance)

        saved_incomes = Income.objects.all()
        self.assertEqual(saved_incomes.count(), 2)

        first_saved_income = saved_incomes[0]
        second_saved_income = saved_incomes[1]
        self.assertEqual(first_saved_income.category.name, 'Salary')
        self.assertEqual(first_saved_income.amount, 1000)
        self.assertEqual(
                    first_saved_income.date,
                    date(2017, 5, 24)
        )
        self.assertEqual(first_saved_income.balance, balance)
        self.assertEqual(second_saved_income.category.name, 'Bonus')
        self.assertEqual(second_saved_income.amount, 2000)
        self.assertEqual(
                second_saved_income.date,
                date(2017, 5, 24)
        )
        self.assertEqual(second_saved_income.balance, balance)

    def test_saving_and_retrieving_expenses(self):
        balance = Balance.objects.get(owner=self.user)
        category = Category.objects.create_category('Food')
        Balance.objects.create_expense(
                category=category,
                amount=10,
                date='05/24/2017',
                balance=balance
                )
        category = Category.objects.create_category('Movie')
        Balance.objects.create_expense(
                category=category,
                amount=20,
                date='05/24/2017',
                balance=balance
                )
        saved_balance = Balance.objects.first()
        self.assertEqual(saved_balance, balance)
        saved_expenses = Expense.objects.all()
        self.assertEqual(saved_expenses.count(), 2)

        first_saved_expense = saved_expenses[0]
        second_saved_expense = saved_expenses[1]
        self.assertEqual(first_saved_expense.category.name, 'Food')
        self.assertEqual(first_saved_expense.amount, 10)
        self.assertEqual(
                    first_saved_expense.date,
                    date(2017, 5, 24)
        )
        self.assertEqual(first_saved_expense.balance, balance)
        self.assertEqual(second_saved_expense.category.name, 'Movie')
        self.assertEqual(second_saved_expense.amount, 20)
        self.assertEqual(
                second_saved_expense.date,
                date(2017, 5, 24)
        )
        self.assertEqual(second_saved_expense.balance, balance)


class BalanceViewTest(BaseTestCase):

    def test_uses_balance_template(self):
        balance = Balance.objects.get(owner=self.user)
        response = self.client.get(
                f'/balance/'
                )
        self.assertTemplateUsed(response, 'balance.html')


    def test_balance_values_are_calculated_right(self):
        balance = Balance.objects.get(owner=self.user)
        category = Category.objects.create_category('Salary')
        Balance.objects.create_income(
                category=category,
                amount=1000,
                date='05/24/2017',
                balance=balance
                )
        category = Category.objects.create_category('Bonus')
        Balance.objects.create_income(
                category=category,
                amount=2000,
                date='05/24/2017',
                balance=balance
                )

        saved_balance = Balance.objects.first()
        self.assertEqual(saved_balance, balance)

        self.assertEqual(saved_balance.total_income, 3000)
        self.assertEqual(saved_balance.total_amount, 3000)

        category = Category.objects.create_category('Food')
        Balance.objects.create_expense(
                category=category,
                amount=100,
                date='05/24/2017',
                balance=balance
                )
        category = Category.objects.create_category('Present')
        Balance.objects.create_expense(
                category=category,
                amount=200,
                date='05/24/2017',
                balance=balance
                )

        saved_balance = Balance.objects.first()
        self.assertEqual(saved_balance, balance)
        self.assertEqual(saved_balance.total_income, 3000)
        self.assertEqual(saved_balance.total_expense, 300)
        self.assertEqual(saved_balance.total_amount, 2700)

    def test_passes_correct_balance_to_template(self):
        correct_balance = Balance.objects.get(owner=self.user)
        response = self.client.get(f'/balance/')
        self.assertEqual(response.context['balance'], correct_balance)


class NewBalanceTest(BaseTestCase):

    def test_can_save_a_POST_request(self):
        self.client.post('/balance/income/',  data={
            'income_category': 'Salary',
            'income_amount': 1000,
            'income_date': '05/24/2017'
            })
        self.assertEqual(Income.objects.count(), 1)
        new_income = Income.objects.first()
        self.assertEqual(new_income.category.name, 'Salary')
        self.assertEqual(new_income.amount, 1000)
        self.assertEqual(new_income.date, date(2017, 5, 24))

    def test_can_save_account_balance_after_a_POST_request(self):
        self.client.post('/balance/income/',  data={
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
        response = self.client.post('/balance/income/', data={
            'income_category': 'Salary',
            'income_amount': 1000,
            'income_date': '05/24/2017'
            })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
                response,
                f'/balance/income/'
                )


class NewIncomeTest(BaseTestCase):

    def test_can_save_a_income_POST_request_to_an_existing_balance(self):
        print(self.user)
        correct_balance = Balance.objects.get(owner=self.user)

        self.client.post(
                f'/balance/income/',
                data={
                    'income_category': 'Salary',
                    'income_amount': 1000,
                    'income_date': '05/24/2017'
                }
            )

        self.assertEqual(Income.objects.count(), 1)
        new_income = Income.objects.first()
        self.assertEqual(new_income.category.name, 'Salary')
        self.assertEqual(new_income.amount, 1000.00)
        self.assertEqual(new_income.date, date(2017, 5, 24))
        self.assertEqual(new_income.balance, correct_balance)


class IncomesByDayView(BaseTestCase):

    def test_incomes_daily_view(self):
        balance = Balance.objects.get(owner=self.user)
        category = Category.objects.create_category('Food')
        Balance.objects.create_income(
                category=category,
                amount=10,
                date=datetime.strftime(datetime.today(), '%m/%d/%Y'),
                balance=balance
                )
        category = Category.objects.create_category('Movie')
        Balance.objects.create_income(
                category=category,
                amount=20,
                date=datetime.strftime(datetime.today(), '%m/%d/%Y'),
                balance=balance
                )
        category = Category.objects.create_category('Water')
        Balance.objects.create_income(
                category=category,
                amount=3,
                date=datetime.strftime(datetime.today(), '%m/%d/%Y'),
                balance=balance
                )
        category = Category.objects.create_category('School')
        Balance.objects.create_income(
                category=category,
                amount=10,
                date=datetime.strftime(datetime.today(), '%m/%d/%Y'),
                balance=balance
                )
        today_str = datetime.strftime(datetime.today(), '%Y-%m-%d')
        response = self.client.get(
                f'/balance/income/{today_str}/'
                )
        self.assertContains(response, '|| Food: 10')
        self.assertContains(response, '|| Movie: 20')
        self.assertContains(response, '|| Water: 3')
        self.assertContains(response, '|| School: 10')

    def test_incomes_weekly_view(self):
        balance = Balance.objects.get(owner=self.user)
        prev_week_day = datetime.today() - timedelta(days=7)
        prev_week_day_str = datetime.strftime(
                datetime.today() - timedelta(days=7), '%m/%d/%Y')
        category = Category.objects.create_category('Food')
        Balance.objects.create_income(
                category=category,
                amount=10,
                date=prev_week_day_str,
                balance=balance
                )
        category = Category.objects.create_category('Movie')
        Balance.objects.create_income(
                category=category,
                amount=20,
                date=prev_week_day_str,
                balance=balance
                )
        category = Category.objects.create_category('Water')
        Balance.objects.create_income(
                category=category,
                amount=3,
                date=prev_week_day_str,
                balance=balance
                )
        category = Category.objects.create_category('School')
        Balance.objects.create_income(
                category=category,
                amount=10,
                date=prev_week_day_str,
                balance=balance
                )
        start_week = prev_week_day - timedelta(days=prev_week_day.weekday())
        end_week = start_week + timedelta(days=6)
        start_week_str = datetime.strftime(start_week, '%Y-%m-%d')
        end_week_str = datetime.strftime(end_week, '%Y-%m-%d')
        response = self.client.get(
            f'/balance/income/{start_week_str}/{end_week_str}/'
                )
        self.assertContains(response, '|| Food: 10')
        self.assertContains(response, '|| Movie: 20')
        self.assertContains(response, '|| Water: 3')
        self.assertContains(
                response, '|| School: 10')

    def test_income_monthly_view(self):
        balance = Balance.objects.get(owner=self.user)
        prev_month_day = datetime.today() - timedelta(days=30)
        prev_month_day_str = datetime.strftime(
                datetime.today() - timedelta(days=30), '%m/%d/%Y')
        category = Category.objects.create_category('Food')
        Balance.objects.create_income(
                category=category,
                amount=10,
                date=prev_month_day_str,
                balance=balance
                )
        category = Category.objects.create_category('Movie')
        Balance.objects.create_income(
                category=category,
                amount=20,
                date=prev_month_day_str,
                balance=balance
                )
        monthdays = monthrange(
                prev_month_day.year, prev_month_day.month)
        start_month_date = date(
                prev_month_day.year, prev_month_day.month, 1)
        start_prev_m = datetime.strftime(start_month_date, '%Y-%m-%d')
        end_month_date = date(
                prev_month_day.year, prev_month_day.month, monthdays[1])
        end_prev_m = datetime.strftime(end_month_date, '%Y-%m-%d')
        response = self.client.get(
            f'/balance/income/m/{start_prev_m}/{end_prev_m}/'
                )
        self.assertContains(response, '|| Food: 10')
        self.assertContains(
                response, '|| Movie: 20')

    def test_income_yearly_view(self):
        balance = Balance.objects.get(owner=self.user)
        prev_year_day = datetime.today() - timedelta(days=365)
        prev_year_day_str = datetime.strftime(
                datetime.today() - timedelta(days=365), '%m/%d/%Y')
        category = Category.objects.create_category('Food')
        Balance.objects.create_income(
                category=category,
                amount=10,
                date=prev_year_day_str,
                balance=balance
                )
        category = Category.objects.create_category('Movie')
        Balance.objects.create_income(
                category=category,
                amount=20,
                date=prev_year_day_str,
                balance=balance
                )
        start_year_date = date(
                prev_year_day.year, 1, 1)
        start_prev_y = datetime.strftime(start_year_date, '%Y-%m-%d')
        end_year_date = date(
                prev_year_day.year, 12, 31)
        end_prev_y = datetime.strftime(end_year_date, '%Y-%m-%d')
        response = self.client.get(
            f'/balance/income/y/{start_prev_y}/{end_prev_y}/'
                )
        self.assertContains(response, '|| Food: 10')
        self.assertContains(
                response, '|| Movie: 20')


class NewExpenseTest(BaseTestCase):

    def test_can_save_a_expense_POST_request_to_an_existing_balance(self):
        correct_balance = Balance.objects.get(owner=self.user)

        self.client.post(
                f'/balance/expenses/',
                data={
                    'expense_category': 'Food',
                    'expense_amount': 10,
                    'expense_date': '05/24/2017'
                }
            )

        self.assertEqual(Expense.objects.count(), 1)
        new_expense = Expense.objects.first()
        self.assertEqual(new_expense.category.name, 'Food')
        self.assertEqual(new_expense.amount, 10.00)
        self.assertEqual(
                new_expense.date,
                date(2017, 5, 24)
        )
        self.assertEqual(new_expense.balance, correct_balance)


class ExpensesByDayView(BaseTestCase):

    def test_expenses_daily_view(self):
        correct_balance = Balance.objects.get(owner=self.user)
        category = Category.objects.create_category('Food')
        Balance.objects.create_expense(
                category=category,
                amount=10,
                date=datetime.strftime(datetime.today(), '%m/%d/%Y'),
                balance=correct_balance
                )
        category = Category.objects.create_category('Movie')
        Balance.objects.create_expense(
                category=category,
                amount=20,
                date=datetime.strftime(datetime.today(), '%m/%d/%Y'),
                balance=correct_balance
                )
        category = Category.objects.create_category('Water')
        Balance.objects.create_expense(
                category=category,
                amount=3,
                date=datetime.strftime(datetime.today(), '%m/%d/%Y'),
                balance=correct_balance
                )
        category = Category.objects.create_category('School')
        Balance.objects.create_expense(
                category=category,
                amount=10,
                date=datetime.strftime(datetime.today(), '%m/%d/%Y'),
                balance=correct_balance
                )
        today_str = datetime.strftime(datetime.today(), '%Y-%m-%d')
        response = self.client.get(
                f'/balance/expenses/{today_str}/'
                )
        self.assertContains(response, '|| Food: 10')
        self.assertContains(response, '|| Movie: 20')
        self.assertContains(response, '|| Water: 3')
        self.assertContains(response, '|| School: 10')

    def test_expenses_weekly_view(self):
        balance = Balance.objects.get(owner=self.user)
        prev_week_day = datetime.today() - timedelta(days=7)
        prev_week_day_str = datetime.strftime(
                datetime.today() - timedelta(days=7), '%m/%d/%Y')
        category = Category.objects.create_category('Food')
        Balance.objects.create_expense(
                category=category,
                amount=10,
                date=prev_week_day_str,
                balance=balance
                )
        category = Category.objects.create_category('Movie')
        Balance.objects.create_expense(
                category=category,
                amount=20,
                date=prev_week_day_str,
                balance=balance
                )
        start_week = prev_week_day - timedelta(days=prev_week_day.weekday())
        end_week = start_week + timedelta(days=6)
        start_week_str = datetime.strftime(start_week, '%Y-%m-%d')
        end_week_str = datetime.strftime(end_week, '%Y-%m-%d')
        response = self.client.get(
            f'/balance/expenses/{start_week_str}/{end_week_str}/'
                )
        self.assertContains(response, '|| Food: 10')
        self.assertContains(response, '|| Movie: 20')

    def test_expenses_monthly_view(self):
        balance = Balance.objects.get(owner=self.user)
        prev_month_day_str = datetime.strftime(
                datetime.today() - timedelta(days=30), '%m/%d/%Y')
        prev_month_day = datetime.today() - timedelta(days=30)
        category = Category.objects.create_category('Food')
        Balance.objects.create_expense(
                category=category,
                amount=10,
                date=prev_month_day_str,
                balance=balance
                )
        category = Category.objects.create_category('Movie')
        Balance.objects.create_expense(
                category=category,
                amount=20,
                date=prev_month_day_str,
                balance=balance
                )
        monthdays = monthrange(
                prev_month_day.year, prev_month_day.month)
        start_month_date = date(
                prev_month_day.year, prev_month_day.month, 1)
        start_prev_m = datetime.strftime(start_month_date, '%Y-%m-%d')
        end_month_date = date(
                prev_month_day.year, prev_month_day.month, monthdays[1])
        end_prev_m = datetime.strftime(end_month_date, '%Y-%m-%d')
        response = self.client.get(
            f'/balance/expenses/m/{start_prev_m}/{end_prev_m}/'
                )
        self.assertContains(response, '|| Food: 10')
        self.assertContains(
                response, '|| Movie: 20')

    def test_expenses_yearly_view(self):
        balance = Balance.objects.get(owner=self.user)
        prev_year_day = datetime.today() - timedelta(days=365)
        prev_year_day_str = datetime.strftime(
                datetime.today() - timedelta(days=365), '%m/%d/%Y')
        category = Category.objects.create_category('Food')
        Balance.objects.create_expense(
                category=category,
                amount=10,
                date=prev_year_day_str,
                balance=balance
                )
        category = Category.objects.create_category('Movie')
        Balance.objects.create_expense(
                category=category,
                amount=20,
                date=prev_year_day_str,
                balance=balance
                )
        start_year_date = date(
                prev_year_day.year, 1, 1)
        start_prev_y = datetime.strftime(start_year_date, '%Y-%m-%d')
        end_year_date = date(
                prev_year_day.year, 12, 31)
        end_prev_y = datetime.strftime(end_year_date, '%Y-%m-%d')
        response = self.client.get(
            f'/balance/expenses/y/{start_prev_y}/{end_prev_y}/'
                )
        self.assertContains(response, '|| Food: 10')
        self.assertContains(
                response, '|| Movie: 20')
