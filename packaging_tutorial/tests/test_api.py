"""--UnitTest for REST API application report of Monaco 2018 Racing--"""
import unittest

from packaging_tutorial.report_FEDONYUK.report_web import app


class TestReportResource(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    def test_get_report_json(self):
        response = self.client.get('/api/v1/report/?format=json&order=desc')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/json')

    def test_get_report_xml(self):
        response = self.client.get('/api/v1/report/?format=xml')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/xml')

    def test_get_report_invalid_format(self):
        response = self.client.get('/api/v1/report/?format=csv')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {'error': 'Invalid format'})

    def test_get_report_driver_json(self):
        response = self.client.get('/api/v1/report/?driver_id=SVF')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/json')

    def test_get_report_driver_xml(self):
        response = self.client.get('/api/v1/report/?format=xml&driver_id=LHM')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/xml')


class TestDriversResource(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    def test_get_drivers_json(self):
        response = self.client.get('/api/v1/report/drivers/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/json')

    def test_get_drivers_xml(self):
        response = self.client.get('/api/v1/report/drivers/?format=xml&order=desc')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/xml')

    def test_get_drivers_invalid_format(self):
        response = self.client.get('/api/v1/report/drivers/?format=txt')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {'error': 'Invalid format'})


if __name__ == '__main__':
    unittest.main()
