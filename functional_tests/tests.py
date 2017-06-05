from selenium.common.exceptions import WebDriverException
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
import time
import os
from datetime import datetime, timedelta, date
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
from calendar import monthrange


MAX_WAIT = 10


class NewVisitorTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'http://' + staging_server
        self.users_count = 0

    def tearDown(self):
        self.browser.quit()

    def get_random_user(self):
        username = 'user-%d' % self.users_count
        self.users_count += 1
        password = '123456qw'
        return {
            'username': username,
            'password': password,
        }

    def init_user(self):
        user = self.get_random_user()
        self.signup_user(user)
        self.signin_user(user)

    def signup_user(self, user):
        btn_nav_users_toggle = 'btn-nav-users-toggle'

        self.click_on_button_with_id(btn_nav_users_toggle)

        btn_nav_sign_up_id = 'btn-nav-sign-up'
        btn_sign_up_id = 'btn-sign-up'
        tb_username_id = 'tb-username'
        tb_password1_id = 'tb-password1'
        tb_password2_id = 'tb-password2'

        # Register
        self.click_on_button_with_id(btn_nav_sign_up_id)

        tb_username = self.wait_for_element_on_page(tb_username_id)
        tb_password1 = self.wait_for_element_on_page(tb_password1_id)
        tb_password2 = self.wait_for_element_on_page(tb_password2_id)
        tb_username.send_keys(user['username'])
        tb_password1.send_keys(user['password'])
        tb_password2.send_keys(user['password'])

        self.click_on_button_with_id(btn_sign_up_id)

    def signin_user(self, user):
        btn_nav_users_toggle = 'btn-nav-users-toggle'

        self.click_on_button_with_id(btn_nav_users_toggle)

        btn_nav_sign_in_id = 'btn-nav-sign-in'
        btn_sign_in_id = 'btn-sign-in'
        tb_username_id = 'tb-username2'
        tb_password_id = 'tb-password'

        self.click_on_button_with_id(btn_nav_sign_in_id)

        tb_username = self.wait_for_element_on_page(tb_username_id)
        tb_password = self.browser.find_element_by_id(tb_password_id)

        tb_username.send_keys(user['username'])
        tb_password.send_keys(user['password'])

        self.click_on_button_with_id(btn_sign_in_id)

    def signout_user(self):
        btn_nav_users_toggle = 'btn-nav-users-toggle'

        self.click_on_button_with_id(btn_nav_users_toggle)

        btn_nav_sign_out_id = 'btn-nav-sign-out'

        self.click_on_button_with_id(btn_nav_sign_out_id)

    def click_on_button_with_id(self, id):
        while True:
            try:
                btn = self.wait_for_element_on_page(id)
                if btn:
                    btn.click()
                return
            except (StaleElementReferenceException) as e:
                # print(e)
                time.sleep(0.2)

    def wait_for_li_in_ul(self, ul_id, row_text):
        start_time = time.time()
        while True:
            try:
                ul = self.browser.find_element_by_id(ul_id)
                lis = ul.find_elements_by_tag_name('li')
                self.assertIn(row_text, [li.text for li in lis])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def assert_if_text(self, element_id, text, timeout=10):
        while True:
            try:
                element = self.browser.find_element_by_id(element_id)
                self.assertEqual(element.text, text)
                return
            except (StaleElementReferenceException) as e:
                # print(e)
                time.sleep(0.2)

    def wait_for_element_on_page_text(self, element_id, timeout=10):
        element = None
        while element is None:
            try:
                element = self.browser.find_element_by_id(element_id)
                self.assertNotEqual(element.text, "")
                if isinstance(element.text, str):
                    # print(element.text)
                    # import ipdb; ipdb.set_trace()
                    break
                else:
                    time.sleep(0.5)
            except (WebDriverException, StaleElementReferenceException) as e:
                time.sleep(0.5)
        return element

    def wait_for_element_on_page(self, element_id, timeout=10):
        wait = WebDriverWait(self.browser, timeout)
        wait.until(EC.element_to_be_clickable((By.ID, element_id)))
        return self.browser.find_element_by_id(element_id)

    def test_can_start_a_personal_account_and_retrieve_it_later(self):
        # Cookie has heard about a cool new online personal finance app.
        # She goes to check out its homepage
        self.browser.get(self.live_server_url)
        self.init_user()

        self.click_on_button_with_id('btn-nav-balance')

        # She notices the page title and header mentioned personal finance
        self.assertIn('Personal Finance', self.browser.title)

        self.click_on_button_with_id('id_incomes')
        # She is invited to enter her income amount and category straight away
        income_inputbox = self.browser.find_element_by_id(
                'id_new_income_category'
                )
        self.assertEqual(
                income_inputbox.get_attribute('placeholder'),
                'Enter income category'
                )
        income_amountbox = self.browser.find_element_by_id(
                'id_new_income_amount'
                )

        self.assertEqual(
                income_amountbox.get_attribute('placeholder'),
                "amount"
                )
        income_date = self.browser.find_element_by_id('id_new_income_date')
        # She types "Salary" and 1000 into a text box
        income_inputbox.send_keys('Salary')
        income_amountbox.send_keys(1000)
        today = datetime.strftime(datetime.today(), '%m/%d/%Y')
        income_date.send_keys(today)
        # When she hits the "Add income" button, the page updates,
        # and now the page lists:
        income_button = self.browser.find_element_by_id('id_new_income_button')
        income_button.click()
        self.browser.implicitly_wait(2)
        # "Salary: 1000"
        today_str = datetime.strftime(datetime.today(), '%d %b %Y')
        self.wait_for_li_in_ul(
                    'id_income_list',
                    f'{today_str} || Salary: 1000.00'
        )

        # She sees a button that tells her "Go to total balance"
        total_balance_button = self.browser.find_element_by_id(
                'id_total_balance_button'
                )

        # She click it and the page is changed to Total balance page:
        total_balance_button.click()
        self.browser.implicitly_wait(2)
        total_balance = self.wait_for_element_on_page('id_total_balance')
        self.assertEqual(
                total_balance.text,
                '1000.00'
                )
        total_income = self.browser.find_element_by_id('id_total_income')
        self.assertEqual(
                total_income.text,
                '1000.00'
                )
        # She sees that her total expenses are 0.00
        total_expenses = self.browser.find_element_by_id('id_total_expenses')
        self.assertEqual(
                total_expenses.text,
                '0.00'
                )
        # She sees the Add new expense button and click it:
        add_expenses_button = self.browser.find_element_by_id(
                'id_add_new_expense'
                )
        add_expenses_button.click()
        self.browser.implicitly_wait(2)
        # She is invited to enter her expenses amount and category
        expenses_inputbox = self.wait_for_element_on_page(
                'id_new_expense_category'
                )
        # She types "Food" and 10
        self.assertEqual(
                expenses_inputbox.get_attribute('placeholder'),
                'Enter a expense category'
                )

        expenses_amountbox = self.browser.find_element_by_id(
                'id_new_expense_amount'
                )
        self.assertEqual(
                expenses_amountbox.get_attribute('placeholder'),
                "amount"
                )
        expenses_date = self.browser.find_element_by_id('id_new_expense_date')

        # When she hits the "Add expense" button, the page updates
        # and now the page lists:
        expenses_inputbox.send_keys("Food")
        expenses_amountbox.send_keys(10)
        today = datetime.strftime(datetime.today(), '%m/%d/%Y')
        expenses_date.send_keys(today)
        expenses_button = self.browser.find_element_by_id(
                'id_new_expense_button'
                )
        expenses_button.click()
        self.browser.implicitly_wait(2)
        # "Food: 10", "Total expences: 10"
        today_str = datetime.strftime(datetime.today(), '%d %b %Y')
        self.wait_for_li_in_ul(
                'id_expenses_list',
                f'{today_str} || Food: 10.00'
        )
        total_expenses = self.browser.find_element_by_id('id_total_expenses')
        self.assertEqual(
                total_expenses.text,
                "10.00"
                )

        # There is still a text box inviting her to add another expense.
        # She enters "Movie" and 20

        expenses_inputbox = self.wait_for_element_on_page(
                'id_new_expense_category'
                )

        expenses_amountbox = self.browser.find_element_by_id(
                'id_new_expense_amount'
                )
        expenses_date = self.browser.find_element_by_id('id_new_expense_date')
        expenses_inputbox.send_keys("Movie")
        expenses_amountbox.send_keys(20)
        yesterday = datetime.strftime(
                    datetime.today() - timedelta(days=1), '%m/%d/%Y'
        )
        expenses_date.send_keys(yesterday)
        expenses_button = self.browser.find_element_by_id(
                'id_new_expense_button'
                )
        expenses_button.click()
        self.browser.implicitly_wait(2)
        # The page updates again, and now shows both expenses,
        today_str = datetime.strftime(datetime.today(), '%d %b %Y')
        self.wait_for_li_in_ul(
                'id_expenses_list',
                f'{today_str} || Food: 10.00'
        )
        yesterday_str = datetime.strftime(
                datetime.today() - timedelta(days=1), '%d %b %Y'
        )
        self.wait_for_li_in_ul(
                'id_expenses_list',
                f'{yesterday_str} || Movie: 20.00')

        # She sees a button that tells her "Go to total balance"
        total_balance_button = self.browser.find_element_by_id(
                'id_total_balance_button'
                )

        # She click it and the page is changed to Total balance page:
        total_balance_button.click()
        self.browser.implicitly_wait(2)
        total_balance = self.wait_for_element_on_page('id_total_balance')
        # Total expenses: 30, and Account balance: 970
        self.assertEqual(
                total_balance.text,
                "970.00"
                )

        total_expenses = self.browser.find_element_by_id('id_total_expenses')
        self.assertEqual(
                total_expenses.text,
                "30.00"
                )

        self.signout_user()

        # Cookie wonderss whether the site will remember her list.
        # Then she sees that the site has generated a unique URL for her --
        # there is some explanatory text
        # to that effect.

        # She visits that URL - her personal finance balance is still there.
        # Satisfied, she goes back to sleep

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # Cookie start a new balance
        self.browser.get(self.live_server_url)

        income_inputbox = self.browser.find_element_by_id(
                'id_new_income_category'
                )
        income_amountbox = self.browser.find_element_by_id(
                'id_new_income_amount'
                )
        income_date = self.browser.find_element_by_id('id_new_income_date')
        # She types "Salary" and 1000 into a
        income_inputbox.send_keys('Salary')
        income_amountbox.send_keys(1000)
        today = datetime.strftime(datetime.today(), '%m/%d/%Y')
        income_date.send_keys(today)
        # When she hits the "Add income" button, the page updates,
        # and now the page lists:
        income_button = self.browser.find_element_by_id('id_new_income_button')
        income_button.click()
        self.browser.implicitly_wait(2)
        today_str = datetime.strftime(datetime.today(), '%d %b %Y')
        # "Salary: 1000" and "Account Balance: 1000"
        self.wait_for_li_in_ul(
                'id_income_list',
                f'{today_str} || Salary: 1000.00'
        )

        # She notices that her balance has a unique URL
        cookie_balance_url = self.browser.current_url
        self.assertRegex(cookie_balance_url, '/balance/.+')

        # Now a new user, Little Cookie, comes along to the site.

        # we use a new browser session to make sure that no information
        # of Cookie's is comming through from cookies etc
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Little Cookie visits the home page. There is no sign of Cookie's
        # balance
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Salary: 1000', page_text)

        # Little Cookie starts a new balance by entering a new item.

        income_inputbox = self.browser.find_element_by_id(
                'id_new_income_category'
                )
        income_amountbox = self.browser.find_element_by_id(
                'id_new_income_amount'
                )
        income_date = self.browser.find_element_by_id('id_new_income_date')
        # She types "Salary" and 800 into a text box
        income_inputbox.send_keys('Salary')
        income_amountbox.send_keys(800)
        today = datetime.strftime(datetime.today(), '%m/%d/%Y')
        income_date.send_keys(today)

        # When she hits the "Add income" button, the page updates,
        # and now the page lists:
        income_button = self.browser.find_element_by_id('id_new_income_button')
        income_button.click()
        self.browser.implicitly_wait(2)
        today_str = datetime.strftime(datetime.today(), '%d %b %Y')
        self.wait_for_li_in_ul(
                'id_income_list',
                f'{today_str} || Salary: 800.00'
        )

        # Little Cookie gets her own unique URL
        little_cookies_balance_url = self.browser.current_url
        self.assertRegex(little_cookies_balance_url, '/balance/.+')
        self.assertNotEqual(little_cookies_balance_url, cookie_balance_url)

        # Again, there is no trace of Cookie's balance
        today_str = datetime.strftime(datetime.today(), '%d %b %Y')
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn(f'{today_str} || Salary: 1000', page_text)
        self.assertIn(f'{today_str} || Salary: 800', page_text)

    def test_layout_and_styling(self):
        # Cookie goes to the home page
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # She notices the input box is nicely centered
        category_inputbox = self.browser.find_element_by_id(
                'id_new_income_category'
                )
        amount_inputbox = self.browser.find_element_by_id(
                'id_new_income_amount'
                )
        date_inputbox = self.browser.find_element_by_id('id_new_income_date')
        button = self.browser.find_element_by_id(
                'id_new_income_button'
                )
        self.assertAlmostEqual(
                category_inputbox.location['x'] +
                (category_inputbox.size['width'] +
                    amount_inputbox.size['width'] +
                    date_inputbox.size['width'] +
                    button.size['width'])/2,
                512,
                delta=10
                )
        category_inputbox.send_keys('Salary')
        amount_inputbox.send_keys(1000)
        today = datetime.strftime(datetime.today(), '%m/%d/%Y')
        date_inputbox.send_keys(today)
        button.click()
        self.browser.implicitly_wait(2)
        today_str = datetime.strftime(datetime.today(), '%d %b %Y')
        self.wait_for_li_in_ul(
                'id_income_list',
                f'{today_str} || Salary: 1000.00'
        )
        category_inputbox = self.browser.find_element_by_id(
                'id_new_income_category'
                )
        amount_inputbox = self.browser.find_element_by_id(
                'id_new_income_amount'
                )
        date_inputbox = self.browser.find_element_by_id('id_new_income_date')
        button = self.browser.find_element_by_id(
                'id_new_income_button'
                )
        self.assertAlmostEqual(
                category_inputbox.location['x'] +
                (category_inputbox.size['width'] +
                    amount_inputbox.size['width'] +
                    date_inputbox.size['width'] +
                    button.size['width'])/2,
                512,
                delta=10
                )

    def test_user_check_expenses_on_daily_basis(self):

        self.browser.get(self.live_server_url)

        # She notices the page title and header mentioned personal finance

        # She is invited to enter her income amount and category straight away
        income_inputbox = self.browser.find_element_by_id(
                'id_new_income_category'
                )
        income_amountbox = self.browser.find_element_by_id(
                'id_new_income_amount'
                )

        income_date = self.browser.find_element_by_id('id_new_income_date')
        # She types "Salary" and 1000 into a text box
        income_inputbox.send_keys('Salary')
        income_amountbox.send_keys(1000)
        today = datetime.strftime(datetime.today(), '%m/%d/%Y')
        income_date.send_keys(today)
        # When she hits the "Add income" button, the page updates,
        # and now the page lists:
        income_button = self.browser.find_element_by_id('id_new_income_button')
        income_button.click()
        self.browser.implicitly_wait(2)
        # "Salary: 1000"
        today_str = datetime.strftime(datetime.today(), '%d %b %Y')
        self.wait_for_li_in_ul(
                    'id_income_list',
                    f'{today_str} || Salary: 1000.00'
        )

        # She sees a button that tells her "Go to total balance"
        total_balance_button = self.browser.find_element_by_id(
                'id_total_balance_button'
                )

        # She click it and the page is changed to Total balance page:
        total_balance_button.click()
        self.browser.implicitly_wait(2)
        total_balance = self.wait_for_element_on_page('id_total_balance')
        self.assertEqual(
                total_balance.text,
                '1000.00'
                )
        total_income = self.browser.find_element_by_id('id_total_income')
        self.assertEqual(
                total_income.text,
                '1000.00'
                )
        # She sees that her total expenses are 0.00
        total_expenses = self.browser.find_element_by_id('id_total_expenses')
        self.assertEqual(
                total_expenses.text,
                '0.00'
                )
        # She sees the Add new expense button and click it:
        add_expenses_button = self.browser.find_element_by_id(
                'id_add_new_expense'
                )
        add_expenses_button.click()
        self.browser.implicitly_wait(2)
        # She is invited to enter her expenses amount and category
        expenses_inputbox = self.wait_for_element_on_page(
                'id_new_expense_category'
                )
        # She types "Food" and 10

        expenses_amountbox = self.browser.find_element_by_id(
                'id_new_expense_amount'
                )
        expenses_date = self.browser.find_element_by_id('id_new_expense_date')

        # When she hits the "Add expense" button, the page updates
        # and now the page lists:
        expenses_inputbox.send_keys("Food")
        expenses_amountbox.send_keys(10)
        today = datetime.strftime(datetime.today(), '%m/%d/%Y')
        expenses_date.send_keys(today)
        expenses_button = self.browser.find_element_by_id(
                'id_new_expense_button'
                )
        expenses_button.click()
        self.browser.implicitly_wait(2)
        today_str = datetime.strftime(datetime.today(), '%d %b %Y')
        # "Food: 10", "Total expences: 10"
        self.wait_for_li_in_ul(
                'id_expenses_list',
                f'{today_str} || Food: 10.00'
        )
        total_expenses = self.browser.find_element_by_id('id_total_expenses')
        self.assertEqual(
                total_expenses.text,
                "10.00"
                )

        # There is still a text box inviting her to add another expense.
        # She enters "Movie" and 20

        expenses_inputbox = self.wait_for_element_on_page(
                'id_new_expense_category'
                )

        expenses_amountbox = self.browser.find_element_by_id(
                'id_new_expense_amount'
                )
        expenses_date = self.browser.find_element_by_id('id_new_expense_date')
        expenses_inputbox.send_keys("Movie")
        expenses_amountbox.send_keys(20)
        yesterday = datetime.strftime(
                datetime.today() - timedelta(days=1), '%m/%d/%Y'
        )
        expenses_date.send_keys(yesterday)
        expenses_button = self.browser.find_element_by_id(
                'id_new_expense_button'
                )
        expenses_button.click()
        self.browser.implicitly_wait(2)
        today_str = datetime.strftime(datetime.today(), '%d %b %Y')
        yesterday_str = datetime.strftime(
                datetime.today() - timedelta(days=1), '%d %b %Y'
        )
        # The page updates again, and now shows both expenses,
        self.wait_for_li_in_ul(
                'id_expenses_list',
                f'{today_str} || Food: 10.00'
        )
        self.wait_for_li_in_ul(
                'id_expenses_list',
                f'{yesterday_str} || Movie: 20.00')
        # Add some expenses from prev week

        total_expenses = self.browser.find_element_by_id('id_total_expenses')
        self.assertEqual(
                total_expenses.text,
                "30.00"
                )

        # Button for dayly view]
        daily_view_button = self.browser.find_element_by_id(
                                            'id_daily_expenses'
                                            )
        # dayly view
        daily_view_button.click()
        self.browser.implicitly_wait(2)
        day = self.wait_for_element_on_page('id_day')
        today_str = datetime.strftime(datetime.today(), '%d %b %Y')
        self.assertEqual(day.text, today_str)
        self.wait_for_li_in_ul(
                'id_expenses_list',
                '|| Food: 10.00'
        )
        total_expenses = self.browser.find_element_by_id('id_total_expenses')
        self.assertEqual(
                total_expenses.text,
                "10.00"
                )
        prev_day_button = self.browser.find_element_by_id('id_prev_day')

        # prev_day_button.send_keys(Keys.ENTER)
        prev_day_button.click()
        self.browser.implicitly_wait(2)

        yesterday_str = datetime.strftime(
                datetime.today() - timedelta(days=1), '%d %b %Y'
        )

        self.assert_if_text("id_day", yesterday_str)

        # day = self.wait_for_element_on_page_text('id_day')
        # self.assertEqual(day.text, yesterday_str)

        total_expenses = self.wait_for_element_on_page('id_total_expenses')
        self.wait_for_li_in_ul(
                'id_expenses_list',
                '|| Movie: 20.00')
        self.assertEqual(
                total_expenses.text,
                "20.00"
                )

    def test_user_check_expenses_on_week_basis(self):

        self.browser.get(self.live_server_url)

        # She notices the page title and header mentioned personal finance

        # She is invited to enter her income amount and category straight away
        income_inputbox = self.browser.find_element_by_id(
                'id_new_income_category'
                )
        income_amountbox = self.browser.find_element_by_id(
                'id_new_income_amount'
                )

        income_date = self.browser.find_element_by_id('id_new_income_date')
        # She types "Salary" and 1000 into a text box
        income_inputbox.send_keys('Salary')
        income_amountbox.send_keys(1000)
        today = datetime.strftime(datetime.today(), '%m/%d/%Y')
        income_date.send_keys(today)
        # When she hits the "Add income" button, the page updates,
        # and now the page lists:
        income_button = self.browser.find_element_by_id('id_new_income_button')
        income_button.click()
        self.browser.implicitly_wait(2)
        # "Salary: 1000"
        today_str = datetime.strftime(datetime.today(), '%d %b %Y')
        self.wait_for_li_in_ul(
                    'id_income_list',
                    f'{today_str} || Salary: 1000.00'
        )

        # She sees a button that tells her "Go to total balance"
        total_balance_button = self.browser.find_element_by_id(
                'id_total_balance_button'
                )

        # She click it and the page is changed to Total balance page:
        total_balance_button.click()
        self.browser.implicitly_wait(2)
        total_balance = self.wait_for_element_on_page('id_total_balance')
        self.assertEqual(
                total_balance.text,
                '1000.00'
                )
        total_income = self.browser.find_element_by_id('id_total_income')
        self.assertEqual(
                total_income.text,
                '1000.00'
                )
        # She sees that her total expenses are 0.00
        total_expenses = self.browser.find_element_by_id('id_total_expenses')
        self.assertEqual(
                total_expenses.text,
                '0.00'
                )
        # She sees the Add new expense button and click it:
        add_expenses_button = self.browser.find_element_by_id(
                'id_add_new_expense'
                )
        add_expenses_button.click()
        self.browser.implicitly_wait(2)
        # She is invited to enter her expenses amount and category
        expenses_inputbox = self.wait_for_element_on_page(
                'id_new_expense_category'
                )
        # She types "Food" and 10

        expenses_amountbox = self.browser.find_element_by_id(
                'id_new_expense_amount'
                )
        expenses_date = self.browser.find_element_by_id('id_new_expense_date')

        # When she hits the "Add expense" button, the page updates
        # and now the page lists:
        expenses_inputbox.send_keys("Food")
        expenses_amountbox.send_keys(10)
        today = datetime.strftime(datetime.today(), '%m/%d/%Y')
        expenses_date.send_keys(today)
        expenses_button = self.browser.find_element_by_id(
                'id_new_expense_button'
                )
        expenses_button.click()
        self.browser.implicitly_wait(2)
        today_str = datetime.strftime(datetime.today(), '%d %b %Y')
        # "Food: 10", "Total expences: 10"
        self.wait_for_li_in_ul(
                'id_expenses_list',
                f'{today_str} || Food: 10.00'
        )
        total_expenses = self.browser.find_element_by_id('id_total_expenses')
        self.assertEqual(
                total_expenses.text,
                "10.00"
                )

        # Add some expenses from prev week

        expenses_inputbox = self.wait_for_element_on_page(
                'id_new_expense_category'
                )

        expenses_amountbox = self.browser.find_element_by_id(
                'id_new_expense_amount'
                )
        expenses_date = self.browser.find_element_by_id('id_new_expense_date')
        expenses_inputbox.send_keys("Books")
        expenses_amountbox.send_keys(20)
        prev_week_day = datetime.strftime(
                datetime.today() - timedelta(days=6), '%m/%d/%Y')
        expenses_date.send_keys(prev_week_day)
        expenses_button = self.browser.find_element_by_id(
                'id_new_expense_button'
                )
        expenses_button.click()
        self.browser.implicitly_wait(2)
        prev_week_day_str = datetime.strftime(
                datetime.today() - timedelta(days=6), '%d %b %Y'
        )
        self.wait_for_li_in_ul(
                'id_expenses_list',
                f'{prev_week_day_str} || Books: 20.00')

        total_expenses = self.browser.find_element_by_id('id_total_expenses')
        self.assertEqual(
                total_expenses.text,
                "30.00"
                )
        week_view_btn = self.wait_for_element_on_page('id_weekly_expenses')
        week_view_btn.click()
        self.browser.implicitly_wait(2)
        week = self.wait_for_element_on_page('id_week')
        today = datetime.today()
        start_week = today - timedelta(days=today.weekday())
        end_week = start_week + timedelta(days=6)
        start_week_str = datetime.strftime(start_week, '%d %b %Y')
        end_week_str = datetime.strftime(end_week, '%d %b %Y')
        self.assertEqual(week.text, f'{start_week_str} - {end_week_str}')
        today_str = datetime.strftime(datetime.today(), '%d %b %Y')
        self.wait_for_li_in_ul(
                'id_expenses_list',
                f'|| Food: 10.00')
        total_expenses = self.wait_for_element_on_page('id_total_expenses')
        self.assertEqual(
                total_expenses.text,
                "10.00"
                )
        prev_week_btn = self.browser.find_element_by_id("id_prev_week")
        prev_week_btn.click()
        self.browser.implicitly_wait(2)
        end_prev_week = start_week - timedelta(days=1)
        start_prev_week = end_prev_week - timedelta(days=6)
        start_week_str = datetime.strftime(start_prev_week, '%d %b %Y')
        end_week_str = datetime.strftime(end_prev_week, '%d %b %Y')
        self.assert_if_text('id_week', f'{start_week_str} - {end_week_str}')
        # week = self.wait_for_element_on_page_text('id_week')
        # self.assertEqual(week.text, f'{start_week_str} - {end_week_str}')

        prev_week_day_str = datetime.strftime(
                datetime.today() - timedelta(days=6), '%d %b %Y'
        )
        self.wait_for_li_in_ul(
                'id_expenses_list',
                '|| Books: 20.00')

        total_expenses = self.wait_for_element_on_page('id_total_expenses')
        self.assertEqual(
                total_expenses.text,
                "20.00"
                )

    def test_user_check_expenses_on_month_basis(self):

        self.browser.get(self.live_server_url)

        # She notices the page title and header mentioned personal finance

        # She is invited to enter her income amount and category straight away
        income_inputbox = self.browser.find_element_by_id(
                'id_new_income_category'
                )
        income_amountbox = self.browser.find_element_by_id(
                'id_new_income_amount'
                )

        income_date = self.browser.find_element_by_id('id_new_income_date')
        # She types "Salary" and 1000 into a text box
        income_inputbox.send_keys('Salary')
        income_amountbox.send_keys(1000)
        today = datetime.strftime(datetime.today(), '%m/%d/%Y')
        income_date.send_keys(today)
        # When she hits the "Add income" button, the page updates,
        # and now the page lists:
        income_button = self.browser.find_element_by_id('id_new_income_button')
        income_button.click()
        self.browser.implicitly_wait(2)
        # "Salary: 1000"
        today_str = datetime.strftime(datetime.today(), '%d %b %Y')
        self.wait_for_li_in_ul(
                    'id_income_list',
                    f'{today_str} || Salary: 1000.00'
        )

        # She sees a button that tells her "Go to total balance"
        total_balance_button = self.browser.find_element_by_id(
                'id_total_balance_button'
                )

        # She click it and the page is changed to Total balance page:
        total_balance_button.click()
        self.browser.implicitly_wait(2)
        total_balance = self.wait_for_element_on_page('id_total_balance')
        self.assertEqual(
                total_balance.text,
                '1000.00'
                )
        total_income = self.browser.find_element_by_id('id_total_income')
        self.assertEqual(
                total_income.text,
                '1000.00'
                )
        # She sees that her total expenses are 0.00
        total_expenses = self.browser.find_element_by_id('id_total_expenses')
        self.assertEqual(
                total_expenses.text,
                '0.00'
                )
        # She sees the Add new expense button and click it:
        add_expenses_button = self.browser.find_element_by_id(
                'id_add_new_expense'
                )
        add_expenses_button.click()
        self.browser.implicitly_wait(2)
        # She is invited to enter her expenses amount and category
        expenses_inputbox = self.wait_for_element_on_page(
                'id_new_expense_category'
                )
        # She types "Food" and 10

        expenses_amountbox = self.browser.find_element_by_id(
                'id_new_expense_amount'
                )
        expenses_date = self.browser.find_element_by_id('id_new_expense_date')

        # When she hits the "Add expense" button, the page updates
        # and now the page lists:
        expenses_inputbox.send_keys("Food")
        expenses_amountbox.send_keys(10)
        today = datetime.strftime(datetime.today(), '%m/%d/%Y')
        expenses_date.send_keys(today)
        expenses_button = self.browser.find_element_by_id(
                'id_new_expense_button'
                )
        expenses_button.click()
        self.browser.implicitly_wait(2)
        today_str = datetime.strftime(datetime.today(), '%d %b %Y')
        # "Food: 10", "Total expences: 10"
        self.wait_for_li_in_ul(
                'id_expenses_list',
                f'{today_str} || Food: 10.00'
        )
        total_expenses = self.browser.find_element_by_id('id_total_expenses')
        self.assertEqual(
                total_expenses.text,
                "10.00"
                )

        expenses_inputbox = self.wait_for_element_on_page(
                'id_new_expense_category'
                )

        expenses_amountbox = self.browser.find_element_by_id(
                'id_new_expense_amount'
                )
        expenses_date = self.browser.find_element_by_id('id_new_expense_date')
        expenses_inputbox.send_keys("Clothes")
        expenses_amountbox.send_keys(20)
        prev_month = datetime.strftime(
                datetime.today() - timedelta(30), '%m/%d/%Y'
        )
        expenses_date.send_keys(prev_month)
        expenses_button = self.browser.find_element_by_id(
                'id_new_expense_button'
                )
        expenses_button.click()
        self.browser.implicitly_wait(2)
        prev_month_str = datetime.strftime(
                datetime.today() - timedelta(30), '%d %b %Y')
        self.wait_for_li_in_ul(
                'id_expenses_list',
                f'{prev_month_str} || Clothes: 20.00')
        total_expenses = self.browser.find_element_by_id('id_total_expenses')
        self.assertEqual(
                total_expenses.text,
                "30.00"
                )
        # month view
        monthly_expenses_btn = self.wait_for_element_on_page(
                'id_montly_expenses')
        monthly_expenses_btn.click()
        self.browser.implicitly_wait(2)
        monthdays = monthrange(datetime.today().year, datetime.today().month)
        start_month_date = date(
                datetime.today().year, datetime.today().month, 1)
        start_month = datetime.strftime(start_month_date, '%d %b %Y')
        end_month_date = date(
                datetime.today().year, datetime.today().month, monthdays[1])
        end_month = datetime.strftime(end_month_date, '%d %b %Y')

        month = self.wait_for_element_on_page('id_month')
        self.assertEqual(month.text, f'{start_month} - {end_month}')
        self.wait_for_li_in_ul(
                'id_expenses_list',
                '|| Food: 10.00')

        total_expenses = self.browser.find_element_by_id('id_total_expenses')
        self.assertEqual(
                total_expenses.text,
                "10.00"
                )
        prev_month_button = self.wait_for_element_on_page('id_prev_month')
        prev_month_button.click()
        self.browser.implicitly_wait(2)

        monthdays = monthrange(
                datetime.today().year, datetime.today().month - 1)
        start_month_date = date(
                datetime.today().year, datetime.today().month - 1, 1)
        start_prev_month = datetime.strftime(start_month_date, '%d %b %Y')
        end_month_date = date(
                datetime.today().year, datetime.today().month-1, monthdays[1])
        end_prev_month = datetime.strftime(end_month_date, '%d %b %Y')

        # month = self.wait_for_element_on_page_text('id_month')
        # self.assertEqual(
        #   month.text,
        #   f'{start_prev_month} - {end_prev_month}')
        self.assert_if_text(
                'id_month',
                f'{start_prev_month} - {end_prev_month}'
                )

        self.wait_for_li_in_ul(
                'id_expenses_list',
                '|| Clothes: 20.00')
        total_expenses = self.browser.find_element_by_id('id_total_expenses')
        self.assertEqual(
                total_expenses.text,
                "20.00"
                )

    def test_user_check_expenses_on_year_basis(self):

        self.browser.get(self.live_server_url)

        # She notices the page title and header mentioned personal finance

        # She is invited to enter her income amount and category straight away
        income_inputbox = self.browser.find_element_by_id(
                'id_new_income_category'
                )
        income_amountbox = self.browser.find_element_by_id(
                'id_new_income_amount'
                )

        income_date = self.browser.find_element_by_id('id_new_income_date')
        # She types "Salary" and 1000 into a text box
        income_inputbox.send_keys('Salary')
        income_amountbox.send_keys(1000)
        today = datetime.strftime(datetime.today(), '%m/%d/%Y')
        income_date.send_keys(today)
        # When she hits the "Add income" button, the page updates,
        # and now the page lists:
        income_button = self.browser.find_element_by_id('id_new_income_button')
        income_button.click()
        self.browser.implicitly_wait(2)
        # "Salary: 1000"
        today_str = datetime.strftime(datetime.today(), '%d %b %Y')
        self.wait_for_li_in_ul(
                    'id_income_list',
                    f'{today_str} || Salary: 1000.00'
        )

        # She sees a button that tells her "Go to total balance"
        total_balance_button = self.browser.find_element_by_id(
                'id_total_balance_button'
                )

        # She click it and the page is changed to Total balance page:
        total_balance_button.click()
        self.browser.implicitly_wait(2)
        total_balance = self.wait_for_element_on_page('id_total_balance')
        self.assertEqual(
                total_balance.text,
                '1000.00'
                )
        total_income = self.browser.find_element_by_id('id_total_income')
        self.assertEqual(
                total_income.text,
                '1000.00'
                )
        # She sees that her total expenses are 0.00
        total_expenses = self.browser.find_element_by_id('id_total_expenses')
        self.assertEqual(
                total_expenses.text,
                '0.00'
                )
        # She sees the Add new expense button and click it:
        add_expenses_button = self.browser.find_element_by_id(
                'id_add_new_expense'
                )
        add_expenses_button.click()
        self.browser.implicitly_wait(2)
        # She is invited to enter her expenses amount and category
        expenses_inputbox = self.wait_for_element_on_page(
                'id_new_expense_category'
                )
        # She types "Food" and 10

        expenses_amountbox = self.browser.find_element_by_id(
                'id_new_expense_amount'
                )
        expenses_date = self.browser.find_element_by_id('id_new_expense_date')

        # When she hits the "Add expense" button, the page updates
        # and now the page lists:
        expenses_inputbox.send_keys("Food")
        expenses_amountbox.send_keys(10)
        today = datetime.strftime(datetime.today(), '%m/%d/%Y')
        expenses_date.send_keys(today)
        expenses_button = self.browser.find_element_by_id(
                'id_new_expense_button'
                )
        expenses_button.click()
        self.browser.implicitly_wait(2)
        today_str = datetime.strftime(datetime.today(), '%d %b %Y')
        # "Food: 10", "Total expences: 10"
        self.wait_for_li_in_ul(
                'id_expenses_list',
                f'{today_str} || Food: 10.00'
        )
        total_expenses = self.browser.find_element_by_id('id_total_expenses')
        self.assertEqual(
                total_expenses.text,
                "10.00"
                )

        expenses_inputbox = self.wait_for_element_on_page(
                'id_new_expense_category'
                )

        expenses_amountbox = self.browser.find_element_by_id(
                'id_new_expense_amount'
                )
        expenses_date = self.browser.find_element_by_id('id_new_expense_date')
        expenses_inputbox.send_keys("Books")
        expenses_amountbox.send_keys(30)
        prev_year = datetime.strftime(
                datetime.today() - timedelta(365), '%m/%d/%Y'
        )
        expenses_date.send_keys(prev_year)
        expenses_button = self.browser.find_element_by_id(
                'id_new_expense_button'
                )
        expenses_button.click()
        self.browser.implicitly_wait(2)
        self.wait_for_li_in_ul(
                'id_expenses_list',
                f'{today_str} || Food: 10.00'
        )
        prev_year_str = datetime.strftime(
                datetime.today() - timedelta(365), '%d %b %Y'
        )
        self.wait_for_li_in_ul(
                'id_expenses_list',
                f'{prev_year_str} || Books: 30.00')
        total_expenses = self.browser.find_element_by_id('id_total_expenses')
        self.assertEqual(
                total_expenses.text,
                "40.00"
                )
        yearly_expenses_btn = self.wait_for_element_on_page(
                'id_yearly_expenses')
        yearly_expenses_btn.click()
        self.browser.implicitly_wait(2)
        year = self.wait_for_element_on_page('id_year')
        current_year_start = date(datetime.today().year, 1, 1)
        current_year_end = date(datetime.today().year, 12, 31)
        current_year_start_str = datetime.strftime(
                current_year_start, '%d %b %Y')
        current_year_end_str = datetime.strftime(current_year_end, '%d %b %Y')
        self.assertEqual(
                year.text,
                f'{current_year_start_str} - {current_year_end_str}')
        self.wait_for_li_in_ul(
                'id_expenses_list',
                '|| Food: 10.00')
        total_expenses = self.browser.find_element_by_id('id_total_expenses')
        self.assertEqual(
                total_expenses.text,
                "10.00"
                )
        prev_year_btn = self.wait_for_element_on_page('id_prev_year')
        prev_year_btn.click()
        self.browser.implicitly_wait(2)

        prev_year_start = date(datetime.today().year - 1, 1, 1)
        prev_year_end = date(datetime.today().year - 1, 12, 31)
        prev_year_start_str = datetime.strftime(prev_year_start, '%d %b %Y')
        prev_year_end_str = datetime.strftime(prev_year_end, '%d %b %Y')

        self.assert_if_text(
                'id_year',
                f'{prev_year_start_str} - {prev_year_end_str}'
                )

        # year = self.wait_for_element_on_page_text('id_year')
        # self.assertEqual(
        #        year.text,
        #        f'{prev_year_start_str} - {prev_year_end_str}')
        # button for year view
        self.wait_for_li_in_ul(
                'id_expenses_list',
                '|| Books: 30.00')
        total_expenses = self.browser.find_element_by_id('id_total_expenses')
        self.assertEqual(
                total_expenses.text,
                "30.00"
                )

    def test_user_check_incomes_on_daily_basis(self):

        self.browser.get(self.live_server_url)

        # She notices the page title and header mentioned personal finance

        # She is invited to enter her income amount and category straight away
        income_inputbox = self.browser.find_element_by_id(
                'id_new_income_category'
                )
        income_amountbox = self.browser.find_element_by_id(
                'id_new_income_amount'
                )

        income_date = self.browser.find_element_by_id('id_new_income_date')
        # She types "Salary" and 1000 into a text box
        income_inputbox.send_keys('Salary')
        income_amountbox.send_keys(1000)
        today = datetime.strftime(datetime.today(), '%m/%d/%Y')
        income_date.send_keys(today)
        # When she hits the "Add income" button, the page updates,
        # and now the page lists:
        income_button = self.browser.find_element_by_id('id_new_income_button')
        income_button.click()

        # "Salary: 1000"
        today_str = datetime.strftime(datetime.today(), '%d %b %Y')
        self.wait_for_li_in_ul(
                    'id_income_list',
                    f'{today_str} || Salary: 1000.00'
        )

        # She sees a button that tells her "Go to total balance"
        total_balance_button = self.browser.find_element_by_id(
                'id_total_balance_button'
                )

        # She click it and the page is changed to Total balance page:
        total_balance_button.click()

        total_balance = self.wait_for_element_on_page('id_total_balance')
        self.assertEqual(
                total_balance.text,
                '1000.00'
                )
        total_income = self.browser.find_element_by_id('id_total_income')
        self.assertEqual(
                total_income.text,
                '1000.00'
                )
        # She sees that her total expenses are 0.00
        total_expenses = self.browser.find_element_by_id('id_total_expenses')
        self.assertEqual(
                total_expenses.text,
                '0.00'
                )
        # She sees the Add new expense button and click it:
        add_incomes_button = self.browser.find_element_by_id(
                'id_add_new_income'
                )
        add_incomes_button.click()

        # She is invited to enter her expenses amount and category
        income_inputbox = self.wait_for_element_on_page(
                'id_new_income_category'
                )
        income_amountbox = self.browser.find_element_by_id(
                'id_new_income_amount'
                )
        income_date = self.browser.find_element_by_id('id_new_income_date')

        income_inputbox.send_keys("Food")
        income_amountbox.send_keys(10)
        today = datetime.strftime(datetime.today(), '%m/%d/%Y')
        income_date.send_keys(today)
        income_button = self.browser.find_element_by_id(
                'id_new_income_button'
                )
        income_button.click()

        today_str = datetime.strftime(datetime.today(), '%d %b %Y')
        # "Food: 10", "Total expences: 10"
        self.wait_for_li_in_ul(
                'id_income_list',
                f'{today_str} || Food: 10.00'
        )
        total_incomes = self.browser.find_element_by_id('id_total_income')
        self.assertEqual(
                total_incomes.text,
                "1010.00"
                )

        # There is still a text box inviting her to add another expense.
        # She enters "Movie" and 20

        income_inputbox = self.wait_for_element_on_page(
                'id_new_income_category'
                )

        income_amountbox = self.browser.find_element_by_id(
                'id_new_income_amount'
                )
        income_date = self.browser.find_element_by_id('id_new_income_date')
        income_inputbox.send_keys("Movie")
        income_amountbox.send_keys(20)
        yesterday = datetime.strftime(
                datetime.today() - timedelta(days=1), '%m/%d/%Y'
        )
        income_date.send_keys(yesterday)
        income_button = self.browser.find_element_by_id(
                'id_new_income_button'
                )
        income_button.click()

        today_str = datetime.strftime(datetime.today(), '%d %b %Y')
        yesterday_str = datetime.strftime(
                datetime.today() - timedelta(days=1), '%d %b %Y'
        )
        # The page updates again, and now shows both expenses,
        self.wait_for_li_in_ul(
                'id_income_list',
                f'{today_str} || Salary: 1000.00')
        self.wait_for_li_in_ul(
                'id_income_list',
                f'{today_str} || Food: 10.00'
        )
        self.wait_for_li_in_ul(
                'id_income_list',
                f'{yesterday_str} || Movie: 20.00')
        # Add some expenses from prev week

        total_incomes = self.browser.find_element_by_id('id_total_income')
        self.assertEqual(
                total_incomes.text,
                "1030.00"
                )

        # Button for dayly view]
        daily_view_button = self.browser.find_element_by_id(
                                            'id_daily_income'
                                            )
        # dayly view
        daily_view_button.click()
        self.browser.implicitly_wait(2)
        day = self.wait_for_element_on_page('id_day')
        today_str = datetime.strftime(datetime.today(), '%d %b %Y')
        self.assertEqual(day.text, today_str)
        self.wait_for_li_in_ul(
                'id_income_list',
                '|| Food: 10.00'
        )
        total_income = self.browser.find_element_by_id('id_total_income')
        self.assertEqual(
                total_income.text,
                "1010.00"
                )
        prev_day_button = self.browser.find_element_by_id('id_prev_day')
        prev_day_button.click()
        self.browser.implicitly_wait(2)
        # prev_day_button.send_keys(Keys.ENTER)
        yesterday_str = datetime.strftime(
                datetime.today() - timedelta(days=1), '%d %b %Y'
        )

        self.assert_if_text('id_day', yesterday_str)
        # day = self.wait_for_element_on_page_text('id_day')
        # self.assertEqual(day.text, yesterday_str)

        total_income = self.wait_for_element_on_page('id_total_income')
        self.wait_for_li_in_ul(
                'id_income_list',
                '|| Movie: 20.00')
        self.assertEqual(
                total_income.text,
                "20.00"
                )

    def test_user_check_incomes_on_week_basis(self):

        self.browser.get(self.live_server_url)

        # She notices the page title and header mentioned personal finance

        # She is invited to enter her income amount and category straight away
        income_inputbox = self.browser.find_element_by_id(
                'id_new_income_category'
                )
        income_amountbox = self.browser.find_element_by_id(
                'id_new_income_amount'
                )

        income_date = self.browser.find_element_by_id('id_new_income_date')
        # She types "Salary" and 1000 into a text box
        income_inputbox.send_keys('Salary')
        income_amountbox.send_keys(1000)
        today = datetime.strftime(datetime.today(), '%m/%d/%Y')
        income_date.send_keys(today)
        # When she hits the "Add income" button, the page updates,
        # and now the page lists:
        income_button = self.browser.find_element_by_id('id_new_income_button')
        income_button.click()
        self.browser.implicitly_wait(2)
        # "Salary: 1000"
        today_str = datetime.strftime(datetime.today(), '%d %b %Y')
        self.wait_for_li_in_ul(
                    'id_income_list',
                    f'{today_str} || Salary: 1000.00'
        )

        # She sees a button that tells her "Go to total balance"
        total_balance_button = self.browser.find_element_by_id(
                'id_total_balance_button'
                )

        # She click it and the page is changed to Total balance page:
        total_balance_button.click()
        self.browser.implicitly_wait(2)
        total_balance = self.wait_for_element_on_page('id_total_balance')
        self.assertEqual(
                total_balance.text,
                '1000.00'
                )
        total_income = self.browser.find_element_by_id('id_total_income')
        self.assertEqual(
                total_income.text,
                '1000.00'
                )
        # She sees that her total expenses are 0.00
        total_expenses = self.browser.find_element_by_id('id_total_expenses')
        self.assertEqual(
                total_expenses.text,
                '0.00'
                )
        # She sees the Add new expense button and click it:
        add_incomes_button = self.browser.find_element_by_id(
                'id_add_new_income'
                )
        add_incomes_button.click()
        self.browser.implicitly_wait(2)
        # She is invited to enter her expenses amount and category
        income_inputbox = self.wait_for_element_on_page(
                'id_new_income_category'
                )
        income_amountbox = self.browser.find_element_by_id(
                'id_new_income_amount'
                )
        income_date = self.browser.find_element_by_id('id_new_income_date')

        income_inputbox.send_keys("Food")
        income_amountbox.send_keys(10)
        today = datetime.strftime(datetime.today(), '%m/%d/%Y')
        income_date.send_keys(today)
        income_button = self.browser.find_element_by_id(
                'id_new_income_button'
                )
        income_button.click()
        self.browser.implicitly_wait(2)
        today_str = datetime.strftime(datetime.today(), '%d %b %Y')
        # "Food: 10", "Total expences: 10"
        self.wait_for_li_in_ul(
                'id_income_list',
                f'{today_str} || Food: 10.00'
        )
        total_incomes = self.browser.find_element_by_id('id_total_income')
        self.assertEqual(
                total_incomes.text,
                "1010.00"
                )

        today_str = datetime.strftime(datetime.today(), '%d %b %Y')
        # The page updates again, and now shows both expenses,
        self.wait_for_li_in_ul(
                'id_income_list',
                f'{today_str} || Salary: 1000.00')
        self.wait_for_li_in_ul(
                'id_income_list',
                f'{today_str} || Food: 10.00'
        )
        # Add some expenses from prev week

        total_incomes = self.browser.find_element_by_id('id_total_income')
        self.assertEqual(
                total_incomes.text,
                "1010.00"
                )

        income_inputbox = self.wait_for_element_on_page(
                'id_new_income_category'
                )

        income_amountbox = self.browser.find_element_by_id(
                'id_new_income_amount'
                )
        income_date = self.browser.find_element_by_id('id_new_income_date')
        income_inputbox.send_keys("Books")
        income_amountbox.send_keys(20)
        prev_week_day = datetime.strftime(
                datetime.today() - timedelta(days=6), '%m/%d/%Y')
        income_date.send_keys(prev_week_day)
        income_button = self.browser.find_element_by_id(
                'id_new_income_button'
                )
        income_button.click()
        self.browser.implicitly_wait(2)
        prev_week_day_str = datetime.strftime(
                datetime.today() - timedelta(days=6), '%d %b %Y')
        self.wait_for_li_in_ul(
                'id_income_list',
                f'{prev_week_day_str} || Books: 20.00')

        total_income = self.browser.find_element_by_id('id_total_income')
        self.assertEqual(
                total_income.text,
                "1030.00"
                )
        # button for week view
        week_view_btn = self.wait_for_element_on_page('id_weekly_income')
        week_view_btn.click()
        self.browser.implicitly_wait(2)
        week = self.wait_for_element_on_page('id_week')
        today = datetime.today()
        start_week = today - timedelta(days=today.weekday())
        end_week = start_week + timedelta(days=6)
        start_week_str = datetime.strftime(start_week, '%d %b %Y')
        end_week_str = datetime.strftime(end_week, '%d %b %Y')
        self.assertEqual(week.text, f'{start_week_str} - {end_week_str}')
        today_str = datetime.strftime(datetime.today(), '%d %b %Y')
        self.wait_for_li_in_ul(
                'id_income_list',
                '|| Salary: 1000.00')
        self.wait_for_li_in_ul(
                'id_income_list',
                '|| Food: 10.00')
        total_income = self.wait_for_element_on_page('id_total_income')
        self.assertEqual(
            total_income.text,
            "1010.00"
                )
        prev_week_btn = self.browser.find_element_by_id("id_prev_week")
        prev_week_btn.click()
        self.browser.implicitly_wait(2)
        end_prev_week = start_week - timedelta(days=1)
        start_prev_week = end_prev_week - timedelta(days=6)
        start_week_str = datetime.strftime(start_prev_week, '%d %b %Y')
        end_week_str = datetime.strftime(end_prev_week, '%d %b %Y')

        # week = self.wait_for_element_on_page_text('id_week')
        # self.assertEqual(week.text, f'{start_week_str} - {end_week_str}')

        self.assert_if_text('id_week', f'{start_week_str} - {end_week_str}')

        total_income = self.wait_for_element_on_page('id_total_income')
        self.wait_for_li_in_ul(
                'id_income_list',
                '|| Books: 20.00')
        self.assertEqual(
                total_income.text,
                "20.00"
                )

    def test_user_check_incomes_on_month_basis(self):

        self.browser.get(self.live_server_url)

        # She notices the page title and header mentioned personal finance

        # She is invited to enter her income amount and category straight away
        income_inputbox = self.browser.find_element_by_id(
                'id_new_income_category'
                )
        income_amountbox = self.browser.find_element_by_id(
                'id_new_income_amount'
                )

        income_date = self.browser.find_element_by_id('id_new_income_date')
        # She types "Salary" and 1000 into a text box
        income_inputbox.send_keys('Salary')
        income_amountbox.send_keys(1000)
        today = datetime.strftime(datetime.today(), '%m/%d/%Y')
        income_date.send_keys(today)
        # When she hits the "Add income" button, the page updates,
        # and now the page lists:
        income_button = self.browser.find_element_by_id('id_new_income_button')
        income_button.click()
        self.browser.implicitly_wait(2)
        # "Salary: 1000"
        today_str = datetime.strftime(datetime.today(), '%d %b %Y')
        self.wait_for_li_in_ul(
                    'id_income_list',
                    f'{today_str} || Salary: 1000.00'
        )

        # She sees a button that tells her "Go to total balance"
        total_balance_button = self.browser.find_element_by_id(
                'id_total_balance_button'
                )

        # She click it and the page is changed to Total balance page:
        total_balance_button.click()
        self.browser.implicitly_wait(2)
        total_balance = self.wait_for_element_on_page('id_total_balance')
        self.assertEqual(
                total_balance.text,
                '1000.00'
                )
        total_income = self.browser.find_element_by_id('id_total_income')
        self.assertEqual(
                total_income.text,
                '1000.00'
                )
        # She sees that her total expenses are 0.00
        total_expenses = self.browser.find_element_by_id('id_total_expenses')
        self.assertEqual(
                total_expenses.text,
                '0.00'
                )
        # She sees the Add new expense button and click it:
        add_incomes_button = self.browser.find_element_by_id(
                'id_add_new_income'
                )
        add_incomes_button.click()
        self.browser.implicitly_wait(2)
        # She is invited to enter her expenses amount and category
        income_inputbox = self.wait_for_element_on_page(
                'id_new_income_category'
                )
        income_amountbox = self.browser.find_element_by_id(
                'id_new_income_amount'
                )
        income_date = self.browser.find_element_by_id('id_new_income_date')

        income_inputbox.send_keys("Food")
        income_amountbox.send_keys(10)
        today = datetime.strftime(datetime.today(), '%m/%d/%Y')
        income_date.send_keys(today)
        income_button = self.browser.find_element_by_id(
                'id_new_income_button'
                )
        income_button.click()
        self.browser.implicitly_wait(2)
        today_str = datetime.strftime(datetime.today(), '%d %b %Y')
        # "Food: 10", "Total expences: 10"
        self.wait_for_li_in_ul(
                'id_income_list',
                f'{today_str} || Food: 10.00'
        )
        total_incomes = self.browser.find_element_by_id('id_total_income')
        self.assertEqual(
                total_incomes.text,
                "1010.00"
                )

        # There is still a text box inviting her to add another expense.
        # She enters "Movie" and 20

        income_inputbox = self.wait_for_element_on_page(
                'id_new_income_category'
                )

        income_amountbox = self.browser.find_element_by_id(
                'id_new_income_amount'
                )
        income_date = self.browser.find_element_by_id('id_new_income_date')
        income_inputbox.send_keys("Movie")
        income_amountbox.send_keys(20)
        yesterday = datetime.strftime(
                datetime.today() - timedelta(days=1), '%m/%d/%Y'
        )
        income_date.send_keys(yesterday)
        income_button = self.browser.find_element_by_id(
                'id_new_income_button'
                )
        income_button.click()
        self.browser.implicitly_wait(2)
        today_str = datetime.strftime(datetime.today(), '%d %b %Y')
        yesterday_str = datetime.strftime(
                datetime.today() - timedelta(days=1), '%d %b %Y'
        )
        # The page updates again, and now shows both expenses,
        self.wait_for_li_in_ul(
                'id_income_list',
                f'{today_str} || Salary: 1000.00')
        self.wait_for_li_in_ul(
                'id_income_list',
                f'{today_str} || Food: 10.00'
        )
        self.wait_for_li_in_ul(
                'id_income_list',
                f'{yesterday_str} || Movie: 20.00')
        # Add some expenses from prev week

        total_incomes = self.browser.find_element_by_id('id_total_income')
        self.assertEqual(
                total_incomes.text,
                "1030.00"
                )

        income_inputbox = self.wait_for_element_on_page(
                'id_new_income_category'
                )

        income_amountbox = self.browser.find_element_by_id(
                'id_new_income_amount'
                )
        income_date = self.browser.find_element_by_id('id_new_income_date')
        income_inputbox.send_keys("Clothes")
        income_amountbox.send_keys(20)
        prev_month = datetime.strftime(
                datetime.today() - timedelta(30), '%m/%d/%Y'
        )
        income_date.send_keys(prev_month)

        income_button = self.browser.find_element_by_id(
                'id_new_income_button'
                )
        prev_month_str = datetime.strftime(
                datetime.today() - timedelta(30), '%d %b %Y'
        )
        income_button.click()
        self.browser.implicitly_wait(2)
        self.wait_for_li_in_ul(
                'id_income_list',
                f'{prev_month_str} || Clothes: 20.00')
        total_incomes = self.browser.find_element_by_id('id_total_income')
        self.assertEqual(
                total_incomes.text,
                "1050.00"
                )
        # month view
        monthly_income_btn = self.wait_for_element_on_page(
                'id_montly_income')
        monthly_income_btn.click()
        self.browser.implicitly_wait(2)
        monthdays = monthrange(datetime.today().year, datetime.today().month)
        start_month_date = date(
                datetime.today().year, datetime.today().month, 1)
        start_month = datetime.strftime(start_month_date, '%d %b %Y')
        end_month_date = date(
                datetime.today().year, datetime.today().month, monthdays[1])
        end_month = datetime.strftime(end_month_date, '%d %b %Y')

        month = self.wait_for_element_on_page('id_month')
        self.assertEqual(month.text, f'{start_month} - {end_month}')
        self.wait_for_li_in_ul(
                'id_income_list',
                '|| Salary: 1000.00')
        self.wait_for_li_in_ul(
                'id_income_list',
                '|| Food: 10.00')
        self.wait_for_li_in_ul(
                'id_income_list',
                '|| Movie: 20.00')

        total_income = self.browser.find_element_by_id('id_total_income')
        self.assertEqual(
                total_income.text,
                "1030.00"
                )
        prev_month_button = self.wait_for_element_on_page('id_prev_month')
        prev_month_button.click()
        self.browser.implicitly_wait(2)

        monthdays = monthrange(
                datetime.today().year, datetime.today().month - 1)
        start_month_date = date(
                datetime.today().year, datetime.today().month - 1, 1)
        start_prev_month = datetime.strftime(start_month_date, '%d %b %Y')
        end_month_date = date(
                datetime.today().year, datetime.today().month-1, monthdays[1])
        end_prev_month = datetime.strftime(end_month_date, '%d %b %Y')

        # month = self.wait_for_element_on_page_text('id_month')
        # self.assertEqual(month.text,
        # f'{start_prev_month} - {end_prev_month}')
        self.assert_if_text(
                'id_month',
                f'{start_prev_month} - {end_prev_month}')

        self.wait_for_li_in_ul(
                'id_income_list',
                '|| Clothes: 20.00')
        total_income = self.browser.find_element_by_id('id_total_income')
        self.assertEqual(
                total_income.text,
                "20.00"
                )

    def test_user_check_incomes_on_year_basis(self):

        self.browser.get(self.live_server_url)

        # She notices the page title and header mentioned personal finance

        # She is invited to enter her income amount and category straight away
        income_inputbox = self.browser.find_element_by_id(
                'id_new_income_category'
                )
        income_amountbox = self.browser.find_element_by_id(
                'id_new_income_amount'
                )

        income_date = self.browser.find_element_by_id('id_new_income_date')
        # She types "Salary" and 1000 into a text box
        income_inputbox.send_keys('Salary')
        income_amountbox.send_keys(1000)
        today = datetime.strftime(datetime.today(), '%m/%d/%Y')
        income_date.send_keys(today)
        # When she hits the "Add income" button, the page updates,
        # and now the page lists:
        income_button = self.browser.find_element_by_id('id_new_income_button')
        income_button.click()
        self.browser.implicitly_wait(2)
        # "Salary: 1000"
        today_str = datetime.strftime(datetime.today(), '%d %b %Y')
        self.wait_for_li_in_ul(
                    'id_income_list',
                    f'{today_str} || Salary: 1000.00'
        )

        # She sees a button that tells her "Go to total balance"
        total_balance_button = self.browser.find_element_by_id(
                'id_total_balance_button'
                )

        # She click it and the page is changed to Total balance page:
        total_balance_button.click()
        total_balance = self.wait_for_element_on_page('id_total_balance')
        self.assertEqual(
                total_balance.text,
                '1000.00'
                )
        total_income = self.browser.find_element_by_id('id_total_income')
        self.assertEqual(
                total_income.text,
                '1000.00'
                )
        # She sees that her total expenses are 0.00
        total_expenses = self.browser.find_element_by_id('id_total_expenses')
        self.assertEqual(
                total_expenses.text,
                '0.00'
                )
        # She sees the Add new expense button and click it:
        add_incomes_button = self.browser.find_element_by_id(
                'id_add_new_income'
                )
        add_incomes_button.click()
        self.browser.implicitly_wait(2)
        # She is invited to enter her expenses amount and category
        income_inputbox = self.wait_for_element_on_page(
                'id_new_income_category'
                )
        income_amountbox = self.browser.find_element_by_id(
                'id_new_income_amount'
                )
        income_date = self.browser.find_element_by_id('id_new_income_date')

        income_inputbox.send_keys("Food")
        income_amountbox.send_keys(10)
        today = datetime.strftime(datetime.today(), '%m/%d/%Y')
        income_date.send_keys(today)
        income_button = self.browser.find_element_by_id(
                'id_new_income_button'
                )
        income_button.click()
        self.browser.implicitly_wait(2)
        today_str = datetime.strftime(datetime.today(), '%d %b %Y')
        # "Food: 10", "Total expences: 10"
        self.wait_for_li_in_ul(
                'id_income_list',
                f'{today_str} || Food: 10.00'
        )
        total_incomes = self.browser.find_element_by_id('id_total_income')
        self.assertEqual(
                total_incomes.text,
                "1010.00"
                )

        income_inputbox = self.wait_for_element_on_page(
                'id_new_income_category'
                )

        income_amountbox = self.browser.find_element_by_id(
                'id_new_income_amount'
                )
        income_date = self.browser.find_element_by_id('id_new_income_date')
        income_inputbox.send_keys("Books")
        income_amountbox.send_keys(30)
        prev_year = datetime.strftime(
                datetime.today() - timedelta(365), '%m/%d/%Y'
        )
        income_date.send_keys(prev_year)
        income_button = self.browser.find_element_by_id(
                'id_new_income_button'
                )
        income_button.click()
        self.browser.implicitly_wait(2)
        prev_year_str = datetime.strftime(
                datetime.today() - timedelta(365), '%d %b %Y'
        )
        self.wait_for_li_in_ul(
                'id_income_list',
                f'{prev_year_str} || Books: 30.00')
        total_income = self.browser.find_element_by_id('id_total_income')
        self.assertEqual(
                total_income.text,
                "1040.00"
                )
        yearly_income_btn = self.wait_for_element_on_page(
                'id_yearly_income')
        yearly_income_btn.click()
        self.browser.implicitly_wait(2)
        year = self.wait_for_element_on_page('id_year')
        current_year_start = date(datetime.today().year, 1, 1)
        current_year_end = date(datetime.today().year, 12, 31)
        current_year_start_str = datetime.strftime(
                current_year_start, '%d %b %Y')
        current_year_end_str = datetime.strftime(current_year_end, '%d %b %Y')
        self.assertEqual(
                year.text,
                f'{current_year_start_str} - {current_year_end_str}')
        self.wait_for_li_in_ul(
                'id_income_list',
                '|| Salary: 1000.00')
        self.wait_for_li_in_ul(
                'id_income_list',
                '|| Food: 10.00')
        total_income = self.browser.find_element_by_id('id_total_income')
        self.assertEqual(
                total_income.text,
                "1010.00"
                )
        prev_year_btn = self.wait_for_element_on_page('id_prev_year')
        prev_year_btn.click()
        self.browser.implicitly_wait(2)

        prev_year_start = date(datetime.today().year - 1, 1, 1)
        prev_year_end = date(datetime.today().year - 1, 12, 31)
        prev_year_start_str = datetime.strftime(prev_year_start, '%d %b %Y')
        prev_year_end_str = datetime.strftime(prev_year_end, '%d %b %Y')

        self.assert_if_text(
                'id_year',
                f'{prev_year_start_str} - {prev_year_end_str}')
        # year = self.wait_for_element_on_page_text('id_year')
        # self.assertEqual(
        #        year.text,
        #        f'{prev_year_start_str} - {prev_year_end_str}')
        # button for year view
        self.wait_for_li_in_ul(
                'id_income_list',
                '|| Books: 30.00')
        total_income = self.browser.find_element_by_id('id_total_income')
        self.assertEqual(
                total_income.text,
                "30.00"
                )
        # year view
        # She sees a button that tells her "Go to total balance"
        total_balance_button = self.browser.find_element_by_id(
                'id_total_balance_button'
                )

        # She click it and the page is changed to Total balance page:
        total_balance_button.click()
        self.browser.implicitly_wait(2)

        total_balance = self.wait_for_element_on_page('id_total_balance')
        # Total expenses: 30, and Account balance: 970
        self.assertEqual(
                total_balance.text,
                "1040.00"
                )

        total_income = self.wait_for_element_on_page('id_total_income')
        # Total expenses: 30, and Account balance: 970
        self.assertEqual(
                total_income.text,
                "1040.00"
                )
        total_expenses = self.browser.find_element_by_id('id_total_expenses')
        self.assertEqual(
                total_expenses.text,
                "0.00"
                )
