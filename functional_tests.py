from selenium import webdriver
import unittest


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_personal_account_and_retrieve_it_later(self):
        # Cookie has heard about a cool new online personal finance app.
        # She goes to check out its homepage
        self.browser.get('http://localhost:8000')

        # She notices the page title and header mentioned personal finance
        self.assertIn('Personal Finance', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Personal Finance', header_text)

        # She is invited to enter her income amount and category straight away
        income_inputbox = self.browser.find_element_by_id('id_new_income_category')
        self.assertEqual(
                income_inputbox.get_attribute('placeholder'),
                'Enter income category'
                )
        income_amountbox = self.browser.find_element_by_id('id_new_income_amount')
        self.assertEqual(
                income_amountbox.getAttribute('value'),
                0
                )
        # She types "Salary" and 1000 into a text box
        income_inputbox.send_keys('Salary')
        income_amountbox.send_keys(1000)

        # When she hits the "Add income" button, the page updates,
        # and now the page lists:
        income_button = self.browser.find_element_by_id('id_new_income_button')
        income_button.click()
        # "Salary: 1000" and "Account Balance: 1000"
        income_table = self.browser.find_element_by_id('id_income_table')
        rows = income_table.find_elements_by_tag_name('tr')
        self.assertTrue(
                any(row.text == 'Salary: 1000' for row in rows)
                )
        account_balance = self.browser.find_element_by_id('id_account_balance')
        self.assertEqual(
                account_balance.text,
                "1000"
                )

        # She is invited to enter her expenses amount and category
        # She types "Food" and 10
        expenses_inputbox = self.browser.find_element_by_id('id_new_expense_category')
        self.assertEqual(
                expenses_inputbox.get_attribute('placeholder'),
                'Enter a expense category'
                )

        expenses_amountbox = self.browser.find_element_by_id('id_new_income_amount')
        self.assertEqual(
                expenses_amountbox.getAttribute('value'),
                0
                )

        # When she hits the "Add expense" button, the page updates
        # and now the page lists:
        expenses_inputbox.send_keys("Food")
        expenses_amountbox.send_keys(10)
        expenses_button = self.browser.find_element_by_id('id_new_expense_button')
        expenses_button.click()
        # "Food: 10", "Total expences: 10" and "Account balance: 990"
        expense_table = self.browser.find_element_by_id('id_expense_table')
        rows = expense_table.find_elements_by_tag_name('tr')
        self.assertTrue(
                any(row.text == 'Food: 10' for row in rows)
                )
        total_expenses = self.browser.find_element_by_id('id_total_expenses')
        self.assertEqual(
                total_expenses.text,
                "10"
                )
        account_balance = self.browser.find_element_by_id('id_account_balance')
        self.assertEqual(
                account_balance.text,
                "990"
                )

        # There is still a text box inviting her to add another expense.
        # She enters "Movie" and 20

        # The page updates again, and now shows both expenses,
        # Total expenses: 30, and Account balance: 970

        # Cookie wonderss whether the site will remember her list.
        # Then she sees that the site has generated a unique URL for her --
        # there is some explanatory text
        # to that effect.

        # She visits that URL - her personal finance balance is still there.
        self.fail('Finish the test')
        # Satisfied, she goes back to sleep


if __name__ == '__main__':
    unittest.main(warnings='ignore')
