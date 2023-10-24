"""This module is creation REST API report of Monaco 2018 Racing"""
from flask import request, make_response
from flask_restful import Resource
from dicttoxml import dicttoxml

from packaging_tutorial.report_FEDONYUK.db_util import get_report, get_drivers


def generate_response(report, report_format):
    """this function helps to create api response server"""
    if report_format == 'json':
        return report, 200
    elif report_format == 'xml':
        xml = dicttoxml(report).decode()
        headers = {'Content-Type': 'application/xml'}
        response = make_response(xml)
        response.headers = headers
        return response
    return {'error': 'Invalid format'}, 400


class ReportResource(Resource):
    def get(self):
        report_format = request.args.get('format', 'json')
        order = request.args.get('order', 'asc')
        driver_id = request.args.get('driver_id', None)
        report = get_report(asc=(order != 'desc'), driver=driver_id)

        return generate_response(report, report_format)


class DriversResource(Resource):
    def get(self):
        report_format = request.args.get('format', 'json')
        order = request.args.get('order', 'asc')
        drivers_list = get_drivers(asc=(order != 'desc'))
        driver_id = request.args.get('driver_id', None)
        if 'driver_id' in request.args:
            drivers_list = get_report(driver=driver_id)

        return generate_response(drivers_list, report_format)
