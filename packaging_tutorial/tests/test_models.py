import unittest
import os
from datetime import datetime, timedelta
from flask import Flask

from packaging_tutorial.report_FEDONYUK.models import db, Driver, DriverModel, model_creation, get_abbreviation, \
    read_log_file, merged_laps, get_drivers, format_timedelta

_BASE_DIR = os.path.join(os.path.dirname(__file__), '../data/')


class TestModels(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Configure your database URI here. For testing purposes, you can use SQLite in memory.
        cls.db_uri = 'sqlite:///:memory:'
        cls.app = Flask(__name__)
        cls.app.config['SQLALCHEMY_DATABASE_URI'] = cls.db_uri
        cls.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db.init_app(cls.app)
        with cls.app.app_context():
            db.create_all()

    def setUp(self):
        with self.app.app_context():
            db.session.begin_nested()

    def tearDown(self):
        with self.app.app_context():
            db.session.rollback()

    def test_get_abbreviation(self):
        abbreviations = get_abbreviation()
        self.assertIsInstance(abbreviations, list)
        self.assertTrue(all(
            isinstance(abb, dict) and 'driver_id' in abb and 'name' in abb and 'team' in abb for abb in abbreviations))

    def test_read_log_file(self):
        log_data = read_log_file('start.log')
        self.assertIsInstance(log_data, dict)
        self.assertTrue(
            all(isinstance(driver_id, str) and isinstance(time, str) for driver_id, time in log_data.items()))

    def test_merged_laps(self):
        laps = merged_laps()
        self.assertIsInstance(laps, list)
        self.assertTrue(all(isinstance(lap, dict) and 'driver_id' in lap and 'best_lap' in lap for lap in laps))

    def test_get_drivers(self):
        drivers = get_drivers()
        self.assertIsInstance(drivers, list)
        self.assertTrue(all(isinstance(driver, Driver) for driver in drivers))

    def test_format_timedelta(self):
        time_obj = timedelta(minutes=1, seconds=45, microseconds=500000)
        formatted_time = format_timedelta(time_obj)
        self.assertEqual(formatted_time, "1:45:500")

    def test_model_creation(self):
        # Testing if the data is saved correctly in the database
        with self.app.app_context():
            model_creation()
            drivers_count = DriverModel.query.count()
            self.assertGreater(drivers_count, 0)

    def test_model_unique_constraints(self):
        # Test uniqueness constraint for driver_id and name
        driver1 = Driver(driver_id="ABC", name="John Doe", team="TEAM A", best_lap="1:30:123")
        driver2 = Driver(driver_id="ABC", name="John Doe", team="TEAM B", best_lap="1:28:456")
        with self.app.app_context():
            driver_model1 = DriverModel(driver1)
            driver_model2 = DriverModel(driver2)
            self.db_session.add(driver_model1)
            with self.assertRaises(Exception) as context:
                self.db_session.add(driver_model2)
                self.db_session.commit()
            self.assertTrue('UNIQUE constraint failed' in str(context.exception))


if __name__ == '__main__':
    unittest.main()
