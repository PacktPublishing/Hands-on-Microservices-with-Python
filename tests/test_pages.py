from unittest import TestCase

import requests


class TestFlaskApiUsingRequests(TestCase):
    def test_home(self):
        response = requests.get('http://192.168.99.100')
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        response = requests.get('http://192.168.99.100/login')
        self.assertEqual(response.status_code, 200)

    def test_register(self):
        response = requests.get('http://192.168.99.100/register')
        self.assertEqual(response.status_code, 200)

    def test_checkout(self):
        response = requests.get('http://192.168.99.100/checkout')
        self.assertEqual(response.status_code, 200)
