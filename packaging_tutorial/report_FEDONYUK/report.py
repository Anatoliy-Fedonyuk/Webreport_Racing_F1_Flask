"""This module is creation --Report of Monaco 2018 Racing F1"""
import os
from datetime import datetime, timedelta

from pydantic import BaseModel, Field, model_validator
from tabulate import tabulate

ABBREVIATION_TXT = "abbreviations.txt"
START_LOG = "start.log"
END_LOG = "end.log"
_BASE_DIR = os.path.join(os.path.dirname(__file__), '../data/')
SEPARATOR_FOR_REPORT = 18  # For this type of tabulate = 15 drivers
SEPARATOR_REPORT_DESC = 7
HEADERS = ["№/RACE", "CODE", "NAME DRIVER", "TEAM FORMULA 1", "BEST LAP"]
HEADERS2 = ["NAME DRIVER", "CODE"]


class Driver(BaseModel):
    """Consolidated class and validate for information about drivers and F1 race Monaco"""
    driver_id: str = Field(..., pattern=r'^[A-Z]{3}$')
    name: str = Field(..., pattern=r'^[A-Z]{1}\w+\W[A-Z]{1}\w+$')
    team: str = Field(..., pattern=r'^[A-Z\W]+$')
    start_lap: datetime
    end_lap: datetime
    best_lap: timedelta = None

    @model_validator(mode='before')
    def calculate_best_lap(cls, values):
        """Function to create and validate the best lap parameter"""
        if 'end_lap' in values and 'start_lap' in values:
            values['best_lap'] = abs(values['end_lap'] - values['start_lap'])
        return values


def get_abbreviation(path: str) -> list[dict]:
    """Function reads the file abbreviations.txt and creates a container to store Abbreviation"""
    with open(os.path.join(path, ABBREVIATION_TXT), encoding='utf-8') as file:
        return [{'driver_id': (l := line.strip().split('_'))[0], 'name': l[1], 'team': l[2].strip()}
                for line in file if line.strip()]


def read_log_file(file_name, path: str) -> dict:
    """Function for reading log files."""
    with open(os.path.join(path, file_name), encoding='utf-8') as file:
        return {line[:3]: line[3:].strip() for line in file if line.strip()}


def merged_laps(path: str) -> list[dict]:
    """Function reads two log file and creates a list of dictionary with start and end lap times"""
    merged_laps = []
    for driver_id, end_lap in read_log_file(END_LOG, path).items():
        start_lap = read_log_file(START_LOG, path).get(driver_id)
        merged_laps.append({'driver_id': driver_id, 'end_lap': end_lap, 'start_lap': start_lap})
    return merged_laps


def get_drivers(path: str) -> list[Driver]:
    """Function to create a class Driver from 3 files, comparing data by driver_id."""
    drivers_all = []  # container list of class Driver
    for abbrev in get_abbreviation(path):
        for merged_lap in merged_laps(path):
            if abbrev['driver_id'] == merged_lap['driver_id']:
                driver = Driver(driver_id=abbrev['driver_id'], name=abbrev['name'], team=abbrev['team'],
                                end_lap=datetime.fromisoformat(merged_lap['end_lap']),
                                start_lap=datetime.fromisoformat(merged_lap['start_lap']))
                drivers_all.append(driver)
    return drivers_all


def get_list_drivers(asc: bool, path: str = _BASE_DIR) -> list[list]:
    """Building a list of drivers on the Monaco race F1 2018."""
    sorted_drivers = sorted(get_drivers(path), key=lambda x: x.name)
    list_drivers = [[dr.name, dr.driver_id] for dr in sorted_drivers]
    if not asc:
        list_drivers.reverse()
    return list_drivers


def build_report(asc: bool = True, driver: str = None, path: str = _BASE_DIR) -> list[list]:
    """Building an overall or separate report on the Monaco race F1 2018."""
    sorted_drivers = sorted(get_drivers(path), key=lambda x: x.best_lap)
    table = []
    for i, dr in enumerate(sorted_drivers, start=1):
        table.append([i, dr.driver_id, dr.name, dr.team, format_timedelta(dr.best_lap)])
    if driver:
        table = [e for e in table if e[1] == driver]
    if not asc:
        table.reverse()
    return table


def print_report(asc: bool = True, driver: str = None, path: str = _BASE_DIR) -> None:
    """this function Prints general or specific driver report"""
    number_separate = SEPARATOR_FOR_REPORT
    if not asc:
        number_separate = SEPARATOR_REPORT_DESC
    table_sep = tabulate(build_report(asc, driver, path), HEADERS, tablefmt="rounded_outline")
    print("    -----------   Report of Monaco 2018 Racing F1   -----------")
    return print(insert_separator(table_sep, number_separate))


def print_list_drivers(asc: bool = True) -> None:
    """this function Prints our list of drivers on the Monaco race"""
    print("--List of drivers of Monaco Racing--")
    print(tabulate(get_list_drivers(asc), HEADERS2, tablefmt="rounded_outline"))


def insert_separator(table_sep: str, number_separate: int) -> str:
    """Insert a separator string after 15 racer"""
    rows = table_sep.split("\n")
    rows.insert(number_separate, "-" * len(rows[0]))
    return "\n".join(rows)


def format_timedelta(time_obj: timedelta) -> str:
    """Function format the lap time from the format -timedelta-"""
    return f"{time_obj.seconds // 60}:{time_obj.seconds % 60:02d}:{str(time_obj.microseconds)[:3]}"


if __name__ == '__main__':
    # print_report()
    # print_report(driver='KRF')
    print_report(False)
    # print_list_drivers(False)
    print_list_drivers()