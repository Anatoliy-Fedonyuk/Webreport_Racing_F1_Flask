from flask import current_app
from sqlalchemy.orm import sessionmaker

from packaging_tutorial.report_FEDONYUK.sqlite_creation import db, DriverModel

Session = sessionmaker()


def get_report(asc: bool = True, driver: str = None) -> list[list]:
    """Building an overall or separate report on the Monaco race F1 2018 from monaco.db"""
    with current_app.app_context():
        Session.configure(bind=db.engine)
        session = Session()
        query = session.query(DriverModel)

        if driver:
            query = query.filter_by(driver_id=driver)
        if not asc:
            query = query.order_by(DriverModel.id.desc())
        report = [driver.to_list() for driver in query.all()]

        session.close()
    return report


def get_drivers(asc: bool = True) -> list[list]:
    """Building a list of drivers on the Monaco race F1 2018 from monaco.db"""
    with current_app.app_context():
        Session.configure(bind=db.engine)
        session = Session()
        query = session.query(DriverModel).order_by(DriverModel.name)

        drivers = [[driver.name, driver.driver_id] for driver in query.all()]
        if not asc:
            drivers.reverse()

        session.close()
    return drivers

