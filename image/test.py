from django.test import TestCase

class TestView(TestCase):
	def test_two_is_three(self):
		self.assertEqual(2,3)

	def test_two_is_two(self):
		self.assertEqual(2,2)