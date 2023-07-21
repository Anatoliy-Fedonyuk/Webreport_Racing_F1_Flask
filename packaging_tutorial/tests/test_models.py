"""--UnitTest for models.py module to create sqlite database model--"""
import unittest
from datetime import timedelta
from flask import Flask

from packaging_tutorial.report_FEDONYUK.models import db, Driver, DriverModel, model_creation, get_abbreviation, \
    read_log_file, merged_laps, get_drivers, format_timedelta


class TestModels(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """For testing purposes, we create SQLite database in memory."""
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
        abbrev = get_abbreviation()
        self.assertIsInstance(abbrev, list)
        self.assertTrue(all(
            isinstance(abb, dict) and 'driver_id' in abb and 'name' in abb and 'team' in abb for abb in abbrev))
        self.assertTrue(len(abbrev) == 19)

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
        self.assertGreater(len(drivers), 15)

    def test_format_timedelta(self):
        time_obj = timedelta(minutes=1, seconds=45, microseconds=500000)
        formatted_time = format_timedelta(time_obj)
        self.assertEqual(formatted_time, "1:45:500")

    def test_model_creation(self):
        """Testing if the data is saved correctly in the database"""
        with self.app.app_context():
            model_creation()
            drivers_count = DriverModel.query.count()
            self.assertEqual(drivers_count, 19)

    def test_single_driver_saved_correctly(self):
        driver_list = [4, "KRF", "Kimi Räikkönen", "FERRARI", "1:12:639"]
        with self.app.app_context():
            saved_driver = DriverModel.query.filter_by(driver_id=driver_list[1]).first()
            # print(saved_driver)
            self.assertIsNotNone(saved_driver)
            self.assertEqual(saved_driver.id, driver_list[0])
            self.assertEqual(saved_driver.driver_id, driver_list[1])
            self.assertEqual(saved_driver.name, driver_list[2])
            self.assertEqual(saved_driver.team, driver_list[3])
            self.assertEqual(saved_driver.best_lap, driver_list[4])

    def test_model_unique_constraints(self):
        """Test uniqueness constraint for driver_id and name"""
        driver1 = Driver(driver_id="ABC", name="John Doe", team="TEAM A", best_lap="1:30:123")
        driver2 = Driver(driver_id="ABC", name="John Doe", team="TEAM B", best_lap="1:28:456")
        with self.app.app_context():
            driver_model1 = DriverModel(driver1)
            driver_model2 = DriverModel(driver2)
            db.session.add(driver_model1)
            with self.assertRaises(Exception) as context:
                db.session.add(driver_model2)
                db.session.commit()
            self.assertTrue('UNIQUE constraint failed' in str(context.exception))


if __name__ == '__main__':
    unittest.main()
