"""--Pytest for Web application report of Monaco 2018 Racing--"""
import re
import pytest
from flask import url_for
from bs4 import BeautifulSoup

from packaging_tutorial.report_FEDONYUK.report_web import app

NUMBER_RIDERS = 19
ONE_RIDER = 1


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_report_html(client):
    response = client.get('/report/')
    assert response.status_code == 200  # Code status check

    soup = BeautifulSoup(response.data, 'html.parser')
    res = soup.find_all('td')
    code_driver = re.findall(r"<td>([A-Z]{3})</td>", str(res))

    if 'driver_id' not in response.request.path:
        assert len(code_driver) == NUMBER_RIDERS  # Checking for 19 driver_ids
        assert len(set(code_driver)) == NUMBER_RIDERS  # Checking all unique drivers

    else:
        driver_id = response.request.args.get('driver_id')
        assert len(code_driver) == ONE_RIDER  # Checking for driver
        assert code_driver == [driver_id]  # Checking if the driver matches the request


def test_drivers_html(client):
    response = client.get('/report/drivers/')
    assert response.status_code == 200  # Code status check

    soup = BeautifulSoup(response.data, 'html.parser')
    res = soup.find_all('td')
    code_driver = re.findall(r'id=([A-Z]{3})">', str(res))

    assert len(code_driver) == NUMBER_RIDERS  # Checking for 19 driver_ids
    assert len(set(code_driver)) == NUMBER_RIDERS  # Checking all unique drivers


def test_show_report(client):
    response = client.get('/report/')
    assert response.status_code == 200
    assert b"Report of Monaco 2018 Racing F1" in response.data


def test_show_drivers(client):
    response = client.get('/report/drivers/')
    assert response.status_code == 200
    assert b"Report of Monaco 2018 Racing F1 - Drivers" in response.data


def test_show_report_desc(client):
    response = client.get('/report/', query_string={'order': 'desc'})
    assert response.status_code == 200
    assert b"Report of Monaco 2018 Racing F1" in response.data


def test_show_drivers_desc(client):
    response = client.get('/report/drivers/', query_string={'order': 'desc'})
    assert response.status_code == 200
    assert b"Report of Monaco 2018 Racing F1 - Drivers" in response.data


def test_show_report_with_driver_id(client):
    response = client.get('/report/', query_string={'driver_id': 'SVM'})
    assert response.status_code == 302  # Redirect to /report/drivers/?driver_id=SVM


def test_show_drivers_with_driver_id(client):
    response = client.get('/report/drivers/', query_string={'driver_id': 'SVM'})
    assert response.status_code == 200
    assert b"Report of Monaco 2018 Racing F1" in response.data


def test_static_file(client):
    app.config['SERVER_NAME'] = 'localhost'  # Added SERVER_NAME setting
    with app.app_context():  # Creating an application context
        response = client.get(url_for('static', filename='style.css'))
        assert response.status_code == 200
        assert response.headers['Content-Type'] == 'text/css; charset=utf-8'


if __name__ == '__main__':
    pytest.main()
