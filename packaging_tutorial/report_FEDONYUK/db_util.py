"""---This module provides utilities for working with the database---"""
from packaging_tutorial.report_FEDONYUK.models import db, DriverModel


def get_report(asc: bool = True, driver: str = None) -> list[list]:
    """Building an overall or separate report on the Monaco race F1 2018 from monaco.db"""
    query = db.session.query(DriverModel).order_by(DriverModel.id)

    if driver:
        query = query.filter_by(driver_id=driver)
    report = [[dr.id, dr.driver_id, dr.name, dr.team, dr.best_lap] for dr in query.all()]
    if not asc:
        report.reverse()

    return report


def get_drivers(asc: bool = True) -> list[list]:
    """Building a list of drivers on the Monaco race F1 2018 from monaco.db"""
    query = db.session.query(DriverModel).order_by(DriverModel.name)

    drivers = [[driver.name, driver.driver_id] for driver in query.all()]
    if not asc:
        drivers.reverse()

    return drivers

