from selenium.common.exceptions import WebDriverException
from django.test import LiveServerTestCase
from selenium import webdriver
import time

MAX_WAIT = 10


class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_table(self, table_id, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id(table_id)
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_can_start_a_personal_account_and_retrieve_it_later(self):
        # Cookie has heard about a cool new online personal finance app.
        # She goes to check out its homepage
        self.browser.get(self.live_server_url)

        # She notices the page title and header mentioned personal finance
        self.assertIn('Personal Finance', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Personal Finance', header_text)

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
        # She types "Salary" and 1000 into a text box
        income_inputbox.send_keys('Salary')
        income_amountbox.send_keys(1000)

        # When she hits the "Add income" button, the page updates,
        # and now the page lists:
        income_button = self.browser.find_element_by_id('id_new_income_button')
        income_button.click()
        # "Salary: 1000" and "Account Balance: 1000"
        self.wait_for_row_in_table('id_income_table', 'Salary: 1000.00')

        # She is invited to enter her expenses amount and category
        # She types "Food" and 10
        expenses_inputbox = self.browser.find_element_by_id(
                                        'id_new_expense_category'
                                        )
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

        # When she hits the "Add expense" button, the page updates
        # and now the page lists:
        expenses_inputbox.send_keys("Food")
        expenses_amountbox.send_keys(10)
        expenses_button = self.browser.find_element_by_id(
                                        'id_new_expense_button'
                                        )
        expenses_button.click()
        # "Food: 10", "Total expences: 10" and "Account balance: 990"
        self.wait_for_row_in_table('id_expense_table', 'Food: 10.00')
        total_expenses = self.browser.find_element_by_id('id_total_expenses')
        self.assertEqual(
                total_expenses.text,
                "10.00"
                )

        # There is still a text box inviting her to add another expense.
        # She enters "Movie" and 20

        expenses_inputbox = self.browser.find_element_by_id(
                                        'id_new_expense_category'
                                        )

        expenses_amountbox = self.browser.find_element_by_id(
                                        'id_new_expense_amount'
                                        )
        expenses_inputbox.send_keys("Movie")
        expenses_amountbox.send_keys(20)
        expenses_button = self.browser.find_element_by_id(
                                    'id_new_expense_button'
                                    )
        expenses_button.click()
        # The page updates again, and now shows both expenses,
        # Total expenses: 30, and Account balance: 970

        self.wait_for_row_in_table('id_expense_table', 'Food: 10.00')
        self.wait_for_row_in_table('id_expense_table', 'Movie: 20.00')
        total_expenses = self.browser.find_element_by_id('id_total_expenses')
        self.assertEqual(
                total_expenses.text,
                "30.00"
                )

        account_balance = self.browser.find_element_by_id(
                                                   'id_account_balance'
                                                   )
        self.assertEqual(
                account_balance.text,
                "970.00"
                )
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
        # She types "Salary" and 1000 into a text box
        income_inputbox.send_keys('Salary')
        income_amountbox.send_keys(1000)

        # When she hits the "Add income" button, the page updates,
        # and now the page lists:
        income_button = self.browser.find_element_by_id('id_new_income_button')
        income_button.click()
        # "Salary: 1000" and "Account Balance: 1000"
        self.wait_for_row_in_table('id_income_table', 'Salary: 1000.00')

        # She notices that her balance has a unique URL
        cookie_balance_url = self.browser.current_url
        self.assertRegex(cookie_balance_url, '/personal_account/.+')

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
        self.assertNotIn('Food: 10', page_text)

        # Little Cookie starts a new balance by entering a new item.

        income_inputbox = self.browser.find_element_by_id(
                                    'id_new_income_category'
                                    )
        income_amountbox = self.browser.find_element_by_id(
                                        'id_new_income_amount'
                                        )
        # She types "Salary" and 800 into a text box
        income_inputbox.send_keys('Salary')
        income_amountbox.send_keys(800)

        # When she hits the "Add income" button, the page updates,
        # and now the page lists:
        income_button = self.browser.find_element_by_id('id_new_income_button')
        income_button.click()
        self.wait_for_row_in_table('id_income_table', 'Salary: 800.00')

        # Little Cookie gets her own unique URL
        little_cookies_balance_url = self.browser.current_url
        self.assertRegex(little_cookies_balance_url, '/personal_account/.+')
        self.assertNotEqual(little_cookies_balance_url, cookie_balance_url)

        # Again, there is no trace of Cookie's balance
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Salary: 1000', page_text)
        self.assertIn('Salary: 800', page_text)
