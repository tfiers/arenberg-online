from django.test import TestCase

from core.models import User

def create_benji():
	benji = User(email="benji@minogue.biz", password="1234")
	benji.save()
	return benji

class UserTest(TestCase):
	def test_create(self):
		self.assertEqual(len(User.objects.all()), 0)
		benji = create_benji()
		self.assertEqual(len(User.objects.all()), 1)
		self.assertEqual(User.objects.all()[0], benji)

	def test_get(self):
		benji = create_benji()
		self.assertEqual(User.objects.get(email="benji@minogue.biz"), benji)

	def test_name(self):
		benji = create_benji()
		self.assertEqual(benji.get_full_name(), "")
		benji.first_name = "Benji"
		benji.last_name = "Minogue"
		benji.save()
		self.assertEqual(benji.get_full_name(), "Benji Minogue")

	def test_delete(self):
		benji = create_benji()
		self.assertEqual(len(User.objects.all()), 1)
		self.assertEqual(User.objects.all()[0], benji)
		benji.delete()
		self.assertEqual(len(User.objects.all()), 0)