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
        self.rowser.get('http://localhost:8000')

        # She notices the page title and header mentioned personal finance
        self.assertIn('Personal Finance', self.browser.title)
        self.fail('Finish the test!')

        # She is invited to enter her income amount and category straight away

        # She types "Salary" and 1000 into a text box

        # When she hits the "Add income" button, the page updates,
        # and now the page lists:
        # "Salary: 1000" and "Account Balance: 1000"

        # She is invited to enter her expenses amount and category
        # She types "Food" and 10

        # When she hits the "Add expense" button, the page updates
        # and now the page lists:
        # "Food: 10", "Total expences: 10" and "Account balance: 990"

        # There is still a text box inviting her to add another expense.
        # She enters "Movie" and 20

        # The page updates again, and now shows both expenses,
        # Total expenses: 30, and Account balance: 970

        # Cookie wonderss whether the site will remember her list.
        # Then she sees that the site has generated a unique URL for her --
        # there is some explanatory text
        # to that effect.

        # She visits that URL - her personal finance balance is still there.

        # Satisfied, she goes back to sleep


if __name__ == '__main__':
    unittest.main(warnings='ignore')
