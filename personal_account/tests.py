from django.test import TestCase


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
