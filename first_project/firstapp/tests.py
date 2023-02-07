from django.test import TestCase

# Create your tests here.


#==========views tests============

class ViewTestCase(TestCase):

	def test_home_page(self):
		resp = self.client.get('/')
		self.assertEqual(resp.status_code,200)