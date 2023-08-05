from datetime import date

from django.test import TestCase

from pfx.pfxcore.model_resolver import ObjectResolver
from pfx.pfxcore.test import TestAssertMixin
from tests.models import Author, Book


class ModelResolverTest(TestAssertMixin, TestCase):

    def test_object_empty_resolver(self):
        resolver = ObjectResolver(None)
        self.assertIsNone(resolver.get_value('name'))

        resolver = ObjectResolver(object())
        with self.assertRaises(Exception):
            resolver.set_value('qwertz', 'Le Hobbit')

    def test_object_resolver(self):
        author = Author.objects.create(
            first_name='John Ronald Reuel',
            last_name='Tolkien',
            slug='jrr-tolkien')
        book = Book.objects.create(
            author=author,
            name="The Hobbit",
            pub_date=date(1937, 1, 1)
        )
        resolver = ObjectResolver(book)
        self.assertEqual(resolver.get_value('name'), 'The Hobbit')
        self.assertEqual(
            resolver.get_value('author__first_name'), 'John Ronald Reuel')
        self.assertIsNone(resolver.get_value('qwertz'))
        self.assertEqual(resolver.get_value(
            ('name', 'Author name', 'CharField')), 'The Hobbit')

        self.assertIsNone(resolver.get_value('type__name'))

        resolver.set_value('name', 'Le Hobbit')
        self.assertEqual(resolver.object.name, 'Le Hobbit')

        resolver.set_values(pages=300, rating=5)
        self.assertEqual(resolver.object.pages, 300)
        self.assertEqual(resolver.object.rating, 5)

        resolver.validate()  # assert no exception
        resolver.save()  # assert no exception

        book.refresh_from_db()
        self.assertEqual(book.name, 'Le Hobbit')
        self.assertEqual(book.pages, 300)
        self.assertEqual(book.rating, 5)
