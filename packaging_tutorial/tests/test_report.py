"""--Pytest for module <report> of Monaco 2018 Racing --"""
import sys
import os
import io
from datetime import datetime, timedelta

import pytest

from packaging_tutorial.report_FEDONYUK import report

MOCK_START_LAP = datetime(2018, 1, 1, 12, 0, 0)
MOCK_END_LAP = datetime(2018, 1, 1, 12, 1, 30)


def test_driver():
    driver_data = {"driver_id": "SVF",
                   "name": "Sebastian Vettel",
                   "team": "FERRARI",
                   "start_lap": MOCK_START_LAP,
                   "end_lap": MOCK_END_LAP}
    driver = report.Driver(**driver_data)
    assert driver.driver_id == driver_data["driver_id"]
    assert driver.name == driver_data["name"]
    assert driver.team == driver_data["team"]
    assert driver.start_lap == driver_data["start_lap"]
    assert driver.end_lap == driver_data["end_lap"]
    assert driver.best_lap == timedelta(minutes=1, seconds=30)


def test_get_list_drivers(asc=False):
    expected_list = [['Valtteri Bottas', 'VBM'], ['Stoffel Vandoorne', 'SVM'], ['Sergio Perez', 'SPF'],
                     ['Sergey Sirotkin', 'SSW'], ['Sebastian Vettel', 'SVF'], ['Romain Grosjean', 'RGH'],
                     ['Pierre Gasly', 'PGS'], ['Nico Hulkenberg', 'NHR'], ['Marcus Ericsson', 'MES'],
                     ['Lewis Hamilton', 'LHM'], ['Lance Stroll', 'LSW'], ['Kimi Räikkönen', 'KRF'],
                     ['Kevin Magnussen', 'KMH'], ['Fernando Alonso', 'FAM'], ['Esteban Ocon', 'EOF'],
                     ['Daniel Ricciardo', 'DRR'], ['Charles Leclerc', 'CLS'], ['Carlos Sainz', 'CSR'],
                     ['Brendon Hartley', 'BHS']]
    assert report.get_list_drivers(asc) == expected_list
    asc = True
    expected_list.reverse()
    assert report.get_list_drivers(asc) == expected_list


def test_build_report_driver():
    expected_driver_info = [[5, 'FAM', 'Fernando Alonso', 'MCLAREN RENAULT', '1:12:657']]
    assert report.build_report(driver='FAM') == expected_driver_info


def test_print_report():
    # Создаем объект для перехвата потока вывода
    captured_output = io.StringIO()
    sys.stdout = captured_output
    # build_report с default данными
    report.print_report()
    # Получаем фактический вывод из перехваченного потока вывода
    actual_output = captured_output.getvalue()
    # Восстанавливаем стандартный поток вывода
    sys.stdout = sys.__stdout__
    # Загружаем сохраненный ожидаемый вывод
    with open(os.path.join(report._BASE_DIR, 'expected_output.txt'), encoding='utf-8') as f:
        expected_output = f.read()
    # Проверяем соответствует ли фактический вывод ожидаемому выводу
    assert actual_output == expected_output


def test_print_report_one_driver():
    # Создаем объект для перехвата потока вывода
    captured_output = io.StringIO()
    sys.stdout = captured_output
    report.print_report(driver='KRF')
    actual_output = captured_output.getvalue()
    # Восстанавливаем стандартный поток вывода
    sys.stdout = sys.__stdout__
    expected_output = ("    -----------   Report of Monaco 2018 Racing F1   -----------\n"
                       "╭──────────┬────────┬────────────────┬──────────────────┬────────────╮\n"
                       "│   №/RACE │ CODE   │ NAME DRIVER    │ TEAM FORMULA 1   │ BEST LAP   │\n"
                       "├──────────┼────────┼────────────────┼──────────────────┼────────────┤\n"
                       "│        4 │ KRF    │ Kimi Räikkönen │ FERRARI          │ 1:12:639   │\n"
                       "╰──────────┴────────┴────────────────┴──────────────────┴────────────╯\n"
                       "----------------------------------------------------------------------\n")
    # Проверяем, соответствует ли фактический вывод ожидаемому выводу
    assert actual_output == expected_output


def test_format_timedelta():
    time_obj = timedelta(minutes=2, seconds=15, milliseconds=500)
    assert report.format_timedelta(time_obj) == "2:15:500"


if __name__ == '__main__':
    pytest.main()
