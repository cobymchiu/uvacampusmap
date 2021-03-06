#from .views import views
#from django.contrib.auth.models import User

#
# def test_html(self):
#     self.assertContains(self.response, '<form')
#     self.assertContains(self.response, 'type="hidden"', 1)
#     self.assertContains(self.response, 'type="text"', 2)
#     self.assertContains(self.response, 'type="radio"', 3)
#     self.assertContains(self.response, 'type="submit"', 1)


from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from map.models import Measurement
from map.views import MapTemplate
from map.views import MapTemplate2

class SmokeCase(TestCase):
    #Make sure testing is working properly
    @classmethod
    def setUpTestData(cls):
        pass
    def setUp(self):
        pass
    def test_simple_math(self):
        self.assertEqual(1 + 1, 2)
    def test_incorrect_math(self):
        self.assertNotEqual(1 + 3, 2)
    def test_false(self):
        self.assertFalse(False)
    def test_true(self):
        self.assertTrue(True)

class ModelTest(TestCase):
    #Test Measurement model
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Measurement.objects.create(location='Rotunda', destination='Rice Hall', distance=2.0)
    def setUp(self):
        self.user = User.objects.create_superuser(username='foo', password='bar', email='foobar@gmail.com')
    def test_location_label(self):
        self.client.force_login(self.user)
        measurement = Measurement.objects.get(id=1)
        field_label = measurement._meta.get_field('location').verbose_name
        self.assertEqual(field_label, 'location')

    def test_destination_label(self):
        self.client.force_login(self.user)
        measurement = Measurement.objects.get(id=1)
        field_label = measurement._meta.get_field('destination').verbose_name
        self.assertEqual(field_label, 'destination')

    def test_distance_label(self):
        self.client.force_login(self.user)
        measurement = Measurement.objects.get(id=1)
        field_label = measurement._meta.get_field('distance').verbose_name
        self.assertEqual(field_label, 'distance')

    def test_max_length(self):
        self.client.force_login(self.user)
        measurement = Measurement.objects.get(id=1)
        max_length1 = measurement._meta.get_field('location').max_length
        self.assertEqual(max_length1, 200)
        max_length2 = measurement._meta.get_field('destination').max_length
        self.assertEqual(max_length2, 200)

    def test_decimal_field(self):
        self.client.force_login(self.user)
        measurement = Measurement.objects.get(id=1)
        max_digits = measurement._meta.get_field('distance').max_digits
        self.assertEqual(max_digits, 10)
        decimal_places = measurement._meta.get_field('distance').decimal_places
        self.assertEqual(decimal_places, 1)

class UrlsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Measurement.objects.create(location='Rotunda', destination='Rice Hall', distance=2.0)

    def setUp(self):
        self.user = User.objects.create_superuser(username='foo', password='bar', email='foobar@gmail.com')

    def test_view_url_exists_at_desired_location_map(self):
        self.client.force_login(self.user)
        response = self.client.get('/map/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_exists_at_desired_location_forum(self):
        self.client.force_login(self.user)
        response = self.client.get('/forum/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_exists_at_desired_location_myprofile(self):
        self.client.force_login(self.user)
        response = self.client.get('/myprofile/')
        self.assertEqual(response.status_code, 200)

    # def test_view_url_exists_at_desired_location2(self):
    #     response2 = self.client.get('/map/template2/')
    #     self.assertEqual(response2.status_code, 200)

    def test_view_url_accessible_by_name_map(self):
        self.client.force_login(self.user)
        response = self.client.get('/map/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name_forum(self):
        self.client.force_login(self.user)
        response = self.client.get('/forum/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name_forum(self):
        self.client.force_login(self.user)
        response = self.client.get('/myprofile/')
        self.assertEqual(response.status_code, 200)


    #
