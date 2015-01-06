from django.test import TestCase

from core.models import User

class UserTestCreate(TestCase):
	def test_create(self):
		self.assertEqual(len(User.objects.all()), 0)
		benji = User(email="benji@minogue.biz", password="1234")
		benji.save()
		self.assertEqual(len(User.objects.all()), 1)
		self.assertEqual(User.objects.all()[0], benji)


class UserTest(TestCase):
	def setUp(self):
		self.benji = User(email="benji@minogue.biz", password="1234")
		self.benji.save()

	def test_get(self):
		self.assertEqual(User.objects.get(email="benji@minogue.biz"), self.benji)

	def test_name(self):
		self.assertEqual(self.benji.get_full_name(), "")
		self.benji.first_name = "Benji"
		self.benji.last_name = "Minogue"
		self.benji.save()
		self.assertEqual(self.benji.get_full_name(), "Benji Minogue")

	def test_delete(self):
		self.assertEqual(len(User.objects.all()), 1)
		self.assertEqual(User.objects.all()[0], self.benji)
		self.benji.delete()
		self.assertEqual(len(User.objects.all()), 0)