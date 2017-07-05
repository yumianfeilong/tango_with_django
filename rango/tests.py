from django.test import TestCase

# Create your tests here.

from rango.models import Category

class CategoryMethodTest(TestCase):
    def test_ensure_views_are_positive(self):
        cat = Category(name='test',views=-1,likes=0)
        cat.save()
        self.assertEqual((cat.views >= 0 ), True)
    def test_slug_line_creation(self):
        cat = Category(name="random category string")
        cat.save()
        self.assertEqual(cat.slug, 'random-category-string')



