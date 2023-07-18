from packaging_tutorial.report_FEDONYUK.sqlite_creation import DriverModel


def get_report(asc: bool = True, driver: str = None) -> list[list]:
    """Building an overall or separate report on the Monaco race F1 2018 from monaco.db"""
    report = [driver.to_list() for driver in DriverModel.query.all()]
    if driver:
        report = [(DriverModel.query.filter_by(driver_id=driver).first()).to_list()]
    if not asc:
        report.reverse()
    return report


def get_drivers(asc: bool = True) -> list[list]:
    """Building a list of drivers on the Monaco race F1 2018 from monaco.db"""
    sort_model = sorted(DriverModel.query.all(), key=lambda x: x.name)
    drivers = [[dr.name, dr.driver_id] for dr in sort_model]
    if not asc:
        drivers.reverse()
    return drivers
