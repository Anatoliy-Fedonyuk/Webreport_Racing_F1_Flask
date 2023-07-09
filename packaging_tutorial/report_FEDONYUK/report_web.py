"""This module is creation Web Report of Monaco 2018 Racing using Flask framework"""
from flask import Flask, render_template, request, redirect
from flask_restful import Api
from flasgger import Swagger

from packaging_tutorial.report_FEDONYUK.report import build_report, get_list_drivers
from packaging_tutorial.report_FEDONYUK.report_api import ReportResource, DriversResource

app = Flask(__name__)
api = Api(app, prefix='/api/v1/')
swagger = Swagger(app, template_file='Swagger/swagger.yml')

api.add_resource(ReportResource, 'report/')
api.add_resource(DriversResource, 'report/drivers/')


@app.errorhandler(404)
def handle_not_found_error(error):
    """Handle 404 Not Found error"""
    return redirect('/apidocs/'), 404


@app.route('/report/')
def show_report():
    """The function processes end-points '/' & '/report/' with query-parameters order and driver_id."""
    order = request.args.get('order', 'asc')  # Get the 'order' parameter from the request, default 'asc'
    asc = (order != 'desc')  # If order is not equal to 'desc' then asc=True, otherwise asc=False

    if 'driver_id' in request.args:  # If we get 'driver_id' then redirect it to '/report/drivers/' for processing
        driver_id = request.args['driver_id']
        return redirect('/report/drivers/' + '?driver_id=' + driver_id)

    report = build_report(asc=asc)  # We send the generated data to display the table in report.html
    return render_template('report.html', report=report)


@app.route('/report/drivers/')
def show_drivers():
    """The function processes end-point '/report/drivers/' with query-parameters order and driver_id."""
    order = request.args.get('order', 'asc')  # Get the 'order' parameter from the request, default 'asc'
    asc = (order != 'desc')  # If order is not equal to 'desc' then asc=True, otherwise asc=False

    if 'driver_id' in request.args:  # Getting and processing query parameter 'driver_id'
        driver_id = request.args['driver_id']
        report = build_report(driver=driver_id)
        return render_template('report.html', report=report)

    drivers = get_list_drivers(asc=asc)  # We send the generated data to display the table in drivers.html
    return render_template('drivers.html', drivers=drivers)


if __name__ == '__main__':
    app.run(debug=False)

