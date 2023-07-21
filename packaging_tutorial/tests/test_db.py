"""--UnitTest for models.py and db_util.py modules for creating and working with a database model--"""
import unittest
from datetime import timedelta
from flask import Flask

from packaging_tutorial.report_FEDONYUK.models import db, Driver, DriverModel, model_creation, get_abbreviation, \
    read_log_file, merged_laps, get_drivers_all, format_timedelta
from packaging_tutorial.report_FEDONYUK.db_util import get_report, get_drivers

ONE_DRIVER = [4, "KRF", "Kimi Räikkönen", "FERRARI", "1:12:639"]
EXPECTED_LIST = [['Valtteri Bottas', 'VBM'], ['Stoffel Vandoorne', 'SVM'], ['Sergio Perez', 'SPF'],
                 ['Sergey Sirotkin', 'SSW'], ['Sebastian Vettel', 'SVF'], ['Romain Grosjean', 'RGH'],
                 ['Pierre Gasly', 'PGS'], ['Nico Hulkenberg', 'NHR'], ['Marcus Ericsson', 'MES'],
                 ['Lewis Hamilton', 'LHM'], ['Lance Stroll', 'LSW'], ['Kimi Räikkönen', 'KRF'],
                 ['Kevin Magnussen', 'KMH'], ['Fernando Alonso', 'FAM'], ['Esteban Ocon', 'EOF'],
                 ['Daniel Ricciardo', 'DRR'], ['Charles Leclerc', 'CLS'], ['Carlos Sainz', 'CSR'],
                 ['Brendon Hartley', 'BHS']]


class TestModels(unittest.TestCase):
    """For testing purposes, we create SQLite database in memory."""

    @classmethod
    def setUpClass(cls):
        cls.db_uri = 'sqlite:///:memory:'
        cls.app = Flask(__name__)
        cls.app.config['SQLALCHEMY_DATABASE_URI'] = cls.db_uri
        cls.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db.init_app(cls.app)
        with cls.app.app_context():
            db.create_all()
            model_creation()

    def setUp(self):
        with self.app.app_context():
            db.session.begin_nested()

    def tearDown(self):
        with self.app.app_context():
            db.session.rollback()

    @classmethod
    def tearDownClass(cls):
        with cls.app.app_context():
            db.drop_all()
            db.session.remove()

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

    def test_get_drivers_all(self):
        drivers = get_drivers_all()
        self.assertIsInstance(drivers, list)
        self.assertTrue(all(isinstance(driver, Driver) for driver in drivers))
        self.assertGreater(len(drivers), 15)

    def test_format_timedelta(self):
        time_obj = timedelta(minutes=1, seconds=45, microseconds=500000)
        formatted_time = format_timedelta(time_obj)
        self.assertEqual(formatted_time, "1:45:500")

    def test_get_report(self):
        """Testing function get_report from module db_utils"""
        with self.app.app_context():
            one_driver = get_report(driver='KRF')
            self.assertIsInstance(one_driver, list)
            self.assertEqual(one_driver, [ONE_DRIVER])
            self.assertEqual(len(one_driver), 1)

    def test_get_drivers(self):
        """Testing function get_drivers from module db_utils"""
        with self.app.app_context():
            drivers_list = get_drivers(False)
            self.assertIsInstance(drivers_list, list)
            self.assertEqual(drivers_list, EXPECTED_LIST)
            self.assertEqual(len(drivers_list), 19)

    def test_model_creation(self):
        """Testing if the data is saved correctly in the database"""
        with self.app.app_context():
            drivers_count = DriverModel.query.count()
            self.assertEqual(drivers_count, 19)

    def test_single_driver_saved_correctly(self):
        driver_list = [1, "SVF", "Sebastian Vettel", "FERRARI", "1:04:415"]
        with self.app.app_context():
            saved_driver = DriverModel.query.filter_by(driver_id=driver_list[1]).first()
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