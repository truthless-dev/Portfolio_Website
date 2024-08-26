from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse


class TestIndexView(TestCase):

    def test_GET(self):
        url = reverse("braille")
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)
