"""This script that should parse and save data from files to a model in sqlite database"""
import os
from datetime import datetime, timedelta
from pydantic import BaseModel, Field
from flask_sqlalchemy import SQLAlchemy

ABBREVIATION_TXT = "abbreviations.txt"
START_LOG = "start.log"
END_LOG = "end.log"
_BASE_DIR = os.path.join(os.path.dirname(__file__), '../data/')

db = SQLAlchemy()


class Driver(BaseModel):
    """Consolidated class and validate for information about drivers and F1 race Monaco"""
    driver_id: str = Field(..., pattern=r'^[A-Z]{3}$')
    name: str = Field(..., pattern=r'^[A-Z]{1}\w+\W[A-Z]{1}\w+$')
    team: str = Field(..., pattern=r'^[A-Z\W]+$')
    best_lap: str

    class Config:
        from_attributes = True


class DriverModel(db.Model):
    """Class that creates a Model SQLAlchemy for our database"""
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    driver_id = db.Column(db.String(3), unique=True, nullable=False)
    name = db.Column(db.String(100), unique=True, nullable=False)
    team = db.Column(db.String(100), nullable=False)
    best_lap = db.Column(db.String(50), nullable=False)

    def __init__(self, driver: Driver):
        self.driver_id = driver.driver_id
        self.name = driver.name
        self.team = driver.team
        self.best_lap = driver.best_lap

    def __repr__(self):
        return f"{self.id}, {self.driver_id}, {self.name}, {self.team}, {self.best_lap}"


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
            driver = {'driver_id': driver_id, 'best_lap': format_timedelta(best_lap)}
            merged_laps.append(driver)
    return merged_laps


def get_drivers_all() -> list[Driver]:
    """Function to create a class Driver from 3 files, comparing data by driver_id."""
    drivers_all = []  # container list of class Driver
    for abbrev in get_abbreviation():
        for merged_lap in merged_laps():
            if abbrev['driver_id'] == merged_lap['driver_id']:
                driver = Driver(driver_id=abbrev['driver_id'], name=abbrev['name'],
                                team=abbrev['team'], best_lap=merged_lap['best_lap'])
                drivers_all.append(driver)
    return drivers_all


def format_timedelta(time_obj: timedelta) -> str:
    """Function format the lap time from the format -timedelta-"""
    return f"{time_obj.seconds // 60}:{time_obj.seconds % 60:02d}:{str(time_obj.microseconds)[:3]}"


def model_creation():
    """Function writes the data of the Driver of the model SQLite"""
    db.create_all()
    drivers = sorted(get_drivers_all(), key=lambda x: x.best_lap)
    for driver in drivers:
        driver_model = DriverModel(driver)
        db.session.add(driver_model)
    db.session.commit()
