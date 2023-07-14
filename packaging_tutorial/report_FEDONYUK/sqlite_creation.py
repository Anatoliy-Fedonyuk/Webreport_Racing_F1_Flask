import os
from datetime import datetime, timedelta
from pydantic import BaseModel, Field, model_validator
from flask_sqlalchemy import SQLAlchemy

from packaging_tutorial.report_FEDONYUK.report_web import app

ABBREVIATION_TXT = "abbreviations.txt"
START_LOG = "start.log"
END_LOG = "end.log"
_BASE_DIR = os.path.join(os.path.dirname(__file__), '../data/')
DATABASE_FILE = os.path.join(_BASE_DIR, 'monaco_sqlite.db')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DATABASE_FILE
db = SQLAlchemy(app)


class Driver(BaseModel):
    """Consolidated class and validate for information about drivers and F1 race Monaco"""
    driver_id: str = Field(..., pattern=r'^[A-Z]{3}$')
    name: str = Field(..., pattern=r'^[A-Z]{1}\w+\W[A-Z]{1}\w+$')
    team: str = Field(..., pattern=r'^[A-Z\W]+$')
    best_lap: timedelta

    class Config:
        orm_mode = True


class DriverModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column(db.String(3), unique=True, nullable=False)
    name = db.Column(db.String(100), unique=True, nullable=False)
    team = db.Column(db.String(100), nullable=False)
    best_lap = db.Column(db.Interval)

    def __init__(self, driver: Driver):
        self.driver_id = driver.driver_id
        self.name = driver.name
        self.team = driver.team
        self.best_lap = driver.best_lap


def get_abbreviation() -> list[dict]:
    """Function reads the file abbreviations.txt and creates a container to store Abbreviation"""
    with open(os.path.join(_BASE_DIR, ABBREVIATION_TXT), encoding='utf-8') as file:
        return [{'driver_id': (l := line.strip().split('_'))[0], 'name': l[1], 'team': l[2].strip()}
                for line in file if line.strip()]


def read_log_file(file_name) -> dict:
    """Function for reading log files."""
    with open(os.path.join(_BASE_DIR, file_name), encoding='utf-8') as file:
        return {line[:3]: line[3:].strip() for line in file if line.strip()}


def merged_laps() -> list[dict]:
    """Function reads two log file and creates a list of dictionary with start and end lap times"""
    merged_laps = []
    for driver_id, end_lap in read_log_file(END_LOG).items():
        start_lap = read_log_file(START_LOG).get(driver_id)
        if start_lap and end_lap:
            best_lap = abs(datetime.fromisoformat(end_lap) - datetime.fromisoformat(start_lap))
            driver = {'driver_id': driver_id, 'best_lap': best_lap}
            merged_laps.append(driver)
    return merged_laps


def get_drivers(path: str) -> list[dict]:
    abbreviations = get_abbreviation(path)
    merged = merged_laps(path)
    drivers_all = []
    for abbrev in abbreviations:
        for merged_data in merged:
            if abbrev['driver_id'] == merged_data['driver_id']:
                driver = {'driver_id': abbrev['driver_id'], 'name': abbrev['name'], 'team': abbrev['team'],
                          'best_lap': merged_data['best_lap']}
                drivers_all.append(driver)
    return drivers_all


def save_drivers(path: str):
    db.create_all()
    drivers = get_drivers(path)
    for index, driver_data in enumerate(drivers, start=1):
        driver = Driver(**driver_data)
        driver_model = DriverModel(driver)
        driver_model.id = index
        db.session.add(driver_model)
    db.session.commit()


if __name__ == '__main__':
    save_drivers(BASE_DIR)
